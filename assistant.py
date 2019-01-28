#!/usr/bin/env python

# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function

import re
import sys

import argparse
import json
import os.path
import pathlib2 as pathlib

import subprocess
import os
import urllib
import requests
from requests.auth import HTTPBasicAuth
import yaml

#not the best approach but more readable
from lms_actions import *
from hass_actions import *

import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file
from google.assistant.library.device_helpers import register_device

# for magicMirror. pubnub auth for python
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.enums import PNReconnectionPolicy
from pubnub.pubnub import PubNub

global pubnub
#Pubnub Communication
def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel("magicmirror").message("hello from python!!").pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        print (message.message)
        # pass  # Handle new message stored in message.message

def init_pubnub():
    global pubnub
    pnconfig = PNConfiguration()
### PubNub credentials fill here!
    pnconfig.subscribe_key = ''
    pnconfig.publish_key = ''
### credentialt above!
    pnconfig.reconnect_policy = PNReconnectionPolicy.LINEAR
    pubnub = PubNub(pnconfig)
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels('magicmirror').execute()
    print ('pubnub subscription completed')

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

WARNING_NOT_REGISTERED = """
    This device is not registered. This means you will not be able to use
    Device Actions or see your device in Assistant Settings. In order to
    register this device follow instructions at:

    https://developers.google.com/assistant/sdk/guides/library/python/embed/register-device
"""

workdir = '/home/pi/squeezebox_assistant/'
audiodir = '/home/pi/squeezebox_assistant/audio/'

with open('/home/pi/squeezebox_assistant/mediavolume.json', 'r') as vol:
    setvolume = json.load(vol)

#-----------------------------------------------------google working part below

def process_event(event):
    """Pretty prints events.

    Prints all events that occur with two spaces between each new
    conversation and a single space between turns of a conversation.

    Args:
        event(event.Event): The current event to process.
    """
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        lessvol()
        #adding sound of start listening
        subprocess.Popen(["aplay", audiodir+"Fb.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pubnub.publish().channel("magicmirror").message("ON_CONVERSATION_TURN_STARTED").pn_async(my_publish_callback)
        print()
    print(event)

    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and event.args and not event.args['with_follow_on_turn']):
        pubnub.publish().channel("magicmirror").message("ON_CONVERSATION_TURN_FINISHED").pn_async(my_publish_callback)
        resvol()
        print()

    if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        pubnub.publish().channel("magicmirror").message("ON_RECOGNIZING_SPEECH_FINISHED : "+event.args['text']).pn_async(my_publish_callback)
        print()

    if event.type == EventType.ON_DEVICE_ACTION:
        for command, params in event.actions:
            print('Do command', command, 'with params', str(params))

    if event.type == EventType.ON_MEDIA_TRACK_PLAY:
        lessvol()
        print()

    if event.type == EventType.ON_MEDIA_TRACK_STOP:
        resvol()
        print()

def main():
    init_pubnub()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--device-model-id', '--device_model_id', type=str,
                        metavar='DEVICE_MODEL_ID', required=False,
                        help='the device model ID registered with Google')
    parser.add_argument('--project-id', '--project_id', type=str,
                        metavar='PROJECT_ID', required=False,
                        help='the project ID used to register this device')
    parser.add_argument('--device-config', type=str,
                        metavar='DEVICE_CONFIG_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'googlesamples-assistant',
                            'device_config_library.json'
                        ),
                        help='path to store and read device configuration')
    parser.add_argument('--credentials', type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='path to store and read OAuth2 credentials')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + Assistant.__version_str__())

    args = parser.parse_args()
    with open(args.credentials, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    device_model_id = None
    last_device_id = None
    try:
        with open(args.device_config) as f:
            device_config = json.load(f)
            device_model_id = device_config['model_id']
            last_device_id = device_config.get('last_device_id', None)
    except FileNotFoundError:
        pass

    if not args.device_model_id and not device_model_id:
        raise Exception('Missing --device-model-id option')

    # Re-register if "device_model_id" is given by the user and it differs
    # from what we previously registered with.
    should_register = (
        args.device_model_id and args.device_model_id != device_model_id)

    device_model_id = args.device_model_id or device_model_id

    with Assistant(credentials, device_model_id) as assistant:
        #adding startup sound
        subprocess.Popen(["aplay", audiodir+"Startup.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        events = assistant.start()

        device_id = assistant.device_id
        print('device_model_id:', device_model_id)
        print('device_id:', device_id + '\n')

        # Re-register if "device_id" is different from the last "device_id":
        if should_register or (device_id != last_device_id):
            if args.project_id:
                register_device(args.project_id, credentials,
                                device_model_id, device_id)
                pathlib.Path(os.path.dirname(args.device_config)).mkdir(
                    exist_ok=True)
                with open(args.device_config, 'w') as f:
                    json.dump({
                        'last_device_id': device_id,
                        'model_id': device_model_id,
                    }, f)
            else:
                print(WARNING_NOT_REGISTERED)

        for event in events:
            process_event(event)

#----------------------- music control for lms
            usrcmd=event.args
            if ('stop music').lower() in str(usrcmd).lower() or ('music stop').lower() in str(usrcmd).lower():
                assistant.stop_conversation()
                lmsstop()
            if ('play music').lower() in str(usrcmd).lower() or ('music play').lower() in str(usrcmd).lower():
                assistant.stop_conversation()
                lmsplay()
            if ('next song').lower() in str(usrcmd).lower() or ('next track').lower() in str(usrcmd).lower():
                assistant.stop_conversation()
                lmsnext()
            if ('previous song').lower() in str(usrcmd).lower() or ('previous track').lower() in str(usrcmd).lower():
                assistant.stop_conversation()
                lmsprev()

### volume control for lms
            if ('set music').lower() in str(usrcmd).lower() and ('volume to').lower() in str(usrcmd).lower():
                for volume in re.findall(r'\b\d+\b', str(usrcmd)):
                    setvol(volume)
            if ('set music volume to maximum').lower() in str(usrcmd).lower() or ('set music volume to 100').lower() in str(usrcmd).lower():
                assistant.stop_conversation()
                volmax()
            if ('make music louder').lower() in str(usrcmd).lower() or ('increase music volume').lower() in str(usrcmd).lower():
                assistant.stop_conversation()
                incvol()
            if ('make music quiet').lower() in str(usrcmd).lower() or ('decrease music volume').lower() in str(usrcmd).lower():
                assistant.stop_conversation()
                decvol()

### homeassistant commands listen
            if ('room ligh').lower() in str(usrcmd).lower() and ('switch').lower() in str(usrcmd).lower():
                assistant.stop_conversation()
                hass_action_main_light()
            if ('heat living room').lower() in str(usrcmd).lower() or ('increase living room temperature').lower() in str(usrcmd).lower():
                assistant.stop_conversation()
                hass_action_ac_heat()
            if ('turn off living room conditioner').lower() in str(usrcmd).lower() or ('living room air conditioner off').lower() in str(usrcmd).lower():
                assistant.stop_conversation()
                hass_action_ac_off()
            if ('heat bedroom').lower() in str(usrcmd).lower() or ('increase bedroom temperature').lower() in str(usrcmd).lower():
                assistant.stop_conversation()
                hass_action_ac_heat_bed()
            if ('turn off bedroom conditioner').lower() in str(usrcmd).lower() or ('bedroom air conditioner off').lower() in str(usrcmd).lower():
                assistant.stop_conversation()
                hass_action_ac_off_bed()
                
### magic mirror on/off
            if ('mirror off').lower() in str(usrcmd).lower() or ('go away').lower() in str(usrcmd).lower():
                assistant.stop_conversation()
                subprocess.call('XAUTHORITY=~pi/.Xauthority DISPLAY=:0 xset dpms force on && xset -dpms && xset s off', shell=True)
            if ('mirror on').lower() in str(usrcmd).lower() or ('wake up').lower() in str(usrcmd).lower():
                assistant.stop_conversation()
                subprocess.call('XAUTHORITY=~pi/.Xauthority DISPLAY=:0 xset dpms force on && xset -dpms && xset s off', shell=True)

if __name__ == '__main__':
    main()

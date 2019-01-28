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

from lms_actions import incvol
from lms_actions import decvol

##commented due language not supproted
#import yaml
#from gtts import gTTS
#from googletrans import Translator

import google.oauth2.credentials


#-----------------------------------------------------------------------------translation possibly will be implemented by google. so leave code here
##translation
keywordfile= workdir+'keywords_ru.yaml'
with open(keywordfile,'r') as conf:
    custom_action_keyword = yaml.load(conf)

##Speech and translator declarations
ttsfilename="/home/pi/say.mp3"
translator = Translator()
language = 'ru'

##Word translator
def trans(words,lang):
    transword= translator.translate(words, dest=lang)
    transword=transword.text
    transword=transword.replace("Text, ",'',1)
    transword=transword.strip()
    print(transword)
    return transword

#Text to speech converter with translation
def say(words):
    newword=trans(words,language)
    tts = gTTS(text=newword, lang=language)
    tts.save(ttsfilename)
    os.system("mpg123 "+ttsfilename)
    os.remove(ttsfilename)

def main():
    with Assistant(credentials, device_model_id) as assistant:
        for event in events:
            process_event(event)
#-----------------------Basic music control for lms
            usrcmd=event.args
# leave this here for possible translation in future
#            if custom_action_keyword['Dict']['Play'].lower() in str(usrcmd).lower() and custom_action_keyword['Track_change']['Next'].lower() in str(usrcmd).lower():
            if ('stop music').lower() in str(usrcmd).lower() or ('music stop').lower() in str(usrcmd).lower():
                assistant.stop_conversation()
                subprocess.Popen(requests.get(url+'p0=stop', auth=(user, passwd)), shell=True)

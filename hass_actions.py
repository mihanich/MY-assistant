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

#Hass variables
with open('/home/pi/squeezebox_assistant/hass_variables.yaml', 'r') as data:
    hassvars = yaml.load(data)
    hassurl = hassvars['basic']['hassurl']
    hasspass = hassvars['basic']['hass_api_pass']

with open('/home/pi/squeezebox_assistant/hass_entity_list.yaml', 'r') as entities:
    entity = yaml.load(entities)

#def hass_action_main_light():
#    headers = {
#    'x-ha-access': hasspass,
#    'Content-Type': 'application/json',
#    }
#    data = '{"entity_id": '+entity['switches']['wall_switch']+'}'
#    response = requests.post(hassurl+'services/switch/toggle', headers=headers, data=data)

##this is hardcoded and work variant.
#            if ('switch main light').lower() in str(usrcmd).lower() or ('toggle main light').lower() in str(usrcmd).lower():
#                assistant.stop_conversation()
def hass_action_main_light():
    headers = {
    'X-HA-Access': hasspass,
    'Content-Type': 'application/json'
    }
    data = '{"entity_id": "switch.wall_switch_left_158d0001a4efdc"}'
    response = requests.post(hassurl+'services/switch/toggle', headers=headers, data=data)
    print(response)


def hass_action_ac_heat():
    headers = {
    'x-ha-access': hasspass,
    'Content-Type': 'application/json'
    }
    data = '{"entity_id": "climate.livingroom_ac", "temperature": "28", "operation_mode": "heat"}'
    response = requests.post(hassurl+'services/climate/set_temperature', headers=headers, data=data)

def hass_action_ac_off():
    headers = {
    'x-ha-access': hasspass,
    'Content-Type': 'application/json'
    }
    data = '{"entity_id": "climate.livingroom_ac", "operation_mode": "off"}'
    response = requests.post(hassurl+'services/climate/set_operation_mode', headers=headers, data=data)

def hass_action_ac_heat_bed():
    headers = {
    'x-ha-access': hasspass,
    'Content-Type': 'application/json'
    }
    data = '{"entity_id": "climate.bedroom_ac", "temperature": "28", "operation_mode": "heat"}'
    response = requests.post(hassurl+'services/climate/set_temperature', headers=headers, data=data)

def hass_action_ac_off_bed():
    headers = {
    'x-ha-access': hasspass,
    'Content-Type': 'application/json'
    }
    data = '{"entity_id": "climate.bedroom_ac", "operation_mode": "off"}'
    response = requests.post(hassurl+'services/climate/set_operation_mode', headers=headers, data=data)

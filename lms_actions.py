import os
import json
import requests
import subprocess
import yaml

### lms variables goes here
with open('/home/pi/squeezebox_assistant/lms_variables.yaml', 'r') as data:
    lmsvar = yaml.load(data)
    user = lmsvar['basic']['user']
    passwd = lmsvar['basic']['passwd']
    url = lmsvar['basic']['url']
    defvolume = lmsvar['volume']['defvolume']
    lessvolume = lmsvar['volume']['lessvolume']
    workdir = lmsvar['directories']['workdir']
    audiodir = lmsvar['directories']['audiodir']

def resvol():
#bring music volume back
    with open(workdir+'mediavolume.json', 'r') as vol:
        setvolume = json.load(vol)
        setvolume=str(setvolume)
    subprocess.Popen(requests.get(url+'p0=mixer&p1=volume&p2='+setvolume, auth=(user, passwd)), shell=True)

def lessvol():
#less volume during assistant talking
    subprocess.Popen(requests.get(url+'p0=mixer&p1=volume&p2='+lessvolume, auth=(user, passwd)), shell=True)


#----------------------- music control for lms
def lmsstop():
    subprocess.Popen(requests.get(url+'p0=stop', auth=(user, passwd)), shell=True)

def lmsplay():
    subprocess.Popen(requests.get(url+'p0=play', auth=(user, passwd)), shell=True)

def lmsnext():
    subprocess.Popen(requests.get(url+'p0=playlist&p1=jump&p2=%2b1', auth=(user, passwd)), shell=True)

def lmsprev():
    subprocess.Popen(requests.get(url+'p0=playlist&p1=jump&p2=-1', auth=(user, passwd)), shell=True)

### volume control of localplayer.
def setvol(volume):
    subprocess.Popen(requests.get(url+'p0=mixer&p1=volume&p2='+volume, auth=(user, passwd)), shell=True)
    with open(workdir+'mediavolume.json', 'w') as vol:
        json.dump(volume, vol)

def volmax():
    subprocess.Popen(requests.get(url+'p0=mixer&p1=volume&p2=100', auth=(user, passwd)), shell=True)
    setvolume=100
    with open(workdir+'mediavolume.json', 'w') as vol:
        json.dump(setvolume, vol)

def incvol():
    with open(workdir+'mediavolume.json', 'r') as vol:
        setvolume = json.load(vol)
        setvolume=int(setvolume)
        loudervolume=setvolume+15
        loudervolume=str(loudervolume)
    subprocess.Popen(requests.get(url+'p0=mixer&p1=volume&p2='+loudervolume, auth=(user, passwd)), shell=True)
    setvolume=loudervolume
    with open(workdir+'mediavolume.json', 'w') as vol:
        json.dump(setvolume, vol)
    subprocess.Popen(["mpg123", audiodir+"musvolinc.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def decvol():
    with open(workdir+'mediavolume.json', 'r') as vol:
        setvolume = json.load(vol)
        setvolume=int(setvolume)
        loudervolume=setvolume-15
        loudervolume=str(loudervolume)
    subprocess.Popen(requests.get(url+'p0=mixer&p1=volume&p2='+loudervolume, auth=(user, passwd)), shell=True)
    setvolume=loudervolume
    with open(workdir+'mediavolume.json', 'w') as vol:
        json.dump(setvolume, vol)
    subprocess.Popen(["mpg123", audiodir+"musvoldec.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

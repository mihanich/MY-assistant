# MY-assistant
Repo for scripts and some config examples for google assistant with additional soft. Squeezebox, MagicMirror, Homeassistant and potential exansion.
Most part of code here - aggregation from available open sources like GitHub.

## NOTE
I'm just doing this for my self. 
If you want to help or improve - you're welcome. 
For code maintainers - guys, you're rock! 
Big Thank You to every person who share knowladge!

# Pre-requisites
## Hardware:
1. Raspberry Pi3B+
2. Jack audio
3. USB headset (logitech H230)
4. HDMI screen
5. Keyboard, mouse (if needed)

## Software:
1. Raspbian Noobs https://www.raspberrypi.org/downloads/noobs/ / Hassbian (for those who want all-in-one work) (https://www.home-assistant.io/docs/installation/hassbian/installation/)
2. Google Project (setup and IDs got, all info according - https://developers.google.com/assistant/sdk/guides/library/python/embed/config-dev-project-and-account)
3. Nano ( to edit some configs and assistant code) / IDE

## Base
1. I use Google Assistant SDK (python one) as a base for all integrations for now
2. As Music base I use squeezebox server (with standalone client on same machine (it was more stable))
3. Optionally you may install Homeassistant with Mosquitto and MQTT brocker for gree AC (but better to install all this to hassbian)
4. As I want to use all this on the wall - I've tryed MagicMirror. cool thing.

## Google Assistant SDK
### Installation:
1. copy client secret to /home/pi/
scp client_secret-NAME OF FILE.json pi@IP:/home/pi/
2. edit squeezebox_assistant/systemd/lmsassistant.service and insert your device ID
3. Run *install.sh* and follow instructions
4. Run squeezebox_assistant/scripts/install_service.sh to install GASDK as service
5. Just in case - reboot

### Issues handling
1. Possibly you may got endless reboot in case don't comment some code in assistant.py (in CONVERSATION_START section)
2. In case you install only GASDK - please comment actions which are not used.
3. No input/outpus sound see squeezebox_assistant/scripts/fix.sh and squeezebox_assistant/scripts/sound_install.sh for solution

## Squeezebox server and client
### Installation
This is most long and painless installation.
Google music installed as a part of server.
1. run install_lms.sh and follow instructions. several confirms required
2. read squeezebox_assistant/scripts/links_lms.txt for additional actions to do

### Usage
Open RASPBERRY_IP:9000 and setup it. After - proceed to Server Admin section and configure addons.
### Issues handling
Not found. Main pain - credentials for lms admin page. (gmusic and youtube)

## MagicMirror
### Installation
1. run squeezebox_assistant/scripts/magicmirror.sh

### Possible issues
1. change screensaver config and rotation manually (i don't know why this doesn't work)

# To Be Reviewed
## Homeassistant and MQTT
### Installation
!!! in case you want to use as smart home - install hassbian as a base.
1. run install_hass.sh (and be accurate. I'm stop using this after install hassbian as a base) and wait
2. Install mosquitto and configure it on home assistant frontend.
3. install mosquitto.serice with  'sudo cp squeezebox_assistant/systemd/mosquitto.serice /lib/systemd/system/'
4. Enable it sudo systemctl enable lmsassistant.service && sudo systemctl start lmsassistant.service
---- Mosqitto+gree brocker+shell-------
5. need look on home system

#!/bin/bash
set -o errexit
scripts_dir="$(dirname "${BASH_SOURCE[0]}")"
GIT_DIR="$(realpath $(dirname ${BASH_SOURCE[0]})/..)"
INSDIR="/home/${USER}/installs"

sudo apt-get update -y
sed 's/#.*//' ${GIT_DIR}/scripts/system-requirements.txt | xargs sudo apt-get install -y
sudo useradd -rm homeassistant -G dialout,gpio
cd /srv
sudo mkdir homeassistant
sudo chown homeassistant:homeassistant homeassistant
#sudo -u homeassistant -H -s
cd /srv/homeassistant
sudo -u homeassistant python3 -m venv .  ### trying to use sudo 'hass' to install everything
sudo -u homeassistant source bin/activate
sudo -u homeassistant python3 -m pip install wheel
sudo -u homeassistant pip3 install homeassistant
sudo -u homeassistant echo "now we'll install service for it."

sudo yes | cp -rf ${GIT_DIR}/homeassistant/configuration.yaml /home/homeassistant/.homeassistant/
sudo yes | cp -rf ${GIT_DIR}/homeassistant/themes.yaml /home/homeassistant/.homeassistant/

sudo -u homeassistant cp ${GIT_DIR}systemd/homeassistant.service /etc/systemd/system/homeassistant.service
#cd ${GIT_DIR}/systemd/
sudo systemctl --system daemon-reload
sudo systemctl enable home-assistant@homeassistant
sudo systemctl start home-assistant@homeassistant

echo "And now better go for restart. but service already started, so you may just take a tea."

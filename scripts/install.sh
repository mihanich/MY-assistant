#!/bin/bash
# Copyright 2017 Google Inc.

set -o errexit

#"VARIABLES"
scripts_dir="$(dirname "${BASH_SOURCE[0]}")"
GIT_DIR="$(realpath $(dirname ${BASH_SOURCE[0]})/..)"
INSDIR="/home/${USER}/installs"

#"MKDIRS FOR EVERYTHING"
cd /home/${USER}/

if [ -d "$INSDIR" ]; then
    cd $INSDIR/
  else
    mkdir $INSDIR
    cd $INSDIR/
fi

#"CP mediavolume file to home"
cp ${GIT_DIR}/mediavolume.json /home/${USER}

# make sure we're running as the owner of the checkout directory
RUN_AS="$(ls -ld "$scripts_dir" | awk 'NR==1 {print $3}')"
if [ "$USER" != "$RUN_AS" ]
then
    echo "This script must run as $RUN_AS, trying to change user..."
    exec sudo -u $RUN_AS $0
fi
clear
echo ""
read -r -p "Enter the your full credential file name including the path and .json extension: " credname
echo ""
read -r -p "Enter the your Google Cloud Console Project-Id: " projid
echo ""
read -r -p "Enter the modelid that was generated in the actions console: " modelid
echo ""
echo "Your Model-Id used for the project is: $modelid" >> /home/${USER}/modelid.txt

sudo apt-get update -y
sed 's/#.*//' ${GIT_DIR}/scripts/system-requirements.txt | xargs sudo apt-get install -y

cd /home/${USER}/

echo "==========Changing particulars in service files=========="
echo "==========Changing particulars in service files for Ok-Google hotword=========="
sed -i '10d' ${GIT_DIR}/systemd/lmsassistant.service
sed -i 's/saved-model-id/'$modelid'/g' ${GIT_DIR}/systemd/lmsassistant.service
sed -i 's/__USER__/'${USER}'/g' ${GIT_DIR}/systemd/lmsassistant.service

python3 -m venv env
env/bin/python -m pip install --upgrade pip setuptools wheel
source env/bin/activate

pip install -r ${GIT_DIR}/scripts/pip-requirements.txt

google-oauthlib-tool --scope https://www.googleapis.com/auth/assistant-sdk-prototype --scope https://www.googleapis.com/auth/gcm --save --headless --client-secrets $credname

echo "==========Testing the installed google assistant. Make a note of the generated Device-Id =========="
echo "========== ODAdMiN, DO NOT FORGET SETUP SCREEN FOR DEBUG =========="
echo "to stop testing press Ctrl+C . By the way reboot device."
googlesamples-assistant-hotword --project_id $projid --device_model_id $modelid

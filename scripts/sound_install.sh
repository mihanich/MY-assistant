#!/bin/bash
#
# Configure Raspberry Pi audio for USB MIC and onboard 3.5mm Jack.

cd "$(dirname "${BASH_SOURCE[0]}")/.."

asoundrc=/home/${SUDO_USER}/.asoundrc
asoundrcpi=/home/pi/.asoundrc
global_asoundrc=/etc/asound.conf

for rcfile in "$asoundrc" "$global_asoundrc"; do
  if [[ -f "$rcfile" ]] ; then
    echo "Renaming $rcfile to $rcfile.bak..."
    sudo mv "$rcfile" "$rcfile.bak"
  fi
done

sudo amixer cset numid=3 1
sudo cp audio/asound.conf "$global_asoundrc"
sudo cp audio/.asoundrc "$asoundrc"
cp audio/.asoundrc "$asoundrcpi"
echo "Installing USB MIC and onboard 3.5mm Jack config is complete"

sudo apt install mpg123 #pulseaudio pulseaudio-utils pulseaudio-module-jack
#pactl set-default-sink alsa_output.platform-soc_audio.analog-stereo
#!/bin/bash
set -o errexit
scripts_dir="$(dirname "${BASH_SOURCE[0]}")"
GIT_DIR="$(realpath $(dirname ${BASH_SOURCE[0]})/..)"
INSDIR="/home/${USER}/installs"

cd /home/${USER}/
if [ ! -d "music" ]; then
  mkdir music
fi
if [ ! -d "playlists" ]; then
  mkdir playlists
fi
if [ -d "$INSDIR" ]; then
    cd $INSDIR/
  else
    mkdir $INSDIR
    cd $INSDIR/
fi

sudo apt-get update -y
sed 's/#.*//' ${GIT_DIR}/scripts/system-requirements.txt | xargs sudo apt-get install -y

#"install of squeezebox server"
cd /home/${USER}/
wget -O logitechmediaserver_arm.deb $(wget -q -O - "http://www.mysqueezebox.com/update/?version=7.9.2&revision=1&geturl=1&os=debarm")
sudo dpkg -i logitechmediaserver_arm.deb -y
mv *.deb /home/${USER}/installs/

# If you cannot understand this, read Bash_Shell_Scripting#if_statements again.
if (whiptail --title "Install local player" --yesno "Install local squeezebox player aside of server?" 8 78); then
    echo "User selected Yes, starting install. Please wait."
    #Installing local player
    cd /home/${USER}/installs
    if [ ! -d "squeezelite" ]; then
      mkdir squeezelite
    fi
    cd squeezelite
    if [ ! -f "squeezelite-armv6hf.tar.gz" ]; then
      wget -O squeezelite-armv6hf.tar.gz http://www.gerrelt.nl/RaspberryPi/squeezelite_ralph/squeezelite-armv6hf.tar.gz
    fi
    # for newest version see: https://sourceforge.net/projects/lmsclients/files/squeezelite/linux
    tar -xvzf squeezelite-armv6hf.tar.gz
    mv squeezelite squeezelite-armv6hf
    sudo mv squeezelite-armv6hf /usr/bin
    sudo chmod a+x /usr/bin/squeezelite-armv6hf
    sudo wget http://www.gerrelt.nl/RaspberryPi/squeezelite_settings.sh
    sudo mv squeezelite_settings.sh /usr/local/bin
    sudo chmod a+x /usr/local/bin/squeezelite_settings.sh
    sudo wget http://www.gerrelt.nl/RaspberryPi/squeezelitehf.sh
    sudo mv squeezelitehf.sh /etc/init.d/squeezelite
    sudo chmod a+x /etc/init.d/squeezelite
    sudo wget http://www.gerrelt.nl/RaspberryPi/squeezelite.service
    sudo mv squeezelite.service /etc/systemd/system
    sudo systemctl enable squeezelite.service
else
    echo "User selected No, $?."
fi

#"dependencies for google music in lms"
sudo apt-get install libxml2-dev libxslt1-dev
if [ ! -f "get-pip.py" ]; then
  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
fi
sudo python get-pip.py
sudo pip install lxml gmusicapi -y
sudo cpan App::cpanminus
sudo cpanm --notest Inline
sudo cpanm --notest Inline::Python
sudo cpanm --notest IO::Socket::SSL
#"end of gmlms"

#clean up a little bit
mv get-pip.py installs/

cd /home/${USER}/

python3 -m venv env
env/bin/python -m pip install --upgrade pip setuptools wheel
source env/bin/activate

pip install -r ${GIT_DIR}/scripts/pip-requirements.txt

echo "everything installed! please reboot to be sure all ok."

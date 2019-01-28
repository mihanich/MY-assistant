#!/bin/bash
### update
sudo apt-get update && sudo apt-get upgrade -y
### dependencies
sudo apt-get install xinit xserver-xorg lxde-core lightdm git libxss1 libnss3 unclutter arandr -y

#"MKDIRS FOR EVERYTHING"
cd /home/${USER}/
if [ -d "$INSDIR" ]; then
    cd $INSDIR/
  else
    mkdir $INSDIR
    cd $INSDIR/
fi

### get and install MagicMirror with the Automatic Installer
curl -sL https://raw.githubusercontent.com/MichMich/MagicMirror/master/installers/raspberry.sh | bash
cd ~/MagicMirror
npm install
cp config/config.js.sample config/config.js
cd ..

#adding lines for rotation
sudo cat >>/boot/config.txt <<EOF
display_rotate=3
disable_splash=1
EOF

### adding pm2 for startup
sudo npm install -g pm2
pm2 startup
sudo env PATH=$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u pi --hp /home/pi

### Disable the screensaver
sudo cat >>/etc/xdg/lxsession/LXDE/autostart <<EOF
@xset s noblank
@xset s off
@xset -dpms
EOF

sudo sed '/[Seat:*]:/a xserver-command=X -s 0 -dpms' /etc/lightdm/lightdm.conf
echo "we need restart. in 5 .... 4 .... 3....2....1...now"
sleep 5s
sudo reboot

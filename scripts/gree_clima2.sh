#!/bin/bash

cd /home/pi/gree-hvac-mqtt-bridge/
node index.js --hvac-host="192.168.2.121" --mqtt-broker-url="mqtt://localhost" --mqtt-topic-prefix="home/greehvac2" --mqtt-username="homeassistant" --mqtt-password="H0me12345"
#node index.js --hvac-host="192.168.2.121" --mqtt-broker-url="mqtt://localhost" --mqtt-topic-prefix="home/greehvac" --mqtt-username="homeassistant" --mqtt-password="H0me12345"

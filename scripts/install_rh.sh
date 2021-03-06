#!/bin/bash

sudo apt-get update && sudo apt-get upgrade -y
sudo apt autoremove -y
sudo apt install wget ntp libjpeg-dev i2c-tools python-dev libffi-dev python-smbus build-essential python-pip git scons swig zip -y
sudo apt install python-rpi.gpio
sudo -H pip install cffi pillow
cd /home/"${1}" || exit
mkdir /home/"${1}"/.old_RotorHazard.old >/dev/null 2>&1
cp -r /home/"${1}"/RotorHazard /home/"${1}"/.old_RotorHazard.old/ >/dev/null 2>&1 # from here
rm -r /home/"${1}"/RotorHazard >/dev/null 2>&1                                    # in case of forced installation - from here to here
rm /home/"${1}"/temp* >/dev/null 2>&1
cp -r /home/"${1}"/RotorHazard-* /home/"${1}"/.old_RotorHazard.old/ >/dev/null 2>&1
rm -r /home/"${1}"/RotorHazard-* >/dev/null 2>&1 # to here
cd /home/"${1}" || exit
wget https://codeload.github.com/RotorHazard/RotorHazard/zip/${2} -O temp.zip
unzip temp.zip
rm temp.zip
mv /home/"${1}"/RotorHazard-${2} /home/"${1}"/RotorHazard
sudo -H pip install -r /home/"${1}"/RotorHazard/src/server/requirements.txt
sudo chmod 777 -R /home/"${1}"/RotorHazard/src/server
cd /home/"${1}" || exit
sudo git clone https://github.com/jgarff/rpi_ws281x.git
cd /home/"${1}"/rpi_ws281x || exit
sudo scons
cd /home/"${1}"/rpi_ws281x/python || exit
sudo python setup.py install
cd /home/"${1}" || exit
sudo git clone https://github.com/chrisb2/pi_ina219.git
cd /home/"${1}"/pi_ina219 || exit
sudo python setup.py install
cd /home/"${1}" || exit
sudo git clone https://github.com/rm-hull/bme280.git
cd /home/"${1}"/bme280 || exit
sudo python setup.py install
sudo apt-get install openjdk-8-jdk-headless -y
sudo rm /lib/systemd/system/rotorhazard.service
echo
echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service
echo '[Unit]' | sudo tee -a /lib/systemd/system/rotorhazard.service
echo 'Description=RotorHazard Server' | sudo tee -a /lib/systemd/system/rotorhazard.service
echo 'After=multi-user.target' | sudo tee -a /lib/systemd/system/rotorhazard.service
echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service
echo '[Service]' | sudo tee -a /lib/systemd/system/rotorhazard.service
echo 'WorkingDirectory=/home/"${1}"/RotorHazard/src/server' | sudo tee -a /lib/systemd/system/rotorhazard.service
echo 'ExecStart=/usr/bin/python server.py' | sudo tee -a /lib/systemd/system/rotorhazard.service
echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service
echo '[Install]' | sudo tee -a /lib/systemd/system/rotorhazard.service
echo 'WantedBy=multi-user.target' | sudo tee -a /lib/systemd/system/rotorhazard.service
echo
sudo chmod 644 /lib/systemd/system/rotorhazard.service
sudo systemctl daemon-reload
sudo systemctl enable rotorhazard.service

from time import sleep
import os
import sys
import platform
import json

if os.path.exists("./updater-config.json") == True:
	with open('updater-config.json') as config_file:
		data = json.load(config_file)
else:
	with open('distr-updater-config.json') as config_file:
		data = json.load(config_file)

if data['debug_mode'] == 1:
	linux_testing = True
else:
	linux_testing = False 

if linux_testing == True:
	user = data['debug_user']
else:
	user = data['pi_user']

preffered_RH_version = data['RH_version']   #### can be 'beta'or 'master' or 'user_defined' - default 'stable'

if preffered_RH_version == 'master':
	server_version = 'master'
if preffered_RH_version == 'beta':
	server_version = '2.1.0-beta.3'
if preffered_RH_version == 'stable':
	server_version = '2.1.0'
if preffered_RH_version =='custom':
	server_version = 'X.X.X'           ### paste custom version number here if you want to declare it manually

class bcolors:
	HEADER = '\033[95m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def internetCheck():
	print("\nPlease wait - checking internet connection state...\n")
	global internet_FLAG
	os.system("timeout 3s sh /home/"+user+"/RH-ota/net_check.sh > /dev/null 2>&1")
	sleep(3.2)
	if os.path.exists("./index.html") == True:
		internet_FLAG=1
	else:
		internet_FLAG=0
	os.system("rm /home/"+user+"/RH-ota/index.html > /dev/null 2>&1")
	os.system("rm /home/"+user+"/RH-ota/wget-log* > /dev/null 2>&1")


def clearTheScreen():
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

def image():
	with open('image.txt', 'r') as file:
		f = file.read()
		print(f)

def first ():
	clearTheScreen()
	print("\n\n\n")
	image()
	sleep(0.5)
first()

def serverChecker():
	if os.path.exists("/home/"+user+"/RotorHazard/src/server/server.py") == True:
		os.system("grep 'RELEASE_VERSION =' ~/RotorHazard/src/server/server.py > ~/.ota_markers/.server_version")
		os.system("sed -i 's/RELEASE_VERSION = \"//' ~/.ota_markers/.server_version")
		os.system("sed -i 's/\" # Public release version code//' ~/.ota_markers/.server_version")
		f = open("/home/"+user+"/.ota_markers/.server_version","r")
		for line in f:
			global server_version_name
			server_version_name = line
	else:
		server_version_name = 'no installation found.'

def sysConf():
	os.system("sudo systemctl enable ssh")
	os.system("sudo systemctl start ssh ")
	os.system("echo 'dtparam=i2c_baudrate=75000' | sudo tee -a /boot/config.txt")
	os.system("echo 'core_freq=250' | sudo tee -a /boot/config.txt")
	os.system("echo 'dtparam=spi=on' | sudo sudo tee -a /boot/config.txt  ")  
	os.system("echo 'i2c-bcm2708' | sudo tee -a /boot/config.txt")
	os.system("echo 'i2c-dev' | sudo tee -a /boot/config.txt")
	os.system("echo 'dtparam=i2c1=on' | sudo tee -a /boot/config.txt")
	os.system("echo 'dtparam=i2c_arm=on' | sudo tee -a /boot/config.txt")
	os.system("sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf")
	os.system("sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf")

def end():
	print("\n\n\n\t\t"+bcolors.GREEN+"Type 'r' for reboot - recommended"+bcolors.ENDC+"\n")
	print("\t\tType 's' to start the server now\n")
	print("\t\t"+bcolors.YELLOW+"Type 'e' for exit\n"+bcolors.ENDC)
	def endMenu():
		selection=str(raw_input(""))
		if selection =='r':	
			os.system("sudo reboot")
		if selection =='e':	
			sys.exit()
		if selection =='s':	
			os.system("python ./server_start.py")
		else: 
			end()
	endMenu()	
	clearTheScreen()

def installation():
	internetCheck()
	if internet_FLAG==0:
		print("Looks like you don't have internet connection. Update canceled.")
	else:
		print("Internet connection - OK")
		clearTheScreen()
		sleep(0.1)
		print("\n\t\t "+bcolors.BOLD+"Installation process started - please wait..."+bcolors.ENDC+" \n")
		os.system("sudo apt-get update && sudo apt-get upgrade -y")
		os.system("sudo apt autoremove -y")
		os.system("sudo apt install wget ntp libjpeg-dev i2c-tools python-dev libffi-dev python-smbus build-essential python-pip git scons swig zip -y")
		if linux_testing == True:            ### on Linux PC system
			os.system("sudo apt dist-upgrade -y")
		else:                                ### on Raspberry
			os.system("sudo apt install python-rpi.gpio")
			if conf_allowed == True:
				sysConf()
		os.system("sudo -H pip install cffi pillow")
		os.chdir("/home/"+user)
		if os.path.exists("/home/"+user+"/.old_RotorHazard.old") == False:
			os.system("mkdir /home/"+user+"/.old_RotorHazard.old")
		if os.path.exists("/home/"+user+"/RotorHazard") == True:
			os.system("cp -r /home/"+user+"/RotorHazard /home/"+user+"/.old_RotorHazard.old/ >/dev/null 2>&1")   ### in case of forced installation
			os.system("rm -r /home/"+user+"/RotorHazard >/dev/null 2>&1")   ### in case of forced installation
		os.system("rm /home/"+user+"/temp >/dev/null 2>&1")     ### in case of forced installation
		os.system("cp -r /home/"+user+"/RotorHazard-* /home/"+user+"/.old_RotorHazard.old/ >/dev/null 2>&1")   ### in case of forced installation
		os.system("rm -r /home/"+user+"/RotorHazard-* >/dev/null 2>&1")   ### in case of forced installation
		os.chdir("/home/"+user)
		os.system("wget https://codeload.github.com/RotorHazard/RotorHazard/zip/"+server_version+" -O temp.zip")
		os.system("unzip temp.zip")
		os.system("rm temp.zip")
		os.system("mv /home/"+user+"/RotorHazard-"+server_version+" /home/"+user+"/RotorHazard")
		os.system("sudo -H pip install -r /home/"+user+"/RotorHazard/src/server/requirements.txt")
		os.system("sudo chmod 777 -R /home/"+user+"/RotorHazard/src/server")
		os.chdir("/home/"+user)
		os.system("sudo git clone https://github.com/jgarff/rpi_ws281x.git")
		os.chdir("/home/"+user+"/rpi_ws281x")
		os.system("sudo scons")
		os.chdir("/home/"+user+"/rpi_ws281x/python")
		os.system("sudo python setup.py install")
		os.chdir("/home/"+user)
		os.system("sudo git clone https://github.com/chrisb2/pi_ina219.git")
		os.chdir("/home/"+user+"/pi_ina219")
		os.system("sudo python setup.py install")
		os.chdir("/home/"+user)
		os.system("sudo git clone https://github.com/rm-hull/bme280.git")
		os.chdir("/home/"+user+"/bme280")
		os.system("sudo python setup.py install")
		os.system("echo 'leave this file here' | sudo tee -a /home/"+user+"/.ota_markers/.installation-check_file.txt")
		os.system("sudo apt-get install openjdk-8-jdk-headless -y")
		os.system("sudo rm /lib/systemd/system/rotorhazard.service")
		os.system("echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo '[Unit]' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo 'Description=RotorHazard Server' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo 'After=multi-user.target' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo '[Service]' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo 'WorkingDirectory=/home/"+user+"/RotorHazard/src/server' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo 'ExecStart=/usr/bin/python server.py' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo '[Install]' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo 'WantedBy=multi-user.target' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("sudo chmod 644 /lib/systemd/system/rotorhazard.service")
		os.system("sudo systemctl daemon-reload")
		os.system("sudo systemctl enable rotorhazard.service")
		print("""\n\n\t
		##############################################
		##                                          ##
		##         """+bcolors.BOLD+"""Installation completed!"""+bcolors.ENDC+"""          ##
		##                                          ##
		############################################## \n\n
		After rebooting please check by typing 'sudo raspi-config' \n
		if I2C, SPI and SSH protocols are active.\n""")
		end()

def update():
	internetCheck()
	if internet_FLAG==0:
		print("Looks like you don't have internet connection. Update canceled.")
	else:
		print("Internet connection - OK")
		clearTheScreen()
		if os.path.exists("/home/"+user+"/RotorHazard") == False:
			print("""\n\t """+bcolors.BOLD+"""Looks like you don't have RotorHazard server software installed for now. \n\t\t
		 If so please install your server software first or you won't be able to use the timer."""+bcolors.ENDC+""" """)
			selection=str(raw_input("""\n\n\t\t"""+bcolors.GREEN+""" 'i' - Install the software - recommended """+ bcolors.ENDC+
			"""\n\n\t\t 'u' - Force update procedure   \n\n\t\t """+bcolors.YELLOW+"""'a' - Abort both  \n\n """+bcolors.ENDC+""" """))
			if selection == 'i':
				conf_allowed = True
				installation()
			if selection == 'u':
				update()
			if selection == 'a':
				sleep(0.5)
				clearTheScreen()
				sys.exit()
			else:
				main()
		else :
			clearTheScreen()
			sleep(0.1)
			print("\n\t\t "+bcolors.BOLD+"Updating existing installation - please wait..."+bcolors.ENDC+" \n")
			os.system("sudo -H python -m pip install --upgrade pip ")
			os.system("sudo -H pip install pillow ")
			os.system("sudo apt-get install libjpeg-dev ntp -y")
			os.system("sudo apt-get update && sudo apt-get upgrade -y")
			if linux_testing == False:
				os.system("sudo apt dist-upgrade -y")
			os.system("sudo apt autoremove -y")
			if os.path.exists("/home/"+user+"/.old_RotorHazard.old") == False:
				os.system("sudo mkdir /home/"+user+"/.old_RotorHazard.old")
			os.system("sudo cp -r /home/"+user+"/RotorHazard-* /home/"+user+"/.old_RotorHazard.old/ >/dev/null 2>&1")   ### just in case of weird sys config
			os.system("sudo rm -r /home/"+user+"/RotorHazard-master >/dev/null 2>&1")   ### just in case of weird sys config
			os.system("sudo rm -r /home/"+user+"/temp.zip >/dev/null 2>&1")   ### just in case of weird sys config
			if os.path.exists("/home/"+user+"/RotorHazard.old") == True:
				os.system("sudo cp -r /home/"+user+"/RotorHazard.old /home/"+user+"/.old_RotorHazard.old/")
				os.system("sudo rm -r /home/"+user+"/RotorHazard.old")
			os.system("sudo mv /home/"+user+"/RotorHazard /home/"+user+"/RotorHazard.old")
			os.chdir("/home/"+user)
			os.system("wget https://codeload.github.com/RotorHazard/RotorHazard/zip/"+server_version+" -O temp.zip")
			os.system("unzip temp.zip")
			os.system("mv /home/"+user+"/RotorHazard-"+server_version+" /home/"+user+"/RotorHazard")
			os.system("sudo rm temp.zip")
			if os.path.exists("/home/"+user+"/backup_RH_data") == False:
				os.system("sudo mkdir /home/"+user+"/backup_RH_data")
			os.system("sudo chmod 777 -R /home/"+user+"/RotorHazard/src/server")
			os.system("sudo chmod 777 -R /home/"+user+"/RotorHazard.old")
			os.system("sudo chmod 777 -R /home/"+user+"/.old_RotorHazard.old")
			os.system("sudo chmod 777 -R /home/"+user+"/backup_RH_data")
			os.system("sudo chmod 777 -R /home/"+user+"/.ota_markers")
			os.system("cp /home/"+user+"/RotorHazard.old/src/server/config.json /home/"+user+"/RotorHazard/src/server/")
			os.system("cp -r /home/"+user+"/RotorHazard.old/src/server/static/image /home/"+user+"/backup_RH_data")
			os.system("cp -r /home/"+user+"/RotorHazard.old/src/server/static/image /home/"+user+"/RotorHazard/src/server/static")
			os.system("cp /home/"+user+"/RotorHazard.old/src/server/config.json /home/"+user+"/backup_RH_data")
			os.system("cp /home/"+user+"/RotorHazard.old/src/server/database.db /home/"+user+"/RotorHazard/src/server/")
			os.system("cp /home/"+user+"/RotorHazard.old/src/server/database.db /home/"+user+"/backup_RH_data")
			os.chdir("/home/"+user+"/RotorHazard/src/server")

			os.system("sudo -H pip install --upgrade --no-cache-dir -r requirements.txt")
			print("""\n\n\t
			##############################################
			##                                          ##
			##            """+bcolors.BOLD+"""Update completed!"""+bcolors.ENDC+"""             ##
			##                                          ##
			##############################################""")
			end()

def main():
	global conf_allowed
	global server_version_name
	clearTheScreen()
	serverChecker()
	sleep(0.2)
	print("""\n\n\t\t"""+bcolors.RED+bcolors.BOLD+"""AUTOMATIC UPDATE AND INSTALLATION OF ROTORHAZARD RACING TIMER SOFTWARE\n\n\t"""+bcolors.ENDC
	+bcolors.BOLD+"""This script will automatically install or update RotorHazard software on your Raspberry Pi. \n\t
	All additional software depedancies and libraries also will be installed or updated.\n\t
	Your current database, config file and custom bitmaps will stay on the updated software.\n\t
	Source of the software will be '"""+bcolors.BLUE+server_version+bcolors.ENDC+bcolors.BOLD+"""' version from the RotorHazard repository.\n\t 
	Remember to perform self-updating of this software, before updating server software.\n\t
	If you prefer to use newest possible beta version - change the source accordingly.\n\t
	Also make sure that you are logged as user '"""+bcolors.BLUE+user+bcolors.ENDC+bcolors.BOLD+"""'. \n\n\t
	You can change those by editing file 'updater-config.json' in text editor - like 'nano'.
	\n\tServer installed right now:"""+bcolors.GREEN+""" """+server_version_name+""""""+bcolors.RED+"""
	\n\t\t\t\t\t\t\t\t\tEnjoy!\n\n\t\t"""+bcolors.ENDC+"""
	\t 'i' - Install software from skratch\n\t\t
	\t 'u' - Update existing installation\n\t\t
	\t"""+bcolors.YELLOW+""" 'a' - Abort \n"""+bcolors.ENDC+""" """)
	selection=str(raw_input(""))
	if selection =='i':	
		if (os.path.exists("/home/"+user+"/.ota_markers/.installation-check_file.txt") == True) or (os.path.exists("/home/"+user+"/RotorHazard") == True):
			clearTheScreen()
			print("""\n\t """+bcolors.BOLD+"""Looks like you already have RotorHazard server software installed."""+bcolors.ENDC+""" \n
	 If so please use update mode instead. """)
			selection=str(raw_input("""\n\n\t\t"""+bcolors.GREEN+""" 'u' - Select update mode - recommended """+ bcolors.ENDC+
			"""\n\n\t\t 'i' - Force installation anyway\n\n\t\t 'c' - Force installation and sys. config.\n\n\t\t """+bcolors.YELLOW+"""'a' - Abort both  \n\n """+bcolors.ENDC+""" """))
			if selection == 'u':
				update()
			if selection == 'i':
				conf_allowed = False
				installation()
			if selection == 'c':
				conf_allowed = True
				installation()
			if selection == 'a':
				clearTheScreen()
				image()
				sleep(0.5)
				clearTheScreen()
				sys.exit()
			else:
				main()
		else :
			conf_allowed = True
			installation()
	if selection =='u':	
		update()
	if selection =='a':	
		clearTheScreen()
		image()
		sleep(0.5)
		clearTheScreen()
		sys.exit()
	else :
		main()
main()


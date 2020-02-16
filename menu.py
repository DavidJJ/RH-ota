####To do:####

# pins low/high as a function
# define number of pins
# flashed - only after success 


########enter pins connected to reset pins on Arduinos########
reset_1 = 12  # node 1
reset_2 = 13  # node 2
reset_3 = 16  # node 3
reset_4 = 26  # node 4


#import RPi.#GPIO as #GPIO # Import Raspberry Pi #GPIO library
from time import sleep # Import the sleep function from the time module
import os
import sys


#GPIO.setwarnings(False) # Ignore warning for now
#GPIO.setmode(#GPIO.BCM) # Use BCM pin numbering
#GPIO.setup(reset_1, #GPIO.OUT, initial=#GPIO.HIGH)
#GPIO.setup(reset_2, #GPIO.OUT, initial=#GPIO.HIGH)
#GPIO.setup(reset_3, #GPIO.OUT, initial=#GPIO.HIGH)
#GPIO.setup(reset_4, #GPIO.OUT, initial=#GPIO.HIGH)

os.system("cls")
os.system("clear")
sleep(0.1)
print("\n\n\n")	
print("		******************************************************************************************")
print("		***                                                                                    ***")
print("		***                                 RotorHazard                                        ***")
print("		***                                                                                    ***")
print("		***    You are about to update nodes firmware. Please do not interrupt this operation! ***")
print("		***                                                                                    ***")
print("		***                                                                                    ***")
print("		******************************************************************************************")




def mainMenu():
	print("\n\n\n What do you want to do now:\n\n")
	print("\t '1' - UPDATE NODES")
	print("\t '2' - EXIT")
	print("\t '3' - ENTER ADVANCED MENU")

	selection=str(raw_input("\n\n\n\t\t\tEnter choice: "))
	if selection =='1':
		update()
	if selection=='2':
		exit()
	if selection=='3':
		advanced()	
	else: 
		print("Enter 1 / 2 / 3")
		mainMenu()	
	

def update():
	print("\n\n\t Choose flashing type\n")
	print("\t '1' - every node gets own firmware")
	print("\t '2' - ground autoselect option")
	print("\t '3' - flashes 'blank' hex on every node")
	sleep(0.1)
	selection=str(raw_input(""))
	if selection=='1':
		programming_type = 1
	if selection=='2':
		programming_type = 2	
	if selection=='3':
		programming_type = 3
	os.system("#sudo pkill server.py")
	os.system("#sudo systemctl stop rotorhazard")
	sleep(0.1)

	#GPIO.output(reset_1, #GPIO.LOW)
	#GPIO.output(reset_2, #GPIO.LOW)
	#GPIO.output(reset_3, #GPIO.LOW)
	#GPIO.output(reset_4, #GPIO.LOW)
	sleep(0.1)
	#GPIO.output(reset_1, #GPIO.HIGH)
	#GPIO.output(reset_2, #GPIO.HIGH)
	#GPIO.output(reset_3, #GPIO.HIGH)
	#GPIO.output(reset_4, #GPIO.HIGH)

	sleep(0.1)
	os.system("#sudo sed -i 's/reset .*/reset = 12;/g' /root/.avrduderc")
	if programming_type ==1 : os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota_1.hex:i")
	if programming_type ==2 : os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
	if programming_type ==3 : os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
	sleep(0.3)

	print("")
	print("				Node 1 - flashed")
	print("\n\n")

	#GPIO.output(reset_1, #GPIO.LOW)
	#GPIO.output(reset_2, #GPIO.LOW)
	#GPIO.output(reset_3, #GPIO.LOW)
	#GPIO.output(reset_4, #GPIO.LOW)
	sleep(0.1)
	#GPIO.output(reset_1, #GPIO.HIGH)
	#GPIO.output(reset_2, #GPIO.HIGH)
	#GPIO.output(reset_3, #GPIO.HIGH)
	#GPIO.output(reset_4, #GPIO.HIGH)


	sleep(0.1)
	os.system("#sudo sed -i 's/reset .*/reset = 13;/g' /root/.avrduderc")
	if programming_type ==1 : os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota_2.hex:i")
	if programming_type ==2 : os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
	if programming_type ==3 : os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
	sleep(0.3)

	print("")
	print("				Node 2 - flashed")
	print("\n\n")

	#GPIO.output(reset_1, #GPIO.LOW)
	#GPIO.output(reset_2, #GPIO.LOW)
	#GPIO.output(reset_3, #GPIO.LOW)
	#GPIO.output(reset_4, #GPIO.LOW)
	sleep(0.1)
	#GPIO.output(reset_1, #GPIO.HIGH)
	#GPIO.output(reset_2, #GPIO.HIGH)
	#GPIO.output(reset_3, #GPIO.HIGH)
	#GPIO.output(reset_4, #GPIO.HIGH)
	sleep(0.1)
	os.system("#sudo sed -i 's/reset .*/reset = 16;/g' /root/.avrduderc")
	if programming_type ==1 : os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota_3.hex:i")
	if programming_type ==2 : os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
	if programming_type ==3 : os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
	sleep(0.3)

	print("")
	print("				Node 3 - flashed")
	print("\n\n")

	#GPIO.output(reset_1, #GPIO.LOW)
	#GPIO.output(reset_2, #GPIO.LOW)
	#GPIO.output(reset_3, #GPIO.LOW)
	#GPIO.output(reset_4, #GPIO.LOW)
	sleep(0.1)
	#GPIO.output(reset_1, #GPIO.HIGH)
	#GPIO.output(reset_2, #GPIO.HIGH)
	#GPIO.output(reset_3, #GPIO.HIGH)
	#GPIO.output(reset_4, #GPIO.HIGH)
	sleep(0.1)

	if programming_type ==1 : os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota_4.hex:i")
	if programming_type ==2 : os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
	if programming_type ==3 : os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
	os.system("#sudo sed -i 's/reset .*/reset = 12;/g' /root/.avrduderc")
	sleep(0.3)

	print("")
	print("				Node 4 - flashed")
	print("\n\n")
	sleep(0.1)
	print("		******************************************************************************************")
	print("		***                                                                                    ***")
	print("		***             CONGRATULATIONS!            Flashing firmware to nodes - 		DONE          ***")
	print("		***                                                                                    ***")
	print("		***                                                                                    ***")
	print("		***    Please power off the timer, unplug voltage source for few seconds and reboot    ***")
	print("		***                                                                                    ***")
	print("		******************************************************************************************")
	print("\n\n")
	sleep(1)
def exit():
	sleep(0.2)
	print("\n\nSee you!\n\n")
	sys.exit()
def advanced():
	sleep(0.1)
	def advancedMenu():
		print ("______________________________________________________________________________\n\n\n")
		print("\n			ADVANCED MENU:\n")
		print ("		'1' - Flash the bootloader")
		print ("		'2' - Fix GPIO pins state")
		print ("		'3' - Try to recover")
		print ("		'4' - Start the server")
		print ("		'5' - Avrdude info")
		print ("		'6' - Program specific node")
		print ("		'7' - Enter main menu")
		print("\n")
			
		selection=str(raw_input("			What would you like to do?\n\n\n"))
		if selection =='1':
			bootloader()
		if selection =='2':
			gpio_fix()
		if selection =='3':
			recover()		
		if selection =='4':
			server_start()
		if selection =='5':
			avr_info()
		if selection =='6':
			program_node()
		if selection =='7':
			sleep(0.2)	
			mainMenu()
		else:
			sleep(0.1) 
			advancedMenu()
	def bootloader(): 
		print("		Attempting to flash a bootloader to Arduinos") 
		os.system("#sudo sed -i 's/reset .*/reset = 12;/g' /root/.avrduderc")
		os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")
		os.system("#sudo sed -i 's/reset .*/reset = 13;/g' /root/.avrduderc")
		os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")
		os.system("#sudo sed -i 's/reset .*/reset = 16;/g' /root/.avrduderc")
		os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")
		os.system("#sudo sed -i 's/reset .*/reset = 26;/g' /root/.avrduderc")
		os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")
		print("\n\tBootloader flashed")
	def gpio_fix(): 
		os.system("echo 12 > /sys/class/#GPIO/unexport")
		os.system("echo 13 > /sys/class/#GPIO/unexport")
		os.system("echo 16 > /sys/class/#GPIO/unexport")
		os.system("echo 26 > /sys/class/#GPIO/unexport")
		os.system("echo 19 > /sys/class/#GPIO/unexport")
		os.system("echo 20 > /sys/class/#GPIO/unexport")
		os.system("echo 21 > /sys/class/#GPIO/unexport") 
		print("\n\n		DONE\n\n")		
	def recover():
		print("\n 		Attempting recovery\n\n")
		os.system("#sudo sed -i 's/reset .*/reset = 12;/g' /root/.avrduderc")
		os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:blank.hex:i")
		os.system("#sudo sed -i 's/reset .*/reset = 13;/g' /root/.avrduderc")
		os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:blank.hex:i")
		os.system("#sudo sed -i 's/reset .*/reset = 16;/g' /root/.avrduderc")
		os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:blank.hex:i")
		os.system("#sudo sed -i 's/reset .*/reset = 26;/g' /root/.avrduderc")
		os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:blank.hex:i")
	def server_start():
		print("\n\n   Server will start in 5 seconds\n\n")
		print("\n\n		Please wait...\n\n")
		print("\n")
		sleep(3)
		os.system("#sudo pkill server.py")
		os.system("#sudo systemctl stop rotorhazard")
		os.system("python ~/RotorHazard/src/server/server.py")	
	def avr_info():
		os.system("sudo avrdude -c linuxgpio -p m328p -v")	
	def program_node():
		def nodeMenu():
			print("\n\t\t NODE MENU")
			print("\n\t 1 - Flash node 1")
			print("\n\t 2 - Flash node 2")
			print("\n\t 3 - Flash node 3")
			print("\n\t 4 - Flash node 4")
			print("\n\t 5 - Abort")
			print("\n\t 6 - Exit program")
			selection=str(raw_input("\n\nWhich node do you want to program: "))
			if selection =='1':
				os.system("#sudo sed -i 's/reset .*/reset = 12;/g' /root/.avrduderc")
				print("\n\t Node 1 selected")
				print("\n\n\t Choose flashing type\n")
				print("\t '1' - node gets own firmware")
				print("\t '2' - ground autoselect option")
				print("\t '3' - flashes 'blank' hex on the node")
				print("\t '4' - flashes bootloader on the node")
				selection2=str(raw_input(""))
				if selection2 =='1' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota_1.hex:i")
				if selection2 =='2' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection2 =='3' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
				if selection2 =='4' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")	
				print("\n\t Node flashed")
			if selection=='2':
				os.system("#sudo sed -i 's/reset .*/reset = 13;/g' /root/.avrduderc")
				print("\n\t Node 2 selected")
				print("\n\n\t Choose flashing type\n")
				print("\t '1' - node gets own firmware")
				print("\t '2' - ground autoselect option")
				print("\t '3' - flashes 'blank' hex on the node")
				print("\t '4' - flashes bootloader on the node")
				selection2=str(raw_input(""))
				if selection2 =='1' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota_2.hex:i")
				if selection2 =='2' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection2 =='3' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
				if selection2 =='4' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")	
				print("\n\t Node flashed")
			if selection=='3':
				os.system("#sudo sed -i 's/reset .*/reset = 16;/g' /root/.avrduderc")
				print("\n\t Node 3 selected")
				print("\n\n\t Choose flashing type\n")
				print("\t '1' - node gets own firmware")
				print("\t '2' - ground autoselect option")
				print("\t '3' - flashes 'blank' hex on the node")
				print("\t '4' - flashes bootloader on the node")
				selection2=str(raw_input(""))
				if selection2 =='1' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota_3.hex:i")
				if selection2 =='2' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection2 =='3' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
				if selection2 =='4' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")	
				print("\n\t Node flashed")
			if selection=='4':
				os.system("#sudo sed -i 's/reset .*/reset = 26;/g' /root/.avrduderc")
				print("\n\t Node 4 selected")	
				print("\n\n\t Choose flashing type\n")
				print("\t '1' - node gets own firmware")
				print("\t '2' - ground autoselect option")
				print("\t '3' - flashes 'blank' hex on the node")
				print("\t '4' - flashes bootloader on the node")
				selection2=str(raw_input(""))
				if selection2 =='1' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota_4.hex:i")
				if selection2 =='2' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection2 =='3' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
				if selection2 =='4' : 
					os.system("#sudo avrdude -c linux#GPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")	
				print("\n\t Node flashed")
			if selection=='5':
				sleep(0.2)	
				advancedMenu()
			if selection=='6':
				sleep(0.2)
				print("\n\nSee you!\n\n")
				sys.exit()	
			else: 
				nodeMenu()	
		nodeMenu()			
	advancedMenu()
mainMenu()
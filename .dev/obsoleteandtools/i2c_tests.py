from smbus import SMBus  # works only on Pi
from time import sleep
import os
import sys
import json

if os.path.exists("/home/pi/RH-ota/updater-config.json"):
    with open('/home/pi/RH-ota/updater-config.json') as config_file:
        data = json.load(config_file)
else:
    with open('/home/pi/RH-ota/updater-config.json') as config_file:
        data = json.load(config_file)

if data['debug_mode']:
    linux_testing = True
else:
    linux_testing = False

if linux_testing:
    user = data['debug_user']
else:
    user = data['pi_user']
preferred_RH_version = data['RH_version']

if preferred_RH_version == 'master':
    firmware_version = 'master'
if preferred_RH_version == 'beta':
    firmware_version = 'beta'
if preferred_RH_version == 'stable':
    firmware_version = 'stable'
if preferred_RH_version == 'custom':
    firmware_version = 'stable'

bus = SMBus(1)  # indicates /dev/ic2-1

node1addr = 0x08  # 8
node2addr = 0x0a  # 10
node3addr = 0x0c  # 12
node4addr = 0x0e  # 14
node5addr = 0x12  # 16
node6addr = 0x14  # 18
node7addr = 0x14  # 20
node8addr = 0x16  # 22

reset_1 = 12

if not linux_testing:
    import RPi.GPIO as GPIO

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    GPIO.setup(reset_1, GPIO.OUT, initial=GPIO.HIGH)


    def all_pins_low():
        GPIO.output(reset_1, GPIO.LOW)
        # GPIO.output(reset_2, GPIO.LOW)
        # GPIO.output(reset_3,   GPIO.LOW)
        # GPIO.output(reset_4, GPIO.LOW)
        # GPIO.output(reset_5, GPIO.LOW)
        # GPIO.output(reset_6, GPIO.LOW)
        # GPIO.output(reset_7, GPIO.LOW)
        # GPIO.output(reset_8, GPIO.LOW)
        sleep(0.05)


    def all_pins_high():
        GPIO.output(reset_1, GPIO.HIGH)
        # GPIO.output(reset_2, GPIO.HIGH)
        # GPIO.output(reset_3, GPIO.HIGH)
        # GPIO.output(reset_4, GPIO.HIGH)
        # GPIO.output(reset_5, GPIO.HIGH)
        # GPIO.output(reset_6, GPIO.HIGH)
        # GPIO.output(reset_7, GPIO.HIGH)
        # GPIO.output(reset_8, GPIO.HIGH)
        sleep(0.05)


    def all_pins_reset():
        GPIO.output(reset_1, GPIO.LOW)
        # GPIO.output(reset_2, GPIO.LOW)
        # GPIO.output(reset_3, GPIO.LOW)
        # GPIO.output(reset_4, GPIO.LOW)
        # GPIO.output(reset_5, GPIO.LOW)
        # GPIO.output(reset_6, GPIO.LOW)
        # GPIO.output(reset_7, GPIO.LOW)
        # GPIO.output(reset_8, GPIO.LOW)
        sleep(0.1)
        GPIO.output(reset_1, GPIO.HIGH)
        # GPIO.output(reset_2, GPIO.HIGH)
        # GPIO.output(reset_3, GPIO.HIGH)
        # GPIO.output(reset_4, GPIO.HIGH)
        # GPIO.output(reset_5, GPIO.HIGH)
        # GPIO.output(reset_6, GPIO.HIGH)
        # GPIO.output(reset_7, GPIO.HIGH)
        # GPIO.output(reset_8, GPIO.HIGH)


    def node_one_reset():
        all_pins_high()
        GPIO.output(reset_1, GPIO.LOW)
        sleep(0.1)
        GPIO.output(reset_1, GPIO.HIGH)


    def node_two_reset():
        bus.write_byte(node1addr, 0x8)
        # sleep(0.1)
        # bus.write_byte(node1addr, 0x1)


    def node_three_reset():
        bus.write_byte(node2addr, 0x0)
        sleep(0.1)
        bus.write_byte(node2addr, 0x1)


    def node_four_reset():
        bus.write_byte(node3addr, 0x0)
        sleep(0.1)
        bus.write_byte(node3addr, 0x1)


    def node_five_reset():
        bus.write_byte(node4addr, 0x0)
        sleep(0.1)
        bus.write_byte(node4addr, 0x1)


    def node_six_reset():
        bus.write_byte(node5addr, 0x0)
        sleep(0.1)
        bus.write_byte(node5addr, 0x1)


    def node_seven_reset():
        bus.write_byte(node6addr, 0x0)
        sleep(0.1)
        bus.write_byte(node6addr, 0x1)


    def node_eight_reset():
        bus.write_byte(node7addr, 0x0)
        sleep(0.1)
        bus.write_byte(node7addr, 0x1)


def test():
    selection = input("What do you want to send? press '0'")
    if selection == '0':
        bus.write_byte(node1addr, 0x79)  # switch it off
        os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U /"
                  "flash:w:/home/pi/RH-ota/firmware/i2c/reset_no_s.hex:i")
        bus.write_byte(node2addr, 0x79)  # switch it off
        os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U /"
                  "flash:w:/home/pi/RH-ota/firmware/i2c/reset_no_s.hex:i")
        bus.write_byte(node1addr, 0x0)  # switch it off
        bus.write_byte(node1addr, 0x0)  # switch it off
        bus.write_byte(node1addr, 0x0)  # switch it off
        bus.write_byte(node1addr, 0x0)  # switch it off
        bus.write_byte(node1addr, 0x0)  # switch it off
        bus.write_byte(node1addr, 0x0)  # switch it off
        bus.write_byte(node1addr, 0x0)  # switch it off
        bus.write_byte(node1addr, 0x0)  # switch it off
        test()
    if selection == '1':
        bus.write_byte(node1addr, 0x1)  # switch it on
        bus.write_byte(node1addr, 0x1)  # switch it on
        bus.write_byte(node1addr, 0x1)  # switch it on
        bus.write_byte(node1addr, 0x1)  # switch it on
        bus.write_byte(node1addr, 0x1)  # switch it on
        bus.write_byte(node1addr, 0x1)  # switch it on
        bus.write_byte(node1addr, 0x1)  # switch it on
        bus.write_byte(node1addr, 0x1)  # switch it on
        bus.write_byte(node1addr, 0x1)  # switch it on
        bus.write_byte(node1addr, 0x1)  # switch it on
        bus.write_byte(node1addr, 0x1)  # switch it on
        test()
    if selection == '2':
        node_two_reset()
        os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"
                  + user + "/RH-ota/comm.hex:i ")
        print("\n\t Node flashed using I2C resetting - blink\n")
        sleep(1.5)
        test()
    if selection == '3':
        sys.exit()


test()

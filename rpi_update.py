import json
import os
import sys
from conf_wizard_ota import conf_ota
from time import sleep
from modules import clear_the_screen, Bcolors, image_show, internet_check
import emoji

if os.path.exists("./updater-config.json"):
    with open('updater-config.json') as config_file:
        data = json.load(config_file)
else:
    with open('distr-updater-config.json') as config_file:
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

if data['pi_4_cfg']:
    pi_4_FLAG = True
else:
    pi_4_FLAG = False

if preferred_RH_version == 'master':
    server_version = 'master'
if preferred_RH_version == 'beta':
    server_version = '2.1.0-beta.3'
if preferred_RH_version == 'stable':
    server_version = '2.1.0'
if preferred_RH_version == 'custom':
    server_version = 'X.X.X'  # paste custom version number here if you want to declare it manually


def server_version_checker():
    if os.path.exists(f"/home/{user}/RotorHazard/src/server/server.py"):
        os.system("grep 'RELEASE_VERSION =' ~/RotorHazard/src/server/server.py > ~/.ota_markers/.server_version")
        os.system("sed -i 's/RELEASE_VERSION = \"//' ~/.ota_markers/.server_version")
        os.system("sed -i 's/\" # Public release version code//' ~/.ota_markers/.server_version")
        f = open(f"/home/{user}/.ota_markers/.server_version", "r")
        for line in f:
            server_version_name = f"{Bcolors.GREEN}{line}{Bcolors.ENDC}"
        server_installed_flag = True
    else:
        server_version_name = f"{Bcolors.YELLOW}no installation found\n{Bcolors.ENDC}"
        server_installed_flag = False
    return server_installed_flag, server_version_name


def config_checker():
    if os.path.exists(f"/home/{user}/RotorHazard/src/server/config.json"):
        config_soft = f"{Bcolors.GREEN}configured {emoji.emojize(':thumbs_up:')}{Bcolors.ENDC}"
        config_flag = True
    else:
        config_soft = f"{Bcolors.YELLOW}{Bcolors.UNDERLINE}not configured{Bcolors.ENDC} " \
                      f"{emoji.emojize(':thumbs_down:')}"
        config_flag = False
    return config_flag, config_soft


def end_update(conf_flag, serv_installed_flag):
    print("\n\n")
    if not conf_flag and serv_installed_flag:
        print(f"{Bcolors.GREEN}\t\t'c' - configure the server now{Bcolors.ENDC}")
    else:
        print("""\t\t'c' - Reconfigure RotorHazard server""")
    print(f"""
                'r' - reboot - recommended when configured\n
                's' - start the server now\n{Bcolors.YELLOW}
                'e' - exit now\n{Bcolors.ENDC}""")

    def end_menu():
        selection = input()
        if selection == 'r':
            os.system("sudo reboot")
        if selection == 'e':
            json_dump()  # todo only to soft
            sys.exit()
        if selection == 'c':
            conf_ota()
            end_update()
        if selection == 's':
            clear_the_screen()
            os.chdir(f"/home/{user}/RH-ota")
            os.system(". ./open_scripts.sh; server_start")
        else:
            end_menu()

    end_menu()
    clear_the_screen()


def end_installation():
    print(f"""\n\n{Bcolors.GREEN}
        'c' - configure the server now - recommended\n
        'r' - reboot - recommended after configuring{Bcolors.ENDC}\n
        's' - start the server now\n{Bcolors.YELLOW}
        'e' - exit now\n{Bcolors.ENDC}""")

    def end_menu():
        selection = input()
        if selection == 'r':
            os.system("sudo reboot")
        if selection == 'e':
            json.dump(soft)  # todo change to soft config
            sys.exit()
        if selection == 'c':
            conf_ota()
            end_update()
        if selection == 's':
            clear_the_screen()
            os.chdir(f"/home/{user}/RH-ota")
            os.system(". ./open_scripts.sh; server_start")
        else:
            end_menu()

    end_menu()
    clear_the_screen()


def installation(conf_allowed):
    if not linux_testing:
        os.system("sudo systemctl stop rotorhazard >/dev/null 2>&1 &")
    internet_flag = internet_check()
    if not internet_flag:
        print("\nLooks like you don't have internet connection. Installation canceled.")
        sleep(2)
    else:
        print("\nInternet connection - OK")
        sleep(2)
        clear_the_screen()
        print(f"\n\t{Bcolors.BOLD}Installation process has been started - please wait...{Bcolors.ENDC}\n")
        installation_completed = """\n\n
            #####################################################
            ##                                                 ##
            ##{bold}{green}Installation completed{thumbs}{endc}##
            ##                                                 ##
            #####################################################


        After rebooting please check by typing 'sudo raspi-config' 
        if I2C, SPI and SSH protocols are active.
                    """.format(thumbs=3 * emoji.emojize(':thumbs_up:') + str(2 * " "), bold=Bcolors.BOLD_S,
                               endc=Bcolors.ENDC_S, green=Bcolors.GREEN_S)
        try:
            os.system(f"./scripts/install_rh.sh {user} {server_version}")
            if conf_allowed:
                os.system("sh. ./scripts/sys_conf.sh")
                config_soft['installation_done'] = 1
                if pi_4_FLAG:
                    os.system("sed -i 's/core_freq=250/#core_freq=250/' /boot/config.txt > /dev/null 2>&1")
            config_soft['installation_performed'] = true  # todo change to this json something
            json.dump()  # sys_config_etc
            print(installation_completed)
        except:  # todo add something
            print("Error occurred. Installation aborted.")
        # os.system("sudo apt-get update && sudo apt-get upgrade -y")  # todo David - ok? delete if yes
        # os.system("sudo apt autoremove -y")
        # os.system("sudo apt install wget ntp libjpeg-dev i2c-tools python-dev libffi-dev python-smbus \
        # build-essential python-pip git scons swig zip -y")
        # if linux_testing:  # on Linux PC system
        #     os.system("sudo apt dist-upgrade -y")
        # else:  # on Raspberry
        #     os.system("sudo apt install python-rpi.gpio")
        #     if conf_allowed:
        #         sys_conf()
        # os.system("sudo -H pip install cffi pillow")
        # os.chdir("/home/" + user)
        # if not os.path.exists(f"/home/{user}/.old_RotorHazard.old"):
        #     os.system(f"mkdir /home/{user}/.old_RotorHazard.old")
        # if os.path.exists(f"/home/{user}/RotorHazard"):
        #     os.system(f"cp -r /home/{user}/RotorHazard /home/{user}/.old_RotorHazard.old/ >/dev/null 2>&1")
        #     #  in case of forced installation
        #     os.system(f"rm -r /home/{user}/RotorHazard >/dev/null 2>&1")  # in case of forced installation
        # os.system(f"rm /home/{user}/temp >/dev/null 2>&1")  # in case of forced installation
        # os.system(f"cp -r /home/{user}/RotorHazard-* /home/{user}/.old_RotorHazard.old/ >/dev/null 2>&1")
        # # in case of forced installation
        # os.system(f"rm -r /home/{user}/RotorHazard-* >/dev/null 2>&1")  # in case of forced installation
        # os.chdir(f"/home/{user}")
        # os.system(f"wget https://codeload.github.com/RotorHazard/RotorHazard/zip/{server_version} -O temp.zip")
        # os.system("unzip temp.zip")
        # os.system("rm temp.zip")
        # os.system(f"mv /home/{user}/RotorHazard-{server_version} /home/{user}/RotorHazard")
        # os.system(f"sudo -H pip install -r /home/{user}/RotorHazard/src/server/requirements.txt")
        # os.system(f"sudo chmod 777 -R /home/{user}/RotorHazard/src/server")
        # os.chdir(f"/home/{user}")
        # os.system("sudo git clone https://github.com/jgarff/rpi_ws281x.git")
        # os.chdir(f"/home/{user}/rpi_ws281x")
        # os.system("sudo scons")
        # os.chdir(f"/home/{user}/rpi_ws281x/python")
        # os.system("sudo python setup.py install")
        # os.chdir(f"/home/{user}")
        # os.system("sudo git clone https://github.com/chrisb2/pi_ina219.git")
        # os.chdir(f"/home/{user}/pi_ina219")
        # os.system("sudo python setup.py install")
        # os.chdir(f"/home/{user}")
        # os.system("sudo git clone https://github.com/rm-hull/bme280.git")
        # os.chdir(f"/home/{user}/bme280")
        # os.system("sudo python setup.py install")
        # config_soft['installation_done'] = 1
        # json.dump()  # soft config
        # os.system("sudo apt-get install openjdk-8-jdk-headless -y")
        # os.system("sudo rm /lib/systemd/system/rotorhazard.service")
        # os.system("echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service")
        # os.system("echo '[Unit]' | sudo tee -a /lib/systemd/system/rotorhazard.service")
        # os.system("echo 'Description=RotorHazard Server' | sudo tee -a /lib/systemd/system/rotorhazard.service")
        # os.system("echo 'After=multi-user.target' | sudo tee -a /lib/systemd/system/rotorhazard.service")
        # os.system("echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service")
        # os.system("echo '[Service]' | sudo tee -a /lib/systemd/system/rotorhazard.service")
        # os.system(f"echo 'WorkingDirectory=/home/{user}/RotorHazard/src/server' \
        # | sudo tee -a /lib/systemd/system/rotorhazard.service")
        # os.system("echo 'ExecStart=/usr/bin/python server.py' | sudo tee -a /lib/systemd/system/rotorhazard.service")
        # os.system("echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service")
        # os.system("echo '[Install]' | sudo tee -a /lib/systemd/system/rotorhazard.service")
        # os.system("echo 'WantedBy=multi-user.target' | sudo tee -a /lib/systemd/system/rotorhazard.service")
        # os.system("sudo chmod 644 /lib/systemd/system/rotorhazard.service")
        # os.system("sudo systemctl daemon-reload")
        # os.system("sudo systemctl enable rotorhazard.service")
        end_installation()


def update():
    if not linux_testing:
        os.system("sudo systemctl stop rotorhazard >/dev/null 2>&1 &")
    internet_flag = internet_check()
    if not internet_flag:
        print("\nLooks like you don't have internet connection. Update canceled.")
        sleep(2)
    else:
        print("\nInternet connection - OK")
        sleep(2)
        clear_the_screen()
        if not os.path.exists(f"/home/{user}/RotorHazard"):
            print(f"""{Bcolors.BOLD}
    Looks like you don't have RotorHazard server software installed for now. \n\t\t
    If so please install your server software first or you won't be able to use the timer.{Bcolors.ENDC}""")
            print(f"""\n\n{Bcolors.GREEN} 
        'i' - Install the software - recommended{Bcolors.ENDC}\n 
        'u' - Force update procedure\n{Bcolors.YELLOW}
        'a' - Abort both  \n\n{Bcolors.ENDC}""")
            selection = input()
            if selection == 'i':
                conf_allowed = True
                installation()
            if selection == 'u':
                update()
            if selection == 'a':
                clear_the_screen()
                sys.exit()
            else:
                main()
        else:
            clear_the_screen()
            print(f"\n\t{Bcolors.BOLD}Updating existing installation - please wait...{Bcolors.ENDC} \n")
            update_completed = """\n\n\t
                ################################################
                ##                                            ##
                ##{bold}{green}Update completed!{thumbs}{endc}##
                ##                                            ##
                ################################################
                        """.format(thumbs=3 * emoji.emojize(':thumbs_up:') + str(2 * " "), bold=Bcolors.BOLD_S,
                                   endc=Bcolors.ENDC_S, green=Bcolors.GREEN_S)
            os.system(f"./scripts/update_rh.sh {user} {server_version}")
            # os.system("sudo -H python -m pip install --upgrade pip")  # todo David - ok? delete if yes
            # os.system("sudo -H pip install pillow ")
            # os.system("sudo apt-get install libjpeg-dev ntp -y")
            # os.system("sudo apt-get update && sudo apt-get upgrade -y")
            # if not linux_testing:
            #     os.system("sudo apt dist-upgrade -y")
            # os.system("sudo apt autoremove -y")
            # if not os.path.exists(f"/home/{user}/.old_RotorHazard.old"):
            #     os.system(f"sudo mkdir /home/{user}/.old_RotorHazard.old")
            # os.system(f"sudo cp -r /home/{user}/RotorHazard-* /home/{user}/.old_RotorHazard.old/ >/dev/null 2>&1")
            # os.system(f"sudo rm -r /home/{user}/RotorHazard-master >/dev/null 2>&1")  # just in case of weird sys cfg
            # os.system(f"sudo rm -r /home/{user}/temp.zip >/dev/null 2>&1")  # just in case of weird sys config
            # if os.path.exists(f"/home/{user}/RotorHazard.old"):
            #     os.system(f"sudo cp -r /home/{user}/RotorHazard.old /home/{user}/.old_RotorHazard.old/")
            #     os.system(f"sudo rm -r /home/{user}/RotorHazard.old")
            # os.system(f"sudo mv /home/{user}/RotorHazard /home/{user}/RotorHazard.old")
            # os.chdir(f"/home/{user}")
            # os.system(f"wget https://codeload.github.com/RotorHazard/RotorHazard/zip/{server_version} -O temp.zip")
            # os.system("unzip temp.zip")
            # os.system(f"mv /home/{user}/RotorHazard-{server_version} /home/{user}/RotorHazard")
            # os.system("sudo rm temp.zip")
            # os.system(f"sudo mkdir /home/{user}/backup_RH_data >/dev/null 2>&1")
            # os.system(f"sudo chmod 777 -R /home/{user}/RotorHazard/src/server")
            # os.system(f"sudo chmod 777 -R /home/{user}/RotorHazard.old")
            # os.system(f"sudo chmod 777 -R /home/{user}/.old_RotorHazard.old")
            # os.system(f"sudo chmod 777 -R /home/{user}/backup_RH_data")
            # os.system(f"sudo chmod 777 -R /home/{user}/.ota_markers")
            # os.system(f"cp /home/{user}/RotorHazard.old/src/server/config.json \
            # /home/{user}/RotorHazard/src/server/ >/dev/null 2>&1 &")
            # os.system(f"cp -r /home/{user}/RotorHazard.old/src/server/static/image \
            # /home/{user}/backup_RH_data")
            # os.system(f"cp -r /home/{user}/RotorHazard.old/src/server/static/image \
            # /home/{user}/RotorHazard/src/server/static")
            # os.system(f"cp /home/{user}/RotorHazard.old/src/server/config.json \
            # /home/{user}/backup_RH_data >/dev/null 2>&1 &")
            # os.system(f"cp /home/{user}/RotorHazard.old/src/server/database.db \
            # /home/{user}/RotorHazard/src/server/ >/dev/null 2>&1 &")
            # os.system(f"cp /home/{user}/RotorHazard.old/src/server/database.db \
            # /home/{user}/backup_RH_data >/dev/null 2>&1 &")
            # os.chdir(f"/home/{user}/RotorHazard/src/server")
            # os.system("sudo pip install --upgrade --no-cache-dir -r requirements.txt")
            print(update_completed)
            end_update(config_checker()[0], server_version_checker()[0])


def main_window(serv_installed_flag, server_version_name, conf_flag):
    sleep(0.1)
    welcome_text = """
        \n\n{red} {bold}
        AUTOMATIC UPDATE AND INSTALLATION OF ROTORHAZARD RACING TIMER SOFTWARE
            {endc}{bold}
        You can automatically install and update RotorHazard timing software. 
        Additional dependencies and libraries also will be installed or updated.
        Current database, configs and custom bitmaps will stay on their place.
        Source of the software is set to {underline}{blue}{server_version}{endc}{bold} version from the official 
        RotorHazard repository.
         
        Perform self-updating of this software, before updating server software.
        Also make sure that you are logged as user {underline}{blue}{user}{endc}{bold}.
        
        You can change those in configuration wizard in Main Menu.
        
        Server installed right now: {server} {bold}
        RotorHazard configuration state: {config_soft}\n\n
        """.format(bold=Bcolors.BOLD, underline=Bcolors.UNDERLINE, endc=Bcolors.ENDC, blue=Bcolors.BLUE,
                   yellow=Bcolors.YELLOW, red=Bcolors.RED, orange=Bcolors.ORANGE, server_version=server_version,
                   user=user, config_soft=conf_flag, server=server_version_name)
    print(welcome_text)
    if not conf_flag and serv_installed_flag:
        print(f"{Bcolors.GREEN}\t\t'c' - Configure RotorHazard server\n{Bcolors.ENDC}")
    else:
        print("\t\t'c' - Reconfigure RotorHazard server\n")
    if not serv_installed_flag:
        print(f"\t\t{Bcolors.GREEN}'i' - Install software from scratch{Bcolors.ENDC}")
    else:
        print("""\t\t'i' - Install software from scratch""")
    print("""
                'u' - Update existing installation\n {yellow}    
                'e' - Exit to Main Menu{endc}\n
            """.format(yellow=Bcolors.YELLOW, endc=Bcolors.ENDC))
    selection = input()
    if selection == 'c':
        if serv_installed_flag:
            conf_ota()
        else:
            print("\n\t\tPlease install server software first")
            sleep(1.5)
    if selection == 'i':
        if config[installation_done]:
            clear_the_screen()
            already_installed_prompt = """
            {bold}
    Looks like you already have RotorHazard server installed
    (or at least that your system was once configured).{endc}
    
    If that's the case please use {underline} update mode {endc} - 'u'
    or force installation {underline} without {endc} sys. config. - 'i'.
            
            {green} 
        'u' - Select update mode - recommended {endc}\n 
        'i' - Force installation without sys. config.\n
        'c' - Force installation and sys. config.\n {yellow}
        'a' - Abort both  \n {endc}""".format(bold=Bcolors.BOLD, endc=Bcolors.ENDC, underline=Bcolors.UNDERLINE,
                                              yellow=Bcolors.YELLOW, green=Bcolors.GREEN)
            print(already_installed_prompt)
            selection = input()
            if selection == 'u':
                update()
            if selection == 'i':
                conf_allowed = False
                installation()
            if selection == 'c':
                confirm_valid_options = ['y', 'yes', 'n', 'no', 'abort', 'a']
                while True:
                    confirm = input("\n\t\tAre you sure? [yes/abort]\t").strip()
                    if confirm in confirm_valid_options:
                        break
                    else:
                        print("\ntoo big fingers :( wrong command. try again! :)")
                if confirm == 'y' or confirm == 'yes':
                    conf_allowed = True
                    installation()
                if confirm in ['n', 'no', 'abort', 'a']:
                    pass
            if selection == 'a':
                clear_the_screen()
                image_show()
                sleep(0.5)
                sys.exit()
            else:
                main()
        else:
            conf_allowed = True
            installation()
    if selection == 'u':
        update()
    if selection == 'e':
        clear_the_screen()
        os.chdir(f"/home/{user}/RH-ota")
        image_show()
        sleep(0.3)
        sys.exit()
    else:
        main()


def rpi_update():
    config_checker()
    server_version_checker()
    main_window(server_version_checker()[0], server_version_checker()[1], config_checker()[1])


def main():
    rpi_update()


if __name__ == "__main__":
    main()

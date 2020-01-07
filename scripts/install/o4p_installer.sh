#!/bin/bash
# Colors: \e[36m=Cyan M ; \e[92m=Light green ; \e[91m=Light red ; \e[93m=Light yellow ; \e[31m=green ; \e[0m=Default ; \e[33m=Yellow ; \e[31m=Red

#Version: 1.9.1 - 20200105
#branch="development"
repo="https://github.com/splitti/oled_phoniebox"
branch="master"

nocolor='\e[0m'
red="\e[1;91m"
cyan="\e[1;36m"
yellow="\e[1;93m"
green="\e[1;92m"
installPath="/home/pi/oled_phoniebox"

clear
echo -e "////////////////////////////////////////////////////////////////////////////////////////////////////////////////"
echo -e "///${cyan}                                                                                                          ${nocolor}///";
echo -e "///${cyan}        ██████╗ ██╗     ███████╗██████╗     ██████╗ ██╗███████╗██████╗ ██╗      █████╗ ██╗   ██╗          ${nocolor}///";
echo -e "///${cyan}       ██╔═══██╗██║     ██╔════╝██╔══██╗    ██╔══██╗██║██╔════╝██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝          ${nocolor}///";
echo -e "///${cyan}       ██║   ██║██║     █████╗  ██║  ██║    ██║  ██║██║███████╗██████╔╝██║     ███████║ ╚████╔╝           ${nocolor}///";
echo -e "///${cyan}       ██║   ██║██║     ██╔══╝  ██║  ██║    ██║  ██║██║╚════██║██╔═══╝ ██║     ██╔══██║  ╚██╔╝            ${nocolor}///";
echo -e "///${cyan}       ╚██████╔╝███████╗███████╗██████╔╝    ██████╔╝██║███████║██║     ███████╗██║  ██║   ██║             ${nocolor}///";
echo -e "///${cyan}        ╚═════╝ ╚══════╝╚══════╝╚═════╝     ╚═════╝ ╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝             ${nocolor}///";
echo -e "///${cyan}                                                                                                          ${nocolor}///";
echo -e "///${cyan}   ███████╗ ██████╗ ██████╗     ██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗██╗███████╗██████╗  ██████╗ ██╗  ██╗   ${nocolor}///";
echo -e "///${cyan}   ██╔════╝██╔═══██╗██╔══██╗    ██╔══██╗██║  ██║██╔═══██╗████╗  ██║██║██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝   ${nocolor}///";
echo -e "///${cyan}   █████╗  ██║   ██║██████╔╝    ██████╔╝███████║██║   ██║██╔██╗ ██║██║█████╗  ██████╔╝██║   ██║ ╚███╔╝    ${nocolor}///";
echo -e "///${cyan}   ██╔══╝  ██║   ██║██╔══██╗    ██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██║██╔══╝  ██╔══██╗██║   ██║ ██╔██╗    ${nocolor}///";
echo -e "///${cyan}   ██║     ╚██████╔╝██║  ██║    ██║     ██║  ██║╚██████╔╝██║ ╚████║██║███████╗██████╔╝╚██████╔╝██╔╝ ██╗   ${nocolor}///";
echo -e "///${cyan}   ╚═╝      ╚═════╝ ╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ${nocolor}///";
echo -e "///${cyan}                                                                                                          ${nocolor}///";
echo -e "////////////////////////////////////////////////////////////////////////////////////////////////////////////////"
echo -e "///                                                                                                          ///"
echo -e "///${cyan}                               https://github.com/splitti/oled_phoniebox                                  ${nocolor}///"
echo -e "///                                                                                                          ///"
echo -e "////////////////////////////////////////////////////////////////////////////////////////////////////////////////"
echo -e ""
echo -e "${red}Please notice:${nocolor} This script will install all needed components for the OLED-Display (Format 128 X 64px) with"
echo -e "SH1106- or SSD1306-Controller. A preinstallation of the jukebox4kids or similiar (MPC) will be needed."
echo -e " "
if [ -d "/home/pi/RPi-Jukebox-RFID" ]; then
	echo -e "${green}RPi-Jukebox-RFID seems to be installed${nocolor}"
	echo -e " "
else
	echo -e "${red}RPi-Jukebox-RFID is missing! Please install necessarily.${nocolor}"
	echo -e " "
fi

echo -e "Do you want to install this OLED-Display-Service?"
echo -e " "
options=("Install" "Quit")

select opt in "${options[@]}"
do
    case $opt in
        "Install")
            break
            ;;

        "Quit")
            exit
            ;;
        *) echo -e "invalid option $REPLY";;
    esac
done

clear
echo -e "////////////////////////////////////////////////////////////////////"
echo -e "///${cyan}   Please choose your display controller type:                ${nocolor}///"
echo -e "////////////////////////////////////////////////////////////////////"
echo -e ""
echo -e "Which type of OLED-Controller should be installed (needed for the "
echo -e "Service-Startup):?"
echo -e " "
options=("ssd1306" "sh1106" "Quit")

select opt in "${options[@]}"
do
    case $opt in
        "ssd1306")
            controller="ssd1306"
            break
            ;;
        "sh1106")
            controller="sh1106"
            break
            ;;
        "Quit")
            exit
            ;;
        *) echo -e "Invalid option $REPLY";;
    esac
done

clear
echo -e "////////////////////////////////////////////////////////////////////"
echo -e "///${cyan}   Please choose your display brightness:                     ${nocolor}///"
echo -e "////////////////////////////////////////////////////////////////////"
echo -e ""
echo -e "Choose your initial setting for brightness, you can change it later:"
echo -e " "
options=("1 dark" "2 normal" "3 bright" "4 very bright" "Quit")

select opt in "${options[@]}"
do
    case $opt in
        "1 dark")
			echo -e ""
            contrast="0"
			echo -e " "
            break
            ;;
        "2 normal")
            echo -e ""
			contrast="85"
			echo -e " "
            break
            ;;
        "3 bright")
            echo -e ""
			contrast="170"
			echo -e " "
            break
            ;;
        "4 very bright")
            echo -e ""
			contrast="255"
			echo -e " "
            break
            ;;
        "Quit")
            exit
            ;;
        *) echo -e "Invalid option $REPLY";;
    esac
done

clear
echo -e "////////////////////////////////////////////////////////////////////"
echo -e "///${cyan}   Please choose your display mode:                           ${nocolor}///"
echo -e "////////////////////////////////////////////////////////////////////"
echo -e ""
echo -e "${cyan}Full${nocolor} is a display mode with much informations like"
echo -e "  -> Tracks and Trackinformations"
echo -e "  -> Wifi-Signal"
echo -e ""
echo -e "${cyan}Lite${nocolor} is a simple display mode just showing the"
echo -e "Tracknr. and WLAN-Signal, other featues like brightness control are"
echo -e "still available."
echo -e ""
echo -e "${cyan}Mix${nocolor} is a mix between lite and full without"
echo -e "Trackinformations like Name, Album and so on. Just Tracks, WLAN-"
echo -e "Signal, Volume and Length."
echo -e ""
echo -e "Choose your Display mode.:"
echo -e " "
options=("Full" "Lite" "Mix" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Full")
			echo -e ""
            mode="full"
			echo -e " "
            break
            ;;
        "Lite")
            echo -e ""
			mode="lite"
			echo -e " "
            break
            ;;
        "Mix")
            echo -e ""
			mode="mix"
			echo -e " "
            break
            ;;
        "Quit")
            exit
            ;;
        *) echo -e "Invalid option $REPLY";;
    esac
done

clear
cd
echo -e "////////////////////////////////////////////////////////////////////"
echo -e "///${cyan}   Check/Install Prerequirements:                             ${nocolor}///"
echo -e "////////////////////////////////////////////////////////////////////"
echo -e " "
echo -e "Do you want to start the installation of needed packages?"
echo -e " "
options=("Install" "Quit")

select opt in "${options[@]}"
do
    case $opt in
        "Install")
            break
            ;;

        "Quit")
            exit
            ;;
        *) echo -e "invalid option $REPLY";;
    esac
done
echo -e ""
echo -e "Starting installation-process, pleae wait, some steps taking"
echo -e "minutes, especially the luma-Packages..."
echo -e ""
echo -e -n "   --> Update Sources:          "
sudo apt -qq update > /dev/null 2>&1
echo -e "${green}done${nocolor}"
echo -e ""
echo -e "Install packages..."

lineLen=24
packages=(git python3 build-essential python3-dev python3-pip python-pil libjpeg-dev i2c-tools) # python3-smbus i2c-tools  libfreetype6-dev   python3-pygame libtiff5)
for p in ${packages[@]}; do
	i=0
	echo -n -e "   --> $p:"
    let lLen="$lineLen"-"${#p}"
    while [ "$i" -lt "$lLen" ]
    do
		let i+=1
		echo -n -e " "
	done
    installer=`sudo dpkg -s ${p}  2>&1 | grep Status | grep installed`
    if [ "$installer" = "" ]
    then
		installer=`sudo apt -qq -y install ${p} > /dev/null 2>&1`
		installer=`sudo dpkg -s ${p} 2>&1 | grep Status | grep installed`
		if [ "$installer" = "" ]
		then
			echo -e "${red}failed${nocolor}"
		else
			echo -e "${green}done${nocolor}"
		fi
	else
		echo -e "${green}already installed${nocolor}"
	fi
done
lumaPackages=(luma.core luma.oled netifaces)
for p in ${lumaPackages[@]}; do
	i=0
	let lLen="$lineLen"-"${#p}"
	echo -n -e "   --> $p:"
	while [ "$i" -lt "$lLen" ]
	do
		let i+=1
		echo -n -e " "
	done
	pipInstalled=`sudo pip3 show ${p}`
	if [ "$pipInstalled" = "" ]
	then
		sudo pip3 install ${p}  > /dev/null 2>&1
		pipInstalled=`sudo pip3 show ${p}`
		if [ "$pipInstalled" = "" ]
		then
			echo -e "${red}failed${nocolor}"
		else
			echo -e "${green}done${nocolor}"
		fi
	else
		echo -e "${green}already installed${nocolor}"
	fi
done
echo -e ""
echo -e "Enable I2C..."
if grep -q 'i2c-bcm2708' /etc/modules; then
  echo -e "   --> i2c-bcm2708 module:      ${green}already exists${nocolor}"
else
  echo 'i2c-bcm2708' | sudo tee -a /etc/modules > /dev/null 2>&1
  echo -e "   --> i2c-bcm2708 module:      ${green}activated${nocolor}"
fi
if grep -q 'i2c-dev' /etc/modules; then
  echo -e "   --> i2c-dev module:          ${green}already exists${nocolor}"
else
  echo 'i2c-dev' | sudo tee -a /etc/modules > /dev/null 2>&1
  echo -e "   --> i2c-dev module:          ${green}activated${nocolor}"
fi
if grep -q '^dtparam=i2c1=on' /boot/config.txt; then
  echo -e "   --> i2c1 boot-parameter:     ${green}already set${nocolor}"
else
  echo 'dtparam=i2c1=on' | sudo tee -a /boot/config.txt > /dev/null 2>&1
  echo -e "   --> i2c1 boot-parameter:     ${green}set${nocolor}"
fi
if grep -q '^dtparam=i2c_arm=on' /boot/config.txt; then
  echo -e "   --> i2c_arm boot-parameter:  ${green}already set${nocolor}"
else
  echo 'dtparam=i2c_arm=on' | sudo tee -a /boot/config.txt > /dev/null 2>&1
  echo -e "   --> i2c_arm boot-parameter:  ${green}set${nocolor}"
fi
if [ -f /etc/udev/rules.d/99-i2c.rules ]; then
  if grep -q '^SUBSYSTEM=="i2c-dev", TAG+="systemd"' /etc/udev/rules.d/99-i2c.rules; then
    echo -e "   --> i2c dev dependency:      ${green}already set${nocolor}"
  else
    echo 'SUBSYSTEM=="i2c-dev", TAG+="systemd"' | sudo tee  /etc/udev/rules.d/99-i2c.rules > /dev/null 2>&1
    echo -e "   --> i2c dev dependency:      ${green}set${nocolor}"
  fi
else
  echo 'SUBSYSTEM=="i2c-dev", TAG+="systemd"' | sudo tee  /etc/udev/rules.d/99-i2c.rules > /dev/null 2>&1
  echo -e "   --> i2c dev dependency:      ${green}set${nocolor}"
fi

if [ -f /etc/modprobe.d/raspi-blacklist.conf ]; then
  sudo sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
  sudo sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
fi

echo -e ""
read -n 1 -s -r -p "Press any key to continue"

clear
echo -e "////////////////////////////////////////////////////////////////////"
echo -e "///${cyan}   Installing Service:                                        ${nocolor}///"
echo -e "////////////////////////////////////////////////////////////////////"
echo -e ""
echo -e "Repository:       ${green}${repo}${nocolor}"
echo -e "Branch:           ${green}${branch}${nocolor}"
echo -e "Install Path:     ${green}${installPath}${nocolor}"
echo -e "Display Mode:     ${green}${mode}${nocolor}"
echo -e "Controler Type:   ${green}${controller}${nocolor}"
echo -e "Contrast:         ${green}${contrast}${nocolor}"
echo -e ""
echo -e -n "   --> Delete old Service:                "
sudo service oled_phoniebox stop > /dev/null 2>&1
sudo systemctl disable /etc/systemd/oled_phoniebox.service > /dev/null 2>&1
sudo rm /etc/systemd/oled_phoniebox.service > /dev/null 2>&1
echo -e "${green}Done${nocolor}"
echo -e ""
echo -e -n "   --> Delete old Repository:             "
sudo rm -R ${installPath} > /dev/null 2>&1
echo -e "${green}Done${nocolor}"
echo -e ""
echo -e -n "   --> Clone oled_phoniebox Repository:   "

git clone ${repo} --branch ${branch} ${installPath} > /dev/null 2>&1
echo -e "${green}Done${nocolor}"
echo -e ""
echo -e -n "   --> Write Config-File:                 "
sudo cp ${installPath}/templates/conf.template ${installPath}/oled_phoniebox.conf > /dev/null
sudo sed -i -e "s:<contrastvalue>:${contrast}:g" ${installPath}/oled_phoniebox.conf> /dev/null
sudo sed -i -e "s:<controllervalue>:${controller}:g" ${installPath}/oled_phoniebox.conf> /dev/null
sudo sed -i -e "s:<modevalue>:${mode}:g" ${installPath}/oled_phoniebox.conf> /dev/null
echo -e "${green}Done${nocolor}"
echo -e ""
echo -e -n "   --> Installing Service:                "
sudo chown -R pi:pi ${installPath} > /dev/null
#sudo chmod +x ${installPath}/oled_phoniebox.py > /dev/null
sudo cp ${installPath}/templates/service.template /etc/systemd/oled_phoniebox.service > /dev/null
sudo chown root:root /etc/systemd/oled_phoniebox.service > /dev/null 2>&1
sudo chmod 644 /etc/systemd/oled_phoniebox.service > /dev/null 2>&1
sudo sed -i -e "s:<PATH>:${installPath}:g" /etc/systemd/oled_phoniebox.service > /dev/null
sudo systemctl daemon-reload > /dev/null 2>&1
sudo systemctl enable /etc/systemd/oled_phoniebox.service > /dev/null 2>&1
sudo service oled_phoniebox restart > /dev/null 2>&1
sudo service phoniebox-gpio-buttons restart > /dev/null 2>&1
echo -e "${green}Done${nocolor}"
echo -e ""
read -n 1 -s -r -p "Press any key to continue"
clear
echo -e "////////////////////////////////////////////////////////////////////"
echo -e "///${cyan}   Edit gpio-buttons.py                                       ${nocolor}///"
echo -e "////////////////////////////////////////////////////////////////////"
echo -e ""
echo -e "If jukebox4kids is already installed, you can choose your new config"
echo -e "for the file:"
echo -e "  ${yellow}/home/pi/RPi-Jukebox-RFID/scripts/gpio-buttons.py${nocolor}"
echo -e ""
echo -e "${cyan}Option 1:${nocolor}"
echo -e "Just deactivate GPIO Pin 3 for the shutdown. This Pin is needed and"
echo -e "used for I2C-Display! The origin gpio-buttons.py-File from the"
echo -e "RPi-Jukebox-RFID-Repository will be changed!!!"
echo -e ""
echo -e "${cyan}Option 2:${nocolor}"
echo -e "Replace the gpio-buttons.py-Service with a file from this "
echo -e "Repository for contrast-control with the prev- and next-Buttons."
echo -e "The origin Repository remains untouched."
echo -e ""
echo -e "${cyan}Option 3:${nocolor}"
echo -e "Just skip... ${red}Needed, if jukebox4kids is not installed!!!${nocolor}"
echo -e " "
echo -e "I recommend option 2 or 3, because editing the origin service could"
echo -e "make problems!"
echo -e " "
options=("Option 1: Deactivate GPIO Pin 3" "Option 2: Replace service for contrast-control" "Option 3: Skip")

select opt in "${options[@]}"
do
    case $opt in
        "Option 1: Deactivate GPIO Pin 3")
			echo -e " "
			sudo service phoniebox-gpio-buttons stop > /dev/null 2>&1
            sudo sed -i -e "s:shut = Button(3, hold_time=2):#shut = Button(3, hold_time=2):g" /home/pi/RPi-Jukebox-RFID/scripts/gpio-buttons.py > /dev/null
			sudo service phoniebox-gpio-buttons start > /dev/null 2>&1
			echo -e "   --> Button replacement finished"
			echo -e ""
            break
            ;;
        "Option 2: Replace service for contrast-control")
			echo -e " "
			echo -e -n "   --> Delete old Service:                "
			#sudo chmod +x ${installPath}/scripts/gpio-buttons/gpio-buttons.py > /dev/null
			sudo service phoniebox-gpio-buttons stop > /dev/null 2>&1
			sudo systemctl disable phoniebox-gpio-buttons > /dev/null  2>&1
			sudo rm /etc/systemd/system/phoniebox-gpio-buttons.service > /dev/null  2>&1
			echo -e "${green}Done${nocolor}"
			echo -e -n "   --> Installing Service:                "
			sudo cp ${installPath}/templates/gpio-service.template /etc/systemd/system/phoniebox-gpio-buttons.service > /dev/null 2>&1
			sudo sed -i -e "s:<PATH>:${installPath}:g" /etc/systemd/system/phoniebox-gpio-buttons.service > /dev/null 2>&1
			sudo chown root:root /etc/systemd/system/phoniebox-gpio-buttons.service > /dev/null 2>&1
			sudo chmod 644 /etc/systemd/system/phoniebox-gpio-buttons.service > /dev/null 2>&1
			sudo systemctl enable phoniebox-gpio-buttons > /dev/null 2>&1
			sudo service phoniebox-gpio-buttons start > /dev/null 2>&1
			echo -e "${green}Done${nocolor}"
			echo -e ""
            break
            ;;
        "Option 3: Skip")
			break
            ;;
        *) echo -e "Invalid option $REPLY";;
    esac
done
echo -e ""
read -n 1 -s -r -p "Press any key to continue"

clear
echo -e ""
echo -e "/////////////////////////////////////////////////////////////////////////////////////////////////////////"
echo -e "///                                                                                                   ///"
echo -e "///   ${green}██╗███╗   ██╗███████╗████████╗ █████╗ ██╗     ██╗      █████╗ ████████╗██╗ ██████╗ ███╗   ██╗   ${nocolor}///";
echo -e "///   ${green}██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║     ██║     ██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║   ${nocolor}///";
echo -e "///   ${green}██║██╔██╗ ██║███████╗   ██║   ███████║██║     ██║     ███████║   ██║   ██║██║   ██║██╔██╗ ██║   ${nocolor}///";
echo -e "///   ${green}██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║     ██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║   ${nocolor}///";
echo -e "///   ${green}██║██║ ╚████║███████║   ██║   ██║  ██║███████╗███████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║   ${nocolor}///";
echo -e "///   ${green}╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ${nocolor}///";
echo -e "///                                                                                                   ///";
echo -e "///   ${green} ██████╗ ██████╗ ███╗   ███╗██████╗ ██╗     ███████╗████████╗███████╗                           ${nocolor}///";
echo -e "///   ${green}██╔════╝██╔═══██╗████╗ ████║██╔══██╗██║     ██╔════╝╚══██╔══╝██╔════╝                           ${nocolor}///";
echo -e "///   ${green}██║     ██║   ██║██╔████╔██║██████╔╝██║     █████╗     ██║   █████╗                             ${nocolor}///";
echo -e "///   ${green}██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝     ██║   ██╔══╝                             ${nocolor}///";
echo -e "///   ${green}╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ███████╗███████╗   ██║   ███████╗                           ${nocolor}///";
echo -e "///   ${green} ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝   ╚═╝   ╚══════╝                           ${nocolor}///";
echo -e "///                                                                                                   ///"
echo -e "/////////////////////////////////////////////////////////////////////////////////////////////////////////"
echo -e ""
echo -e "If this is a new installation, a reboot is required..."
echo -e ""
echo -e "Do you want to reboot now?"
echo -e " "
options=("Reboot" "Quit")

select opt in "${options[@]}"
do
    case $opt in
        "Reboot")
            sudo reboot
            ;;

        "Quit")
            exit
            ;;
        *) echo -e "invalid option $REPLY";;
    esac
done

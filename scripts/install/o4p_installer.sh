#!/bin/bash
# Colors: \e[36m=Cyan M ; \e[92m=Light green ; \e[91m=Light red ; \e[93m=Light yellow ; \e[31m=green ; \e[0m=Default ; \e[33m=Yellow ; \e[31m=Red

nocolor='\e[0m'
red="\e[91m"
blue="\033[1;34"
cyan="\e[36m"
yellow="\e[93m"
green="\e[92m"

clear
echo -e "////////////////////////////////////////////////////////////////////"
echo -e "///${cyan}     ____  __   _______    ___  _          __                 ${nocolor}///"
echo -e "///${cyan}    / __ \/ /  / __/ _ \  / _ \(_)__ ___  / /__ ___ __        ${nocolor}///"
echo -e "///${cyan}   / /_/ / /__/ _// // / / // / (_-</ _ \/ / _ \`/ // /        ${nocolor}///"
echo -e "///${cyan}   \____/____/___/____/ /____/_/___/ .__/_/\_,_/\_, /         ${nocolor}///"
echo -e "///${cyan}      ___           ___  __       /_/   _     _/___/          ${nocolor}///"
echo -e "///${cyan}     / _/__  ____  / _ \/ /  ___  ___  (_)__ / /  ___ __ __   ${nocolor}///"
echo -e "///${cyan}    / _/ _ \/ __/ / ___/ _ \/ _ \/ _ \/ / -_) _ \/ _ \\ \ /   ${nocolor}///"
echo -e "///${cyan}   /_/ \___/_/   /_/  /_//_/\___/_//_/_/\__/_.__/\___/_\_\    ${nocolor}///"
echo -e "///                                                              ///"
echo -e "////////////////////////////////////////////////////////////////////"
echo -e "///                                                              ///"
echo -e "///${cyan}           https://github.com/splitti/oled_phoniebox           ${nocolor}///"
echo -e "///                                                              ///"
echo -e "////////////////////////////////////////////////////////////////////"
echo -e ""
echo -e "Please notice: This script will install all needed components for"
echo -e "the OLED-Display (Format 128 X 64px) with SH1106- or SSD1306-"
echo -e "Controller. A preinstallation of the jukebox4kids or similiar (MPC)"
echo -e "will be needed."
echo -e " "
echo -e "Do want to install this OLED-Display-Service?"
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
echo -e "Service-Startup:?"
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
cd
echo -e "////////////////////////////////////////////////////////////////////"
echo -e "///${cyan}   Check/Install Prerequirements:                             ${nocolor}///"
echo -e "////////////////////////////////////////////////////////////////////"
echo -e ""
echo -e "Starting installation-process, pleae wait..."
echo -e ""
echo -e -n ">>> Update Sources:          "
sudo apt -qq update > /dev/null 2>&1
echo -e "${green}done${nocolor}"
echo -e ""
echo -e "Install packages..."

lineLen=24
packages=(git python3-dev python-imaging mc asdasdasdads python3-smbus i2c-tools python3-pip libfreetype6-dev libjpeg-dev build-essential python3-pygame libtiff5)
for p in ${packages[@]}; do
                i=0
                echo -n -e ">>> $p:"
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
lumaPackages=(luma.oled luma.core)
echo -e -n ">>> luma.oled:               "
pipInstalled=`sudo pip3 list --format=columns | grep luma.oled`
if [ "$pipInstalled" = "" ]
then
	sudo pip3 install --upgrade luma.oled  > /dev/null 2>&1
	pipInstalled=`sudo pip3 list --format=columns | grep luma.oled`
	if [ "$pipInstalled" = "" ]
	then
		echo -e "${red}failed${nocolor}"
	else
		echo -e "${green}done${nocolor}"
	fi
else
	echo -e "${green}already installed${nocolor}"
fi
echo -e ""
read -n 1 -s -r -p "Press any key to continue"

clear
echo -e "////////////////////////////////////////////////////////////////////"
echo -e "///${cyan}   Installing Service:                                        ${nocolor}///"
echo -e "////////////////////////////////////////////////////////////////////"
echo -e ""
echo -e ">>> Delete old Repository..."
sudo rm -R oled_phoniebox > /dev/null 2>&1
echo -e ""
echo -e ">>> Clone oled_phoniebox Repository..."
installPath="/home/pi/oled_phoniebox"
sudo git clone https://github.com/splitti/oled_phoniebox --branch development ${installPath}  > /dev/null 2>&1
sudo chown pi:pi ${installPath}/scripts/contrast/contrast.last > /dev/null
echo -e ""
echo -e ">>> Installing Service..."
sudo systemctl disable /etc/systemd/oled_phoniebox.service > /dev/null 2>&1
sudo rm /etc/systemd/oled_phoniebox.service > /dev/null 2>&1
sudo cp ${installPath}/service.template /etc/systemd/oled_phoniebox.service > /dev/null
sudo sed -i -e "s:<PATH>:$installPath:g" /etc/systemd/oled_phoniebox.service > /dev/null
sudo sed -i -e "s:<CONTROLLER>:$controller:g" /etc/systemd/oled_phoniebox.service > /dev/null
sudo systemctl daemon-reload > /dev/null
sudo systemctl enable /etc/systemd/oled_phoniebox.service
sudo service oled_phoniebox start
echo -e ""
echo -e "${green}INSTALLATION FINISHED${nocolor}"
echo -e ""
read -n 1 -s -r -p "Press any key to end install-process"
echo -e ""


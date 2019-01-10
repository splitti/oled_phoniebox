#!/bin/bash
# Colors: \e[36m=Cyan M ; \e[92m=Light green ; \e[91m=Light red ; \e[93m=Light yellow ; \e[31m=green ; \e[0m=Default ; \e[33m=Yellow ; \e[31m=Red

nocolor='\e[0m'
red="\e[91m"
blue="\033[1;34"
cyan="\e[36m"
yellow="\e[93m"
green="\e[92m"

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
echo -e "Please notice: This script will install all needed components for the OLED-Display (Format 128 X 64px) with"
echo -e "SH1106- or SSD1306-Controller. A preinstallation of the jukebox4kids or similiar (MPC) will be needed."
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
packages=(git python3 build-essential python3-dev python3-pip python-imaging) # python3-smbus i2c-tools  libfreetype6-dev libjpeg-dev  python3-pygame libtiff5)
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
lumaPackages=(luma.core luma.oled)
for p in ${lumaPackages[@]}; do
	i=0
	let lLen="$lineLen"-"${#p}"
	echo -n -e ">>> $p:"
	while [ "$i" -lt "$lLen" ]
	do
		let i+=1
		echo -n -e " "
	done
	pipInstalled=`sudo pip3 show ${p}`
	if [ "$pipInstalled" = "" ]
	then
		sudo pip3 install luma.oled  > /dev/null 2>&1
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
read -n 1 -s -r -p "Press any key to continue"

clear
installPath="/home/pi/oled_phoniebox"
echo -e "////////////////////////////////////////////////////////////////////"
echo -e "///${cyan}   Installing Service:                                        ${nocolor}///"
echo -e "////////////////////////////////////////////////////////////////////"
echo -e ""
echo -e "Install Path:                          ${green}$installPath${nocolor}"
echo -e "Controler Type:                        ${green}$controller${nocolor}"
echo -e ""
echo -e -n ">>> Delete old Service:                "
sudo sudo service oled_phoniebox stop > /dev/null 2>&1
sudo systemctl disable /etc/systemd/oled_phoniebox.service > /dev/null 2>&1
sudo rm /etc/systemd/oled_phoniebox.service > /dev/null 2>&1
echo -e "${green}Done${nocolor}"
echo -e ""
echo -e -n ">>> Delete old Repository:             "
sudo rm -R ${installPath} > /dev/null 2>&1
echo -e "${green}Done${nocolor}"
echo -e ""
echo -e -n ">>> Clone oled_phoniebox Repository:   "

git clone https://github.com/splitti/oled_phoniebox --branch development ${installPath} > /dev/null 2>&1
sudo chown -R pi:pi ${installPath} > /dev/null
echo -e "${green}Done${nocolor}"
echo -e ""
echo -e -n ">>> Installing Service:                "
sudo cp ${installPath}/service.template /etc/systemd/oled_phoniebox.service > /dev/null
sudo sed -i -e "s:<PATH>:$installPath:g" /etc/systemd/oled_phoniebox.service > /dev/null
sudo sed -i -e "s:<CONTROLLER>:$controller:g" /etc/systemd/oled_phoniebox.service > /dev/null
sudo systemctl daemon-reload > > /dev/null 2>&1
sudo systemctl enable /etc/systemd/oled_phoniebox.service > /dev/null 2>&1
sudo service oled_phoniebox start > /dev/null 2>&1
echo -e "${green}Done${nocolor}"
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
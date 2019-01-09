#!/bin/bash

# Colors: \e[96m = Cyan M \e[96m = Light green ; \e[91m = Light red ; \e[93m = Light yellow ; \e[31m = green ; \e[39m = Default ; \e[33m = Yellow ; \e[31m = Red


if [ "$EUID" -ne 0 ]
  then echo "Please run as root: sudo setup.sh"
  exit
fi

clear
echo "////////////////////////////////////////////////////////////////////
///\e[96m     ____  __   _______    ___  _          __                 \e[39m///
///\e[96m    / __ \/ /  / __/ _ \  / _ \(_)__ ___  / /__ ___ __        \e[39m///
///\e[96m   / /_/ / /__/ _// // / / // / (_-</ _ \/ / _ `/ // /        \e[39m///
///\e[96m   \____/____/___/____/ /____/_/___/ .__/_/\_,_/\_, /         \e[39m///
///\e[96m      ___           ___  __       /_/   _     _/___/          \e[39m///
///\e[96m     / _/__  ____  / _ \/ /  ___  ___  (_)__ / /  ___ __ __   \e[39m///
///\e[96m    / _/ _ \/ __/ / ___/ _ \/ _ \/ _ \/ / -_) _ \/ _ \\ \ /   \e[39m///
///\e[96m   /_/ \___/_/   /_/  /_//_/\___/_//_/_/\__/_.__/\___/_\_\    \e[39m///
///                                                              ///
////////////////////////////////////////////////////////////////////
///                                                              ///
///\e[96m           https://github.com/splitti/oled_phoniebox           \e[39m///
///                                                              ///
////////////////////////////////////////////////////////////////////

Please notice: This script will install all needed components for
the OLED-Display (Format 128 X 64px) with SH1106- or SSD1306-
Controller. A preinstallation of the jukebox4kids or similiar (MPC)
will be needed.

Do want to install this OLED-Display-Service?"

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
        *) echo "invalid option $REPLY";;
    esac
done

cls
echo "////////////////////////////////////////////////////////////////////"
echo "///\e[96m   Please choose your display controller type:                \e[39m///"
echo "////////////////////////////////////////////////////////////////////"

options=("Controller type ssd1306" "Controller type sh1106" "Quit")

select opt in "${options[@]}"
do
    case $opt in
        "Controller type ssd1306")
            controller="ssd1306"
            break
            ;;
        "Controller type sh1106")
            controller="sh1106"
            break
            ;;
        "Quit")
            exit
            ;;
        *) echo "Invalid option $REPLY";;
    esac
done

thisPath=`pwd`
cls
cd
echo "////////////////////////////////////////////////////////////////////"
echo "///\e[96m   Check/Install Prerequirements:                             \e[39m///"
echo "////////////////////////////////////////////////////////////////////"
echo ">>> \e[96mUpdate Sources"
apt --qq update

packages=(git python3-dev python-imaging python3-smbus i2c-tools python3-pip libfreetype6-dev libjpeg-dev build-essential python3-pygame libtiff5)
for p in ${packages[@]}; do
    installer = `dpkg -l | grep p`
	if ${installer} != p
		echo ">>> \e[96mInstall ${p}"
		installer = `apt install -qq -y ${p}`
		installer = `ècho $installer | grep installed`
		if $installer == ""
			echo ">>> \e[91mInstallation failed:    ${p}"	
		else
			echo ">>> \e[96mInstallation finished:  ${p}"			
		fi
	else
		echo ">>> \e[96mAlready installed:      ${p}"
	fi	
done
sleep 2
exit
echo ">>> \e[92mClone luma.examples from github"
echo ">>> Clone luma.examples from github"
git clone https://github.com/rm-hull/luma.examples $thisPath/luma.examples
echo ">>> Installing luma Packages"
pip3 install --upgrade luma.oled
pip3 install -e $thisPath/luma.examples/
echo ">>> Installing Service..."
rm /etc/systemd/oled_phoniebox.service
cp $thisPath/service.template /etc/systemd/oled_phoniebox.service
sed -i -e "s:<PATH>:$thisPath:g" /etc/systemd/oled_phoniebox.service
sed -i -e "s:<CONTROLLER>:$controller:g" /etc/systemd/oled_phoniebox.service
sudo systemctl daemon-reload
systemctl enable /etc/systemd/oled_phoniebox.service
service oled_phoniebox start
#service oled_phoniebox status
echo ">>> Installation finished"
echo ">>> Please reboot Pi"
echo ">>> Changing some File Permissons"
echo ">>> Controller type: \e[31m            "$controller
echo ">>> Installing needed packages..."
chown pi:pi $thisPath/scripts/contrast/contrast.last

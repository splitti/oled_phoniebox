#!/bin/bash

# Colors: \e[92m = Light green ; \e[91m = Light red ; \e[93m = Light yellow ; \e[31m = green ; \e[39m = Default ; \e[33m = Yellow ; \e[31m = Red


if [ "$EUID" -ne 0 ]
  then echo "Please run as root: sudo setup.sh"
  exit
fi

clear
echo "////////////////////////////////////////////////////////////////////
///     ____  __   _______    ___  _          __                 ///
///    / __ \/ /  / __/ _ \  / _ \(_)__ ___  / /__ ___ __        ///
///   / /_/ / /__/ _// // / / // / (_-</ _ \/ / _ `/ // /        ///
///   \____/____/___/____/ /____/_/___/ .__/_/\_,_/\_, /         ///
///      ___           ___  __       /_/   _     _/___/          ///
///     / _/__  ____  / _ \/ /  ___  ___  (_)__ / /  ___ __ __   ///
///    / _/ _ \/ __/ / ___/ _ \/ _ \/ _ \/ / -_) _ \/ _ \\ \ /   ///
///   /_/ \___/_/   /_/  /_//_/\___/_//_/_/\__/_.__/\___/_\_\    ///
///                                                              ///
////////////////////////////////////////////////////////////////////
///                                                              ///
///          https://github.com/splitti/oled_phoniebox           ///
///                                                              ///
////////////////////////////////////////////////////////////////////

Please notice: This script will install all needed components for
the OLED-Display (Format 128 X 64px) with SH1106- or SSD1306-
Controller. A preinstallation of the jukebox4kids or similiar (MPC)
will be needed."

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
echo "///   Please choose your display controller type:                ///"
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
        *) echo "invalid option $REPLY";;
    esac
done

thisPath=`pwd`
cls
cd
echo "////////////////////////////////////////////////////////////////////"
echo "///   Prerequirements:                                           ///"
echo "////////////////////////////////////////////////////////////////////"
apt update
apt install -y git 
apt install -y python3-dev
apt install -y python-imaging
apt install -y python3-smbus
apt install -y i2c-tools
apt install -y python3-pip
apt install -y libfreetype6-dev
apt install -y libjpeg-dev
apt install -y build-essential
apt install -y python3-pygame
apt install -y libtiff5

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

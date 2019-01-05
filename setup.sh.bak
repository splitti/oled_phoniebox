#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root: sudo setup.sh"
  exit
fi
echo "Installaing OLED Display Python Based Service for Jukebox4kids"
echo "=============================================================="
echo "Please choose your display controller type: "
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
echo ">>> Install Path: "$thisPath
echo ">>> Controller type: "$controller
echo ">>> Installing needed packages..."
apt install -y python3-dev python-imaging python3-smbus i2c-tools python3-pip libfreetype6-dev libjpeg-dev build-essential python3-pygame libtiff5
echo ">>> Clone luma.examples from github"
git clone https://github.com/rm-hull/luma.examples $thisPath/luma.examples
echo ">>> Installing luma Packages"
pip3 install --upgrade luma.oled
pip3 install -e $thisPath/luma.examples/
echo ">>> Link demo_opts.py"
rm $thisPath/demo_opts.py
ln -s $thisPath/luma.examples/examples/demo_opts.py $thisPath/demo_opts.py
echo ">>> Installing Service..."
rm /etc/systemd/oled_phoniebox.service
cp $thisPath/service.template /etc/systemd/oled_phoniebox.service
sed -i -e "s:<PATH>:$thisPath:g" /etc/systemd/oled_phoniebox.service
sed -i -e "s:<CONTROLLER>:$controller:g" /etc/systemd/oled_phoniebox.service
sudo systemctl daemon-reload
systemctl enable /etc/systemd/oled_phoniebox.service
#service oled_phoniebox start
service oled_phoniebox status
echo ">>> Installation finished"
echo ">>> Please reboot Pi"

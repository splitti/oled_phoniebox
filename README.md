# oled_phoniebox
oled_phoniebox
Based on https://github.com/rm-hull/luma.oled

## Installation Steps

### Installation I2C
Please follow these Instructions: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

### Deactivate Buttons
It is possible, that the Display uses the same GPIO like the Shut-Command of the jukebox4kids. In this case, you should edit the file gpio-buttons.py like this
> sed -i -e "s:shut = Button(3, hold_time=2):#shut = Button(3, hold_time=2):g" ~/RPi-Jukebox-RFID/scripts/gpio-buttons.py

### Service Installation
1. sudo apt install -y git 
2. sudo git clone https://github.com/splitti/oled_phoniebox ~/oled_phoniebox
3. cd ~/oled_phoniebox
4. sudo chmod 777 setup.sh
5. sudo ./setup.sh


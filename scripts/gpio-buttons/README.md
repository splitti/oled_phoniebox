# GPIO-Buttons Example for Contrast Control

## Contrast Control
You can control the contrast level in four steps. You can use this Python-Script or modify the code, maybe for different ways of controlling the contrast level. 
Please notice:
- The Contrast-Level will be done by the Mainscript of the Oled Phoniebox Script. This Script must be started!
- The Mainscript works with a sleep-intervall, so the Display reacts with a small delay.

### Installation
Copy the script like this way:
> sudo mv /home/pi/RPi-Jukebox-RFID/scripts/gpio-buttons.py /home/pi/RPi-Jukebox-RFID/scripts/gpio-buttons.py_original
> sudo cp /home/pi/oled_phoniebox/scripts/gpio-buttons/gpio-buttons.py /home/pi/RPi-Jukebox-RFID/scripts/gpio-buttons.py
> sudo kill $(ps aux | grep gpio-buttons.py | grep -v grep | awk '{print $2}')

That's it.

Please notice:
- I disabled the Shutdown-Button, because we use the Gpio for the OLED Display
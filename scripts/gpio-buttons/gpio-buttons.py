#!/usr/bin/python3
from gpiozero import Button
from signal import pause
from subprocess import check_call
from time import sleep

# This script will block any I2S DAC e.g. from Hifiberry, Justboom, ES9023, PCM5102A
# due to the assignment of GPIO 19 and 21 to a buttons

# 2018-10-31
# Added the function on holding volume + - buttons to change the volume in 0.3s interval
#
# 2018-10-15
# this script has the `pull_up=True` for all pins. See the following link for additional info: 
# https://github.com/MiczFlor/RPi-Jukebox-RFID/issues/259#issuecomment-430007446
#
# 2017-12-12
# This script was copied from the following RPi forum post:
# https://forum-raspberrypi.de/forum/thread/13144-projekt-jukebox4kids-jukebox-fuer-kinder/?postID=312257#post312257
# I have not yet had the time to test is, so I placed it in the misc folder.
# If anybody has ideas or tests or experience regarding this solution, please create pull requests or contact me.

def def_shutdown():
    check_call("./scripts/playout_controls.sh -c=shutdown", shell=True)

def def_volU():
    check_call("./scripts/playout_controls.sh -c=volumeup", shell=True)

def def_volD():
    check_call("./scripts/playout_controls.sh -c=volumedown", shell=True)

def def_vol0():
    check_call("./scripts/playout_controls.sh -c=mute", shell=True)

def def_next():
    sleep(0.5)
    if not next.is_pressed == True :
      check_call("./scripts/playout_controls.sh -c=playernext", shell=True)

def def_contrastup():
     check_call("/usr/bin/python3 /home/pi/oled_phoniebox/scripts/contrast/contrast_up.py", shell=True)

def def_contrastdown():
     check_call("/usr/bin/python3 /home/pi/oled_phoniebox/scripts/contrast/contrast_down.py", shell=True)

def def_prev():
    sleep(0.5)
    if not prev.is_pressed == True :
      check_call("./scripts/playout_controls.sh -c=playerprev", shell=True)

def def_halt():
    check_call("./scripts/playout_controls.sh -c=playerpause", shell=True)

def longPressCnt(Button,PressTime):
    PressTimer = 0
    for cnt in range(50):
      if Button.when_pressed == False :
        PressTimer = PressTimer + 1
      else:
        break
      sleep(0.1)
    if PressTimer >= PressTime:
      rc = True
    else:
      rc = False
    return rc

#shut = Button(3, hold_time=2)
vol0 = Button(13,pull_up=True)
volU = Button(16,pull_up=True,hold_time=0.3,hold_repeat=True)
volD = Button(19,pull_up=True,hold_time=0.3,hold_repeat=True)
next = Button(26,pull_up=True,hold_time=3.0,hold_repeat=False)
prev = Button(20,pull_up=True,hold_time=3.0,hold_repeat=False)
halt = Button(21,pull_up=True)

#shut.when_held = def_shutdown
vol0.when_pressed = def_vol0
volU.when_pressed = def_volU
#When the Volume Up button was held for more than 0.3 seconds every 0.3 seconds he will call a ra$
volU.when_held = def_volU
volD.when_pressed = def_volD
#When the Volume Down button was held for more than 0.3 seconds every 0.3 seconds he will lower t$
volD.when_held = def_volD
next.when_pressed = def_next
next.when_held = def_contrastup
prev.when_pressed = def_prev
prev.when_held = def_contrastdown
halt.when_pressed = def_halt

pause()

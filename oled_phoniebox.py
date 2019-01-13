#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# For more details go to https://github.com/splitti/oled_phoniebox/

import signal
import sys
sys.path.append("/home/pi/oled_phoniebox/scripts/")
from o4p_functions import Init,get_device,GetCurrContrast,SetCharacters,GetMPC,GetWifiConn,GetSpecialInfos
from time import sleep
from datetime import datetime
import os
from luma.core.render import canvas
from PIL import ImageFont, Image
font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                            'fonts', 'Bitstream Vera Sans Mono Roman.ttf'))
font = ImageFont.truetype(font_path, 12)
font_small = ImageFont.truetype(font_path, 10)
font_hightower = ImageFont.truetype(font_path, 54)

confFile = "/home/pi/oled_phoniebox/oled_phoniebox.conf"
tempFile = "/tmp/o4p_overview.temp"
version = "1.4.4 - 20190113"

def ShowImage(imgname):
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', imgname+'.png'))
    logo = Image.open(img_path).convert("RGBA")
    fff = Image.new(logo.mode, logo.size, (255,) * 4)
    background = Image.new("RGBA", device.size, "black")
    posn = ((device.width - logo.width) // 2, 0)
    img = Image.composite(logo, fff, logo)
    background.paste(img, posn)
    device.display(background.convert(device.mode))

def sigterm_handler(signal, frame):
    # save the state here or do whatever you want
    ShowImage("poweroff")
    sleep(1)
    os._exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

def main(num_iterations=sys.maxsize):
    oldContrast = GetCurrContrast(confFile)
    device.contrast(oldContrast)
    ShowImage("music")
    tmpcard = 3
    line1 = 4
    line2 = 19 
    line3 = 34
    line4org = 49
    line4 = device.height-1-10
    lenLine1 = -1
    lenLine2 = -1
    lenLine3 = -1
    subLine1 = 0
    subLine2 = 0
    subLine3 = 0
    widthLetter = 7
    spaceJump = 35
    oldMPC = ""
    oldPlaying = "-"
    displayTime = 3
    oldVol = "FirstStart"
    WifiConn = GetWifiConn()
    while num_iterations > 0:
      num_iterations = 1
      curr_time = datetime.now()
      seconds = curr_time.strftime('%S')
      sleep(0.8)
      seconds = int(seconds)%5
      if seconds == 0:
        WifiConn = GetWifiConn()
      try:
      #if WifiConn != "BUGFIXING_LINE":
        if os.path.exists(tempFile):
          specialInfos = GetSpecialInfos()
          with canvas(device) as draw:
            draw.text((0, line1),  "WLAN: "+specialInfos[0],font=font_small, fill="white")
            draw.text((0, line2),  "IP:   "+specialInfos[1],font=font_small, fill="white")
            draw.text((0, line3),  "Version:",font=font_small, fill="white")
            draw.text((0, line4org),version,font=font_small, fill="white")
          sleep(8)
          os.remove(tempFile)
        currContrast = GetCurrContrast(confFile)
        if currContrast != oldContrast:
          device.contrast(currContrast)
          oldContrast = currContrast
        mpcstatus = SetCharacters(GetMPC("mpc status"))
        playing = mpcstatus.split("\n")[1].split(" ")[0] #Split to see if mpc is playing at the moment
        currMPC = mpcstatus.split("\n")[0]
        if (playing == "[playing]") or (playing == "[paused]"):
          volume = mpcstatus.split("\n")[2].split("   ")[0].split(":")[1]
        else:
          volume = mpcstatus.split("   ")[0].split(":")[1]
        vol = "V"+str(volume.replace("%",""))
        if oldPlaying != playing:
          if playing == "[playing]":
            with canvas(device) as draw:
              draw.polygon([(49, 10), (79, 32), (49, 54)], outline="white", fill="white")
            sleep(displayTime)
          if playing == "[paused]":
            with canvas(device) as draw:
              draw.rectangle((51,10,59,54), outline="white", fill="white")
              draw.rectangle((69,10,77,54), outline="white", fill="white")
            sleep(displayTime)
          oldPlaying = playing
        volume = int(volume.replace(" ","").replace("%",""))
        if (oldVol != volume) and (oldVol != "FirstStart"):
          with canvas(device) as draw:
            draw.rectangle((30,22,45,42), outline="white", fill="white")
            draw.polygon([(45, 22),(60, 10), (60,54), (45, 42)], outline="white", fill="white")
            draw.rectangle((75,28,105,36), outline="white", fill="white")
            if oldVol < volume:
              draw.rectangle((86,17,94,47), outline="white", fill="white")
          sleep(displayTime)
        oldVol = volume
        if (playing == "[playing]") or (playing == "[paused]"):
          if playing == "[playing]":
            #timer = SetCharacters(GetMPC("mpc -f %time% current"))
            elapsed = mpcstatus.split("\n")[1].replace("  "," ").split(" ")[3]
          if currMPC != oldMPC:
            track =   mpcstatus.split("\n")[1].replace("  "," ").split(" ")[1].replace("#","") #SetCharacters(GetMPC("mpc -f %track% current"))
            if len(track.split("/")[1]) > 2:
              track = track.split("/")[0]
            if track == "\n":
              track = mpcstatus.split("\n")[1].replace("  ", " ").split(" ")[1].replace("#","") #.split("/")[0]
            if initVars['GENERAL']['mode'] == "full" :
              file = SetCharacters(GetMPC("mpc -f %file% current")) # Get the current title
              if file.startswith("http"): # if it is a http stream!
                txtLine1 = SetCharacters(GetMPC("mpc -f %name% current"))
                txtLine2 = SetCharacters(GetMPC("mpc -f %title% current"))
                txtLine3 = ""
                track = "--/--"
              else: # if it is not a stream
                  lenLine1 = -1
                  lenLine2 = -1
                  lenLine3 = -1
                  subLine1 = 0
                  subLine2 = 0
                  subLine3 = 0
                  txtLine1 = SetCharacters(GetMPC("mpc -f %album% current"))
                  txtLine3 = SetCharacters(GetMPC("mpc -f %title% current"))
                  txtLine2 = SetCharacters(GetMPC("mpc -f %artist% current"))
              if txtLine2 == "\n":
                  filename = SetCharacters(GetMPC("mpc -f %file% current"))
                  filename = filename.split(":")[2]
                  filename = SetCharacters(filename)
                  localfile = filename.split("/")
                  txtLine1 = localfile[1]
                  txtLine2 = localfile[0]
          if initVars['GENERAL']['mode'] == "lite" :
            track = track.split("/")[0]
            if len(track) == 1:
              xpos = device.width/2-15
            if len(track) == 2:
              xpos = device.width/2-30
            if len(track) == 3:
              xpos = device.width/2-45
            if len(track) == 4:
              xpos = device.width/2-60
            with canvas(device) as draw:
              draw.text((xpos, 4),track,font=font_hightower, fill="white")

          if initVars['GENERAL']['mode'] == "full" :
            if lenLine1 == -1:
              lenLine1 = (len(txtLine1)*widthLetter)-device.width+spaceJump
              if lenLine1 > 0 and lenLine1 < spaceJump:
                lenLine1 = spaceJump+1
              if lenLine1 < 1:
                lenLine1 = 0
              lenLine2 = (len(txtLine2)*widthLetter)-device.width+spaceJump
              if lenLine2 > 0 and lenLine2 < spaceJump:
                lenLine2 = spaceJump+1
              if lenLine2 < 1:
                lenLine2 = 0
                lenLine3 = (len(txtLine3)*widthLetter)-device.width+spaceJump
              if lenLine3 > 0 and lenLine3 < spaceJump:
                lenLine3 = spaceJump+1
              if lenLine3 < 1:
                lenLine3 = 0
              cnt = 0
            if (cnt < lenLine1+spaceJump) and (lenLine1 != 0):
              subLine1 = cnt
              subLine2 = 0
              subLine3 = 0
            else:
              subLine1 = 0
              if (cnt-lenLine1 < lenLine2) and (lenLine2 != 0):
                subLine2 = cnt-lenLine1
              else:
                subLine2 = 0
                if (cnt-lenLine2-lenLine3 < lenLine3) and (lenLine3 != 0):
                  subLine3 = cnt-lenLine1-lenLine2
                else:
                  cnt = 0
                  subLine3 = 0
            if playing != "[paused]":
              TimeLine = elapsed.split("/")
              if TimeLine[1] != "0:00":
                elapsed = TimeLine[1]
              else:
                elapsed = "-:--"
              if len(elapsed) == 4:
                elapsed = "L "+elapsed
              if len(elapsed) == 5:
                elapsed = "L"+elapsed
            else:
              elapsed = "PAUSE"
            if not file.startswith("http"):
              TimeLineP = int(mpcstatus.split("\n")[1].replace("   "," ").replace("  "," ").split(" ")[3].replace("(","").replace("%)",""))
              TimeLineP = device.width * TimeLineP / 100
            else:
              TimeLineP = device.width
            track = track.replace("\n","")
            if len(track) == 1:
              track = "    "+track
            if len(track) == 2:
              track = "   "+track
            if len(track) == 3:
              track = "  "+track
            if len(track) == 4:
              track = " "+track
            if len(track) == 5:
              track = track
            with canvas(device) as draw:
              draw.rectangle((0,0,TimeLineP,1), outline="white", fill="white")
              draw.rectangle((109, line4+8,111,line4+10), outline=WifiConn[0], fill=WifiConn[0])
              draw.rectangle((114, line4+6,116,line4+10), outline=WifiConn[1], fill=WifiConn[1])
              draw.rectangle((119, line4+4,121,line4+10), outline=WifiConn[2], fill=WifiConn[2])
              draw.rectangle((124, line4+2,126,line4+10), outline=WifiConn[3], fill=WifiConn[3])
              draw.line((0, line4-2, device.width, line4-2), fill="white")
              draw.line((39, line4-2, 39, device.height), fill="white")
              draw.line((75, line4-2, 75, device.height), fill="white")
              draw.line((105, line4-2, 105, device.height), fill="white")
              draw.text((0-subLine1, line1),txtLine1,font=font, fill="white")
              draw.text((0-subLine2, line2),txtLine2,font=font, fill="white")
              draw.text((0-subLine3, line3),txtLine3,font=font, fill="white")
              draw.text((0, line4),elapsed,font=font_small, fill="white")
              draw.text((42, line4),track,font=font_small, fill="white")
              draw.text((78, line4),vol,font=font_small, fill="white")
              draw.text((108, line4),"---",font=font_small, fill=WifiConn[4])
              oldMPC = currMPC
            seconds = int(seconds)%6
            if seconds == 0:
              cnt = cnt + spaceJump
        else:
          oldMPC = currMPC
          if tmpcard < 3:
            sleep(0.5)
            tmpcard = tmpcard + 1
          else:
            ShowImage("cardhand")
            tmpcard = 0
      except:
        sleep(0.5)
#        ShowImage("music")

#if __name__ == "__main__":
initVars = Init(confFile)
try:
  device = get_device(initVars['GENERAL']['controller'])
  main()
except KeyboardInterrupt:
  pass

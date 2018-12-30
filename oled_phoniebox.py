#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from time import sleep
from datetime import datetime
import os
from luma.core.render import canvas
from demo_opts import get_device
from PIL import ImageFont
from PIL import Image
font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                            'fonts', 'PIXEARG_.TTF')) #C&C Red Alert [INET].ttf'))
font = ImageFont.truetype(font_path, 8)
chars = {'ö':chr(246),'ä':chr(228),'ü':chr(252),'ß':chr(223),'Ä':chr(196),'Ü':chr(220),'Ö':chr(214),'%20':' ',' 1/4':chr(252),'%C3%9C':chr(220),'%C3%BC':chr(252),'%C3%84':chr(196),'%C3%A4':chr(228),'%C3%96':chr(214),'%C3%B6':chr(246),'%C3%9F':chr(223)}

def SetCharacters(text):
    for char in chars:
       text = text.replace(char,chars[char])
    return text

def GetMPC(command):
    from subprocess import check_output
    process = check_output(command.split())
    process = process.decode()
    for char in chars:
       process = process.replace(char,chars[char])
    return process

def ShowImage(imgname):
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', imgname+'.png'))
    logo = Image.open(img_path).convert("RGBA")
    fff = Image.new(logo.mode, logo.size, (255,) * 4)
    background = Image.new("RGBA", device.size, "black")
    posn = ((device.width - logo.width) // 2, 0)
    img = Image.composite(logo, fff, logo)
    background.paste(img, posn)
    device.display(background.convert(device.mode))
	
def main(num_iterations=sys.maxsize):
    line1 = 0
    line2 = 14
    line3 = 28
    line4 = device.height-1-10 
    lenLine1 = -1
    lenLine2 = -1
    lenLine3 = -1
    subLine1 = 0
    subLine2 = 0
    subLine3 = 0
    widthLetter = 7
    spaceJump = 60
    oldMPC = ""
    oldPlaying = "-"
    displayTime = 3
    oldVol = "FirstStart"

    while num_iterations > 0:
      try:
        num_iterations = 1
        sleep(0.5)
        mpcstatus = GetMPC("mpc status")
        playing = mpcstatus.split("\n")[1].split(" ")[0] #Split to see if mpc is playing at the moment
        currMPC = mpcstatus.split("\n")[0]
        if (playing == "[playing]") or (playing == "[paused]"):
          volume = mpcstatus.split("\n")[2].split("   ")[0].split(":")[1]
          track = GetMPC("mpc -f %track% current")
          if track == "\n":
            track = mpcstatus.split("\n")[1].replace("  ", " ").split(" ")[1].replace("#","").split("/")[0]
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

        if (playing == "[playing]") or (playing == "[paused]"): # If it is currently playing
          if playing == "[paused]":
            plpause = "PAUSE"
          else:
            plpause = ""
          file = GetMPC("mpc -f %file% current") # Get the current title
          if file.startswith("http"): # if it is a http stream!
            txtLine1 = GetMPC("mpc -f %name% current")
            txtLine2 = GetMPC("mpc -f %title% current")
            txtLine3 = ""
          else: # if it is not a stream
            if currMPC != oldMPC:
              lenLine1 = -1
              lenLine2 = -1
              lenLine3 = -1
              subLine1 = 0
              subLine2 = 0
              subLine3 = 0
              txtLine1 = GetMPC("mpc -f %album% current"  )
              txtLine3 = GetMPC("mpc -f %title% current")
              txtLine2 = GetMPC("mpc -f %artist% current")
          timer = GetMPC("mpc -f %time% current")
          elapsed = mpcstatus.split("\n")[1].split(" ")[4].replace("/0:00","")
          if txtLine2 == "\n":
              if currMPC != oldMPC:
                filename = GetMPC("mpc -f %file% current")
                filename = filename.split(":")[2]
                filename = SetCharacters(filename)
                localfile = filename.split("/")
                txtLine1 = localfile[1]
                txtLine2 = localfile[0]
          if lenLine1 == -1:
            lenLine1 = (len(txtLine1)*widthLetter)-device.width
            if lenLine1 > 0 and lenLine1 < spaceJump:
              lenLine1 = spaceJump + 1
            if lenLine1 < 1:
              lenLine1 = 0
            lenLine2 = (len(txtLine2)*widthLetter)-device.width
            if lenLine2 > 0 and lenLine2 < spaceJump:
              lenLine2 = spaceJump + 1
            if lenLine2 < 1:
              lenLine2 = 0
            lenLine3 = (len(txtLine3)*widthLetter)-device.width
            if lenLine3 > 0 and lenLine3 < spaceJump:
              lenLine3 = spaceJump + 1
            if lenLine3 < 1:
              lenLine3 = 0
            cnt = 0
          if (cnt < lenLine1) and (lenLine1 != 0):
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
          with canvas(device) as draw:
            draw.line((0, line4-2, device.width, line4-2), fill="white")
            draw.line((60, line4-2, 60, device.height), fill="white")
            draw.line((98, line4-2, 98, device.height), fill="white")
            draw.text((103, line4),vol, font=font, fill="white")
            draw.text((0-subLine2, line2),txtLine2, font=font, fill="white")
            draw.text((0-subLine3, line3),txtLine3,font=font, fill="white")
            draw.text((65, line4),"T "+track,font=font, fill="white")
            draw.text((0, line4),elapsed,font=font, fill="white")
            draw.text((0, line4),plpause,font=font, fill="white")
            draw.text((0-subLine1, line1),txtLine1,font=font, fill="white")
          oldMPC = currMPC
          curr_time = datetime.now()
          seconds = curr_time.strftime('%S')
          seconds = int(seconds)%5
          if seconds == 0:
            cnt = cnt + spaceJump
        else:
          oldMPC = currMPC
          ShowImage("cardhand")
      except:
        ShowImage("music")

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass


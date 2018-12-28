#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from time import sleep
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

def ShowImage():
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'music.png'))
    logo = Image.open(img_path).convert("RGBA")
    fff = Image.new(logo.mode, logo.size, (255,) * 4)
    background = Image.new("RGBA", device.size, "black")
    posn = ((device.width - logo.width) // 2, 0)
    img = Image.composite(logo, fff, logo)
    background.paste(img, posn)
    device.display(background.convert(device.mode))

def main(num_iterations=sys.maxsize):
#    welcomeText = "Phoniebox"
#    i = 0
#    while i < len(welcomeText):
#      with canvas(device) as draw:
#        draw.text((12, 29),welcomeText[0:i],font=font, fill="white")
#      sleep(0.1)
#      i += 1
#    sleep(4)
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
        else:
          volume = mpcstatus.split("   ")[0].split(":")[1]
        vol = "Vol."+str(volume)
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
            name = GetMPC("mpc -f %name% current")
            titel = GetMPC("mpc -f %title% current")
            with canvas(device) as draw:
              draw.line((0, 53, device.width, 53), fill="white")
              draw.line((80, 53, 80, device.height), fill="white")
              draw.text((0, 0),name,font=font, fill="white")
              draw.text((0, 12),titel,font=font, fill="white")
              draw.text((0, 54),plpause,font=font, fill="white")
              draw.text((85, 54),vol, font=font, fill="white")
          else: # if it is not a stream
            if currMPC != oldMPC:
              album = GetMPC("mpc -f %album% current"  )
              titel = GetMPC("mpc -f %title% current")
              track = GetMPC("mpc -f %track% current")
              artist = GetMPC("mpc -f %artist% current")
            timer = GetMPC("mpc -f %time% current")
            elapsed = mpcstatus.split("\n")[1].split(" ")[4]
            with canvas(device) as draw:
              draw.line((0, 53, device.width, 53), fill="white")
              draw.line((80, 53, 80, device.height), fill="white")
              draw.text((85, 54),vol, font=font, fill="white")
              draw.text((0, 12),artist, font=font, fill="white")
              draw.text((0, 24),titel,font=font, fill="white")
#              if track != "\n":
#                draw.text((0, 24),"Track "+track,font=font, fill="white")
              draw.text((0, 54),elapsed,font=font, fill="white")
              draw.text((0, 54),plpause,font=font, fill="white")
              draw.text((0, 0),album,font=font, fill="white")
              if artist == "\n":
                if currMPC != oldMPC:
                  filename = GetMPC("mpc -f %file% current")
                  filename = filename.split(":")[2]
                  filename = SetCharacters(filename)
                  localfile = filename.split("/")
                draw.text((0, 0),localfile[1], font=font, fill="white")
                draw.text((0, 12),localfile[0], font=font, fill="white")
          oldMPC = currMPC
        else:
          oldMPC = currMPC
          ShowImage()
      except:
        ShowImage()

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass


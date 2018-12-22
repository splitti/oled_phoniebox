#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from time import sleep
import os
from luma.core.render import canvas
from demo_opts import get_device
from PIL import ImageFont
font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                            'fonts', 'C&C Red Alert [INET].ttf'))
font = ImageFont.truetype(font_path, 12)

def SetCharacters(text):
    chars = {'ö':'oe','ä':'ae','ü':'ue','ß':'ss','Ä':'Ae','Ü':'Ue','Ö':'Oe','%20':' ',' 1/4':'ue'}
    for char in chars:
       text = text.replace(char,chars[char])
    return text

def GetMPC(command):
    from subprocess import check_output
    process = check_output(command.split())
    return process

def main(num_iterations=sys.maxsize):
    device = get_device()
    while num_iterations > 0:
        try:
          num_iterations = 1
          sleep(0.5)
          mpcstatus = GetMPC("mpc status")
          playing = mpcstatus.split("\n")[1].split(" ")[0] #Split to see if mpc is playing at the moment
          file = GetMPC("mpc -f %file% current") # Get the current title
          if (playing == "[playing]") or (playing == "[paused]"): # If it is currently playing
            if file.startswith("http"): # if it is a http stream!
              name = GetMPC("mpc -f %name% current")
              titel = GetMPC("mpc -f %title% current")
              with canvas(device) as draw:
                draw.text((0, 12),titel,font=font, fill="cyan")
            else: # if it is not a stream
              album = GetMPC("mpc -f %album% current"  )
              titel = GetMPC("mpc -f %title% current")
              track = GetMPC("mpc -f %track% current")
              timer = GetMPC("mpc -f %time% current")
              artist = GetMPC("mpc -f %artist% current")
              #playlist = GetMPC("mpc -f %file% playlist")
              elapsed = mpcstatus.split("\n")[1].split(" ")[4]
              #track = "Track: "+track+"   "+elapsed
              if playing == "[paused]":
                plpause = "PAUSE"
              else:
                plpause = ""
              with canvas(device) as draw:
                draw.text((0, 0),artist, font=font, fill="white")
                draw.text((0, 12),titel,font=font, fill="cyan")
                if track == "\n":
                  draw.text((0, 24),elapsed,font=font, fill="cyan")
                  draw.text((0, 24),plpause,font=font, fill="cyan")
                else:
                  draw.text((0, 24),"Track "+track,font=font, fill="cyan")
                  draw.text((55, 24),elapsed,font=font, fill="cyan")
                  draw.text((55, 24),plpause,font=font, fill="cyan")
                draw.text((0, 36),album,font=font, fill="cyan")
                laenge="-"+artist+"-"
                if artist == "\n":
                  filename = GetMPC("mpc -f %file% current")
                  filename = filename.split(":")[2]
                  filename = SetCharacters(filename)
                  draw.text((0, 0),filename, font=font, fill="white")
              #show_message(device, album+"TEST "+titel, fill="white", font=proportional(SINCLAIR_FONT))
          else:
            with canvas(device) as draw:
              draw.text((0, 0),"Karte auflegen...", font=font, fill="white")
        except:
          with canvas(device) as draw:
            draw.text((0, 0),"Houston, wir haben ein", font=font, fill="white")
            draw.text((0, 10),"Problem", font=font, fill="white")
            draw.text((0, 20),"Ruf den Papa :-)", font=font, fill="white") 

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

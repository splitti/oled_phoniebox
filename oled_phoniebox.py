#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# For more details go to https://github.com/splitti/oled_phoniebox/

import signal
import sys
sys.path.append("/home/pi/oled_phoniebox/scripts/")
from o4p_functions import init_config, get_device, get_currcontrast, set_characters, get_mpc, get_wificonn, get_specialinfos, set_newmode
from time import sleep
from datetime import datetime
import os
from luma.core.render import canvas
from PIL import ImageFont, Image

FONT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                            'fonts', 'Bitstream Vera Sans Mono Roman.ttf'))
FONT_STANDARD = ImageFont.truetype(FONT_PATH, 12)
FONT_SMALL = ImageFont.truetype(FONT_PATH, 10)
FONT_MIDTOWER = ImageFont.truetype(FONT_PATH, 42)
FONT_HIGHTOWER = ImageFont.truetype(FONT_PATH, 54)
FONT_PATH_WIFI = os.path.abspath(os.path.join(os.path.dirname(__file__),
                            'fonts', 'WIFI.ttf'))
FONT_WIFI = ImageFont.truetype(FONT_PATH_WIFI, 64)
FONT_WIFI_MIX = ImageFont.truetype(FONT_PATH_WIFI, 48)

CONFFILE = "/home/pi/oled_phoniebox/oled_phoniebox.conf"
TEMPFILE = "/tmp/o4p_overview.temp"
VERSION = "1.9.0 - 20200105"

def showimage(imgname):
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', imgname+'.png'))
    logo = Image.open(img_path).convert("RGBA")
    fff = Image.new(logo.mode, logo.size, (255,) * 4)
    background = Image.new("RGBA", device.size, "black")
    posn = ((device.width - logo.width) // 2, 0)
    img = Image.composite(logo, fff, logo)
    background.paste(img, posn)
    device.display(background.convert(device.mode))

def sigterm_handler(*_):
    # save the state here or do whatever you want
    showimage("poweroff")
    sleep(1)
    sys.exit(0)
    #os._exit(0)

def main(num_iterations=sys.maxsize):
    oldcontrast = get_currcontrast(CONFFILE)
    device.contrast(oldcontrast)
    showimage("music")
    tmpcard = 3
    linepos = 1
    line1 = 4
    line2 = 19
    line3 = 34
    line4org = 49
    line4 = device.height-1-10
    lenline1 = -1
    lenline2 = -1
    lenline3 = -1
    subline1 = 0
    subline2 = 0
    subline3 = 0
    widthletter = 7
    spacejump = 7
    oldmpc = ""
    oldplaying = "-"
    displaytime = 0.5
    oldvol = "FirstStart"
    wificonn = get_wificonn()
    special = 0
    while num_iterations > 0:
        num_iterations = 1
        curr_time = datetime.now()
        seconds = curr_time.strftime('%S')
        sleep(0.8)
        seconds = int(seconds)%5
        if seconds == 0:
            wificonn = get_wificonn()
        try:
        #if wificonn != "BUGFIXING_LINE":
            if (os.path.exists(TEMPFILE)) or (special == 1):
                specialinfos = get_specialinfos()
                if special == 0:
                    special = 1
                    timetoshow = 10
                    os.remove(TEMPFILE)
                with canvas(device) as draw:
                    draw.text((0, line1),  "WLAN: "+specialinfos[0],font=FONT_SMALL, fill="white")
                    draw.text((0, line2),  "IP:   "+specialinfos[1],font=FONT_SMALL, fill="white")
                    draw.text((0, line3),  "Version:",font=FONT_SMALL, fill="white")
                    draw.text((0, line4org),VERSION,font=FONT_SMALL, fill="white")
                    draw.rectangle((device.width-4,0,device.width,device.height/10*timetoshow), outline="white", fill="white")

                    #draw.line((device.width, , device.width, device.height), fill="white")
                    #draw.text((110, line4org),timetoshow,font=FONT_SMALL, fill="white")
                sleep(1)
                timetoshow = timetoshow - 1
                if timetoshow == 0:
                    special = 0
                if os.path.exists(TEMPFILE):
                    timetoshow = 10
                    os.remove(TEMPFILE)
                    newmode = set_newmode(CONFFILE)
                    initvars.set('GENERAL', 'mode', newmode)
                    with canvas(device) as draw:
                        draw.text((0, line1),initvars['GENERAL']['mode'],font=FONT_HIGHTOWER, fill="white")
                    sleep(displaytime)
            else:
                currcontrast = get_currcontrast(CONFFILE)
                if currcontrast != oldcontrast:
                    device.contrast(currcontrast)
                    oldcontrast = currcontrast
                mpcstatus = set_characters(get_mpc("mpc status"))
                playing = mpcstatus.split("\n")[1].split(" ")[0] #Split to see if mpc is playing at the moment
                currmpc = mpcstatus.split("\n")[0]
                if (playing == "[playing]") or (playing == "[paused]"):
                    volume = mpcstatus.split("\n")[2].split("   ")[0].split(":")[1]
                else:
                    volume = mpcstatus.split("   ")[0].split(":")[1]
                vol = "V"+str(volume.replace("%",""))
                if oldplaying != playing:
                    if playing == "[playing]":
                        with canvas(device) as draw:
                            draw.polygon([(49, 10), (79, 32), (49, 54)], outline="white", fill="white")
                        sleep(displaytime)
                    if playing == "[paused]":
                        with canvas(device) as draw:
                            draw.rectangle((51,10,59,54), outline="white", fill="white")
                            draw.rectangle((69,10,77,54), outline="white", fill="white")
                        sleep(displaytime)
                    oldplaying = playing
                volume = int(volume.replace(" ","").replace("%",""))
                if (oldvol != volume) and (oldvol != "FirstStart"):
                    with canvas(device) as draw:
                        draw.rectangle((30,22,45,42), outline="white", fill="white")
                        draw.polygon([(45, 22),(60, 10), (60,54), (45, 42)], outline="white", fill="white")
                        if volume != 0:
                            draw.rectangle((75,28,105,36), outline="white", fill="white")
                            if oldvol < volume:
                                draw.rectangle((86,17,94,47), outline="white", fill="white")
                        else:
                            draw.text((75, 2),"X",font=FONT_HIGHTOWER, fill="white") 
                    sleep(displaytime)
                oldvol = volume
                if (playing == "[playing]") or (playing == "[paused]"):
                    if playing == "[playing]":
                        #timer = set_characters(get_mpc("mpc -f %time% current"))
                        elapsed = mpcstatus.split("\n")[1].replace("  "," ").split(" ")[3]
                    if currmpc != oldmpc:
                        track =   mpcstatus.split("\n")[1].replace("  "," ").split(" ")[1].replace("#","") #set_characters(get_mpc("mpc -f %track% current"))
                        if len(track.split("/")[1]) > 2:
                            track = track.split("/")[0]
                        if track == "\n":
                            track = mpcstatus.split("\n")[1].replace("  ", " ").split(" ")[1].replace("#","") #.split("/")[0]
                        file = set_characters(get_mpc("mpc -f %file% current")) # Get the current title
                        if initvars['GENERAL']['mode'] == "full" :
                            if file.startswith("http"): # if it is a http stream!
                                txtline1 = set_characters(get_mpc("mpc -f %name% current"))
                                txtline2 = set_characters(get_mpc("mpc -f %title% current"))
                                txtline3 = ""
                                track = "--/--"
                            else: # if it is not a stream
                                lenline1 = -1
                                lenline2 = -1
                                lenline3 = -1
                                subline1 = 0
                                subline2 = 0
                                subline3 = 0
                                linepos = 1
                                txtline1 = set_characters(get_mpc("mpc -f %album% current"))
                                txtline3 = set_characters(get_mpc("mpc -f %title% current"))
                                txtline2 = set_characters(get_mpc("mpc -f %artist% current"))
                            if txtline2 == "\n":
                                filename = set_characters(get_mpc("mpc -f %file% current"))
                                filename = filename.split(":")[2]
                                filename = set_characters(filename)
                                localfile = filename.split("/")
                                txtline1 = localfile[1]
                                txtline2 = localfile[0]
                    if initvars['GENERAL']['mode'] == "lite" :
                        if playing != "[paused]":
                            timeline = elapsed.split("/")
                            if not file.startswith("http"):
                                if timeline[1] != "0:00":
                                    elapsed = timeline[1]
                        if not file.startswith("http"):
                            timelinep = int(mpcstatus.split("\n")[1].replace("   "," ").replace("  "," ").split(" ")[3].replace("(","").replace("%)",""))
                            timelinep = device.width * timelinep / 100
                        else:
                            timelinep = device.width 
                            track = "X"
                            xpos_w = device.width/2-38
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
                            if not file.startswith("http"):
                                draw.text((xpos, 4),track,font=FONT_HIGHTOWER, fill="white")
                            else:
                                draw.text((xpos_w, 4),track,font=FONT_WIFI, fill="white")
                            draw.rectangle((0,0,timelinep,1), outline="white", fill="white")
                            draw.rectangle((109, line4+8,111,line4+10), outline=wificonn[0], fill=wificonn[0])
                            draw.rectangle((114, line4+6,116,line4+10), outline=wificonn[1], fill=wificonn[1])
                            draw.rectangle((119, line4+4,121,line4+10), outline=wificonn[2], fill=wificonn[2])
                            draw.rectangle((124, line4+2,126,line4+10), outline=wificonn[3], fill=wificonn[3])
                    if initvars['GENERAL']['mode'] == "mix" :
                        if playing != "[paused]":
                            timeline = elapsed.split("/")
                            if timeline[0] == "(0%)":
                                elapsed = "-:--"
                            elif timeline[1] != "0:00":
                                elapsed = timeline[1]
                            else:
                                elapsed = "-:--"
                            if len(elapsed) == 4:
                                elapsed = "L "+elapsed
                            if len(elapsed) == 5:
                                elapsed = "L"+elapsed
                        else:
                            elapsed = "PAUSE"
                        if not file.startswith("http"):
                            timelinep = int(mpcstatus.split("\n")[1].replace("   "," ").replace("  "," ").split(" ")[3].replace("(","").replace("%)",""))
                            timelinep = device.width * timelinep / 100
                        else:
                            timelinep = device.width
                            xpos_w = device.width/2-28
                            track = "X"
                        tracki = track.replace("\n","")
                        if len(tracki) == 1:
                            tracki = "    "+tracki
                        if len(tracki) == 2:
                            tracki = "   "+tracki
                        if len(tracki) == 3:
                            tracki = "  "+tracki
                        if len(tracki) == 4:
                            tracki = " "+tracki
                        if len(tracki) == 5:
                            tracki = tracki
                        track = track.split("/")[0]
                        if len(track) == 1:
                            xpos = device.width/2-13
                        if len(track) == 2:
                            xpos = device.width/2-26
                        if len(track) == 3:
                            xpos = device.width/2-39
                        if len(track) == 4:
                            xpos = device.width/2-52
                        with canvas(device) as draw:
                            if not file.startswith("http"):
                                draw.line((39, line4-2, 39, device.height), fill="white")
                                draw.text((0, line4),elapsed,font=FONT_SMALL, fill="white")
                                draw.text((42, line4),tracki,font=FONT_SMALL, fill="white")
                                draw.line((0, line4-2, device.width, line4-2), fill="white")
                                draw.text((xpos, 4),track,font=FONT_MIDTOWER, fill="white")
                            else:
                                draw.line((75, line4-2, device.width, line4-2), fill="white")
                                draw.text((xpos_w, 4),track,font=FONT_WIFI_MIX, fill="white")
                            draw.rectangle((0,0,timelinep,1), outline="white", fill="white")
                            draw.rectangle((109, line4+8,111,line4+10), outline=wificonn[0], fill=wificonn[0])
                            draw.rectangle((114, line4+6,116,line4+10), outline=wificonn[1], fill=wificonn[1])
                            draw.rectangle((119, line4+4,121,line4+10), outline=wificonn[2], fill=wificonn[2])
                            draw.rectangle((124, line4+2,126,line4+10), outline=wificonn[3], fill=wificonn[3])
                            draw.line((75, line4-2, 75, device.height), fill="white")
                            draw.line((105, line4-2, 105, device.height), fill="white")
                            draw.text((78, line4),vol,font=FONT_SMALL, fill="white")
                            draw.text((108, line4),"---",font=FONT_SMALL, fill=wificonn[4])
                            #draw.line((device.width/2, 0, device.width/2, device.height), fill="white")
                    if initvars['GENERAL']['mode'] == "full" :
                        if lenline1 == -1:
                            lenline1 = (len(txtline1)*widthletter)-device.width
                            if lenline1 > 0 and lenline1 < spacejump:
                                lenline1 = spacejump
                            if lenline1 < 1:
                                lenline1 = 0
                            lenline2 = (len(txtline2)*widthletter)-device.width
                            if lenline2 > 0 and lenline2 < spacejump:
                                lenline2 = spacejump
                            if lenline2 < 1:
                                lenline2 = 0
                            lenline3 = (len(txtline3)*widthletter)-device.width
                            if lenline3 > 0 and lenline3 < spacejump:
                                lenline3 = spacejump
                            if lenline3 < 1:
                                lenline3 = 0
                            cnt = 0
                        if linepos == 1:
                            if (cnt <= lenline1+spacejump*3) and (lenline1 != 0):
                                subline1 = cnt
                                subline2 = 0
                                subline3 = 0
                            else:
                                linepos = 2
                                cnt = 0-spacejump
                        elif linepos == 2:
                            if (cnt <= lenline2+spacejump*3) and (lenline2 != 0):
                                subline1 = 0
                                subline2 = cnt
                                subline3 = 0
                            else:
                                linepos = 3
                                cnt = 0-spacejump
                        elif  linepos == 3:
                            if (cnt <= lenline3+spacejump*3) and (lenline3 != 0):
                                subline1 = 0
                                subline2 = 0
                                subline3 = cnt
                            else:
                                linepos = 1
                                cnt = 0-spacejump
                    if initvars['GENERAL']['mode'] == "full" :
                        if playing != "[paused]":
                            timeline = elapsed.split("/")
                            if timeline[0] == "(0%)":
                                elapsed = "-:--"
                            elif timeline[1] != "0:00":
                                elapsed = timeline[1]
                            else:
                                elapsed = "-:--"
                            if len(elapsed) == 4:
                                elapsed = "L "+elapsed
                            if len(elapsed) == 5:
                                elapsed = "L"+elapsed
                        else:
                            elapsed = "PAUSE"
                        if not file.startswith("http"):
                            timelinep = int(mpcstatus.split("\n")[1].replace("   "," ").replace("  "," ").split(" ")[3].replace("(","").replace("%)",""))
                            timelinep = device.width * timelinep / 100
                        else:
                            timelinep = device.width
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
                            if not file.startswith("http"):
                                draw.line((39, line4-2, 39, device.height), fill="white")
                                draw.text((0, line4),elapsed,font=FONT_SMALL, fill="white")
                                draw.text((42, line4),track,font=FONT_SMALL, fill="white")
                                draw.line((0, line4-2, device.width, line4-2), fill="white")
                            else:
                                draw.line((75, line4-2, device.width, line4-2), fill="white")
                            draw.rectangle((0,0,timelinep,1), outline="white", fill="white")
                            draw.rectangle((109, line4+8,111,line4+10), outline=wificonn[0], fill=wificonn[0])
                            draw.rectangle((114, line4+6,116,line4+10), outline=wificonn[1], fill=wificonn[1])
                            draw.rectangle((119, line4+4,121,line4+10), outline=wificonn[2], fill=wificonn[2])
                            draw.rectangle((124, line4+2,126,line4+10), outline=wificonn[3], fill=wificonn[3])
                            draw.line((75, line4-2, 75, device.height), fill="white")
                            draw.line((105, line4-2, 105, device.height), fill="white")
                            draw.text((0-subline1, line1),txtline1,font=FONT_STANDARD, fill="white")
                            draw.text((0-subline2, line2),txtline2,font=FONT_STANDARD, fill="white")
                            draw.text((0-subline3, line3),txtline3,font=FONT_STANDARD, fill="white")
                            draw.text((78, line4),vol,font=FONT_SMALL, fill="white")
                            draw.text((108, line4),"---",font=FONT_SMALL, fill=wificonn[4])
                            oldmpc = currmpc
                        cnt = cnt + spacejump
                else:
                    oldmpc = currmpc
                    if tmpcard < 3:
                        sleep(0.5)
                        tmpcard = tmpcard + 1
                    else:
                        showimage("cardhand")
                        tmpcard = 0
        except:
            sleep(0.5)
            showimage("music")

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    initvars = init_config(CONFFILE)
    device = get_device(initvars['GENERAL']['controller'])
    try:
        main()
    except KeyboardInterrupt:
        pass
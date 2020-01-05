#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
sys.path.append("/home/pi/oled_phoniebox/scripts")
import os
from o4p_functions import init_config

CONFFILE = "/home/pi/oled_phoniebox/oled_phoniebox.conf"

def main():
    initvars = init_config(CONFFILE)
    currcontrast = int(initvars['GENERAL']['contrast'])
    if currcontrast < 171 and currcontrast != "":
        initvars.set('GENERAL', 'contrast', str(currcontrast+85))
        with open(CONFFILE, 'w') as configfile:
            initvars.write(configfile)
main()

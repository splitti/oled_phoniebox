#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
sys.path.append("/home/pi/oled_phoniebox/scripts")
import os
from o4p_functions import Init

confFile = "/home/pi/oled_phoniebox/oled_phoniebox.conf"

def main():
 initVars = Init(confFile)
 currContrast = int(initVars['GENERAL']['contrast'])
 if currContrast > 84 and currContrast != "":
  initVars.set('GENERAL', 'contrast', str(currContrast-85))
  with open(confFile, 'w') as configfile:
    initVars.write(configfile)
main()

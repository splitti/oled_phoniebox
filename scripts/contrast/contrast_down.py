#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys,getopt
import os
from time import sleep

ContrastLastFile = "/home/pi/oled_phoniebox/scripts/contrast/contrast.last"

def GetCurrContrast():
    line = ""
    ContrastFile = open(ContrastLastFile)
    ContrastFileContent = ContrastFile.readlines()
    ContrastFile.close()
    for line in ContrastFileContent:
      if "contrast=" in line:
        line = line.split("=")[1].replace("\n","")
        break
    return line

def SetContrast(newContrast,oldContrast):
  with open(ContrastLastFile, 'r') as file :
    filedata = file.read()
  file.close()
  filedata = filedata.replace(str(oldContrast), str(newContrast))
  with open(ContrastLastFile, 'w') as file:
    file.write(filedata)
  file.close()

def main():
 currContrast = int(GetCurrContrast())
 if currContrast > 84 and currContrast != "":
  SetContrast(currContrast-85,currContrast)

main()

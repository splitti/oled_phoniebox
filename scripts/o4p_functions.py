#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
#

def Init(File):
  import configparser
  config = configparser.ConfigParser()
  config.read(File)
  config.sections()
  return config

def get_device(deviceName):
    from luma.core import cmdline, error
    """
    Create device from command-line arguments and return it.
    """
    actual_args = ['-d', deviceName]
    parser = cmdline.create_parser(description='luma.examples arguments')
    args = parser.parse_args(actual_args)
    if args.config:
        # load config from file
        config = cmdline.load_config(args.config)
        args = parser.parse_args(config + actual_args)
    # create device
    try:
        device = cmdline.create_device(args)
    except error.Error as e:
        parser.error(e)
    return device

def GetCurrContrast(File):
  import configparser
  config = configparser.ConfigParser()
  config.read(File)
  config.sections()
  return int(config['GENERAL']['contrast'])

def SetCharacters(text):
    chars = {'ö':chr(246),'ä':chr(228),'ü':chr(252),'ß':chr(223),'Ä':chr(196),'Ü':chr(220),'Ö':chr(214),'%20':' ',' 1/4':chr(252),'%C3%9C':chr(220),'%C3%BC':chr(252),'%C3%84':chr(196),'%C3%A4':chr(228),'%C3%96':chr(214),'%C3%B6':chr(246),'%C3%9F':chr(223)}
    for char in chars:
       text = text.replace(char,chars[char])
    return text

def GetMPC(command):
    from subprocess import check_output
    process = check_output(command.split())
    process = process.decode()
    return process

def GetWifiConn():
  import os
  WifiFile = "/proc/net/wireless"
  first = "black"
  second = "black"
  third = "black"
  fourth = "black"
  alternate = "black"
  try:
    if os.path.exists(WifiFile):
      WifiRateFile = open(WifiFile)
      WifiRate = WifiRateFile.readlines()
      WifiRateFile.close()
      WifiRate = WifiRate[2].replace("   ", " ").replace("  "," ")
      WifiRate = WifiRate.split(" ")
      WifiRate = WifiRate[4].replace(".","")
      if WifiRate[0:1] == "-":
        WifiRate = 100 + float(WifiRate)
      else:
        WifiRate = float(WifiRate)
      if WifiRate > 0:
        first = "white"
      if WifiRate > 30:
        second = "white"
      if WifiRate > 60:
        third = "white"
      if WifiRate > 80:
        fourth = "white"
    else:
      alternate = "white"
  except:
    alternate = "white" 
  return (first,second,third,fourth,alternate)

def GetSpecialInfos():
    from subprocess import check_output
    process = check_output("iwgetid".split())
    process = process.decode()
    wlan = process.split(":")[1].replace('"','').replace('\n','')
    import netifaces as ni
    ni.ifaddresses('wlan0')
    ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    return (wlan, ip)

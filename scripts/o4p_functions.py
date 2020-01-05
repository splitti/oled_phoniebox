#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
# 1.9.0 - 20200105

def init_config(File):
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

def get_currcontrast(File):
    import configparser
    config = configparser.ConfigParser()
    config.read(File)
    config.sections()
    return int(config['GENERAL']['contrast'])

def set_newmode(File):
    import configparser
    config = configparser.ConfigParser()
    config.read(File)
    config.sections()
    if config['GENERAL']['mode'] == "full":
        config.set('GENERAL', 'mode', 'lite')
    elif config['GENERAL']['mode'] == "lite":
        config.set('GENERAL', 'mode', 'mix')
    elif config['GENERAL']['mode'] == "mix":
        config.set('GENERAL', 'mode', 'full')
    with open(File, 'w') as configfile:
        config.write(configfile)
    return config['GENERAL']['mode']

def set_characters(text):
    chars = {'ö':chr(246),'ä':chr(228),'ü':chr(252),'ß':chr(223),'Ä':chr(196),'Ü':chr(220),'Ö':chr(214),'%20':' ',' 1/4':chr(252),'%C3%9C':chr(220),'%C3%BC':chr(252),'%C3%84':chr(196),'%C3%A4':chr(228),'%C3%96':chr(214),'%C3%B6':chr(246),'%C3%9F':chr(223)}
    for char in chars:
        text = text.replace(char,chars[char])
    return text

def get_mpc(command):
    from subprocess import check_output
    process = check_output(command.split())
    process = process.decode()
    return process

def get_wificonn():
    import os
    wififile = "/proc/net/wireless"
    first = "black"
    second = "black"
    third = "black"
    fourth = "black"
    alternate = "black"
    try:
        if os.path.exists(wififile):
            wifirateFile = open(wififile)
            wifirate = wifirateFile.readlines()
            wifirateFile.close()
            wifirate = wifirate[2].replace("   ", " ").replace("  "," ")
            wifirate = wifirate.split(" ")
            wifirate = wifirate[4].replace(".","")
            if wifirate[0:1] == "-":
                wifirate = 100 + float(wifirate)
            else:
                wifirate = float(wifirate)
            if wifirate > 0:
                first = "white"
            if wifirate > 40:
                second = "white"
            if wifirate > 60:
                third = "white"
            if wifirate > 80:
                fourth = "white"
        else:
            alternate = "white"
    except:
        alternate = "white"
    return (first,second,third,fourth,alternate)

def get_specialinfos():
    from subprocess import check_output
    process = check_output("iwgetid".split())
    process = process.decode()
    wlan = process.split(":")[1].replace('"','').replace('\n','')
    import netifaces as ni
    ni.ifaddresses('wlan0')
    ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    return (wlan, ip)


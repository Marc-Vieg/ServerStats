# -*- coding: utf-8 -*-
from configobj import ConfigObj
import botglobalvars as MyGlobals
import os
import time


def loadSettings(path):
    #load settings from file to replace default values in MyGlobals (temporary)
    MyGlobals.sendAlerts = getConfig(path, 'Alerts', 'sendAlerts', 'bool')
    MyGlobals.autoSend = getConfig(path, 'Alerts', 'autoSend', 'bool')
    MyGlobals.autoSendTime = getConfig(path, 'Alerts', 'autoSendTime', 'int')
    MyGlobals.memorythreshold = getConfig(path, 'Graph', 'memth', 'int')
    MyGlobals.usagethreshold = getConfig(path, 'Graph', 'cputh', 'int')
    MyGlobals.GraphicHours = getConfig(path, 'Graph', 'length', 'int')
    MyGlobals.poll = getConfig(path, 'Bot', 'poll', 'int')
    print("settings loaded", MyGlobals.sendAlerts)


def setConfig(path, section, option, value):
    config = ConfigObj(path)
    config[section][option] = value
    print(section, option, value, config[section][option])
    try:
        config.write()
    except:
        print("error writing config file")


def exist(path):
    return os.path.exists(path)


def createConfig(path):
    """
    Create a config file
    """
    config = ConfigObj(path)
    graphSection = {
        'length': 12,
        'cputh': 90,
        'memth': 90
    }
    config['Graph'] = graphSection

    alertSection = {
        'sendAlerts': 1,
        'autoSend': 0,
        'autoSendTime': 30
    }
    config['Alerts'] = alertSection
    botSection = {
        'poll': 10
    }
    config['Bot'] = botSection

    config.write()


def getConfig(path, section, option, type):
    config = ConfigObj(path)
    if type == 'str':
        return config[section][option]
    elif type == 'int':
        return config[section].as_int(option)
    elif type == 'bool':
        #print('bool : ', section, option, config[section].as_bool(option))
        result = config[section].as_bool(option)
        if result:
            return 1
        else:
            return 0

if __name__ == "__main__":
    path = "settings.ini"
    createConfig(path)
    setConfig(path, 'graph', 'length', '60')

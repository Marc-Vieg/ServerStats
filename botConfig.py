# -*- coding: utf-8 -*-
from configobj import ConfigObj
import botglobalvars as MyGlobals
import os


def loadSettings(path):
    #load settings from file to replace default values in MyGlobals
    MyGlobals.alertsEnlabed = getConfig(path, 'Alerts', 'sendAlerts', 'bool')
    MyGlobals.surveillanceActive = getConfig(path, 'Alerts', 'autoSend', 'bool')
    MyGlobals.memorythreshold = getConfig(path, 'Graph', 'memth', 'int')
    MyGlobals.usagethreshold = getConfig(path, 'Graph', 'cputh', 'int')
    MyGlobals.GraphicHours = getConfig(path, 'Graph', 'length', 'int') * 3600


def setConfig(path, section, option, value):
    config = ConfigObj(path)
    config[section][option] = value
    print(section, option, value, config[section][option])
    config.write()


def exist(path):
    return os.path.exists(path)


def createConfig(path):
    """
    Create a config file
    """
    config = ConfigObj(path)
    #
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
        #print((path, ':', section, option, config[section][option]))
        return config[section][option]
    elif type == 'int':
        #print('int : ', section, option, config[section].as_int(option))
        return config[section].as_int(option)
    elif type == 'bool':
        print('bool : ', section, option, config[section].as_bool(option))
        result = config[section].as_bool(option)
        if result:
            return 1
        else:
            return 0
        #return result

if __name__ == "__main__":
    path = "settings.ini"
    createConfig(path)
    setConfig(path, 'graph', 'length', '60')

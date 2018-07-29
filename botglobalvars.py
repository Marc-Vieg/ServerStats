# -*- coding: utf-8 -*-
from datetime import datetime
from telepot.namedtuple import ReplyKeyboardMarkup
import botConfig as config


class MyGlobals(object):

    menu = ['Main', 'Utils', 'Settings']
    currentMenu = ''

    sendAlerts = 0
    autoSend = 0
    autoSendTime = 30
    memorythreshold = 60  # If memory usage more this %
    usagethreshold = 70  # If cpu usage is more than this %
    poll = 10  # seconds
    isEmbyPresent = 0
    isPiholePresent = 0

    LISTSMAX = 864000
    #hours to show in grap (can be 0.5 to 30 minutes for example)
    GraphicHours = 3 * 3600

    Datas = dict()
    Datas['timing'] = []
    Datas['cpu'] = []
    Datas['mem'] = []
    Datas['temp'] = []

    xaxis = []
    xaxiscpu = []
    xaxistemp = []
    settingmemth = []
    settingcputh = []
    setpolling = []
    graphstart = datetime.now()
    shellexecution = []
    myCores = ['Core 0', 'Core 1']

    def createKb():
        print("create kb")
        keyboard=[['Utils', 'Settings'],
                 ['Others', '/who']]
        keyboardrow = []
        if config.getConfig('settings.ini', 'Bot', 'isPiholePresent', 'bool'):
            print("pihole present")
            keyboardrow.append('PiHole')
            keyboard.append(keyboardrow)
        myKeyboard = ReplyKeyboardMarkup(keyboard=keyboard)
        return myKeyboard
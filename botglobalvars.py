# -*- coding: utf-8 -*-
from datetime import datetime
from telepot.namedtuple import ReplyKeyboardMarkup


class MyGlobals(object):

    menu = ['Main', 'Utils', 'Settings']
    currentMenu = ''

    surveillanceActive = False
    memorythreshold = 60  # If memory usage more this %
    usagethreshold = 70  # If cpu usage is more than this %
    poll = 10  # seconds
    pollSurv = 30
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
    alertsEnlabed = True
    mainKeyboard = ReplyKeyboardMarkup(keyboard=[
                     ['Utils', 'Settings'],
                     ['Others'],
                     ['/who']])
    myCores = ['Core 0', 'Core 1']



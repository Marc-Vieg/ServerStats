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
    # I'ld like to make an interval for auto sending graph, maybe later...
    pollSurv = 30
    LISTSMAX = 864000
    #nb d'heures a afficher dans le graphique
    GraphicHours = 3

    Datas = dict()
    #Datas['init'] = datetime.now()
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
    settorrenttype = []
    graphstart = datetime.now()
    shellexecution = []
    #MAINSLEEP = 5
    alertsEnlabed = True
    mainKeyboard = ReplyKeyboardMarkup(keyboard=[
                     ['Utils', 'Settings'],
                     ['Others'],
                     ['/who']])
    myCores = ['Core 0', 'Core 1']



from datetime import datetime
from telepot.namedtuple import ReplyKeyboardMarkup


class MyGlobals(object):

    menu = ['Main', 'Utils', 'Settings']
    currentMenu = ''

    surveillanceActive = False
    memorythreshold = 85  # If memory usage more this %
    usagethreshold = 90  # If cpu usage is more than this %
    poll = 10  # seconds
    pollSurv = 30 # I'ld like to make an interval for auto sending graph, maybe later...
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

    mainKeyboard = ReplyKeyboardMarkup(keyboard=[
                     ['Utils', 'Settings'],
                     ['Others', '/service'],
                     ['/who']])

    myCores = ['Core 0', 'Core 1']




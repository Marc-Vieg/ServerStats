# -*- coding: utf-8 -*-

from configobj import ConfigObj
from datetime import datetime
import os


class BotConfig:
    """
    This is an object to define bot configuration
    """
    def __init__(self, path):
        # Bot informations
        self.path = path

        if not self.exist(self.path):
            self.createConfig()
            self.setConfig('Graph', 'length', '60')

        self.sendAlerts = False
        self.autoSend = False
        self.autoSendTime = 30
        self.memorythreshold = 60  # If memory usage more this %
        self.usagethreshold = 70  # If cpu usage is more than this %
        self.poll = 25200  # seconds (7h)
        self.LISTSMAX = 864000
        # Hours to show in grap (can be 0.5 to 30 minutes for example)
        self.GraphicHours = 3 * 3600
        self.MyIp = '0'
        self.xaxis = []
        self.xaxiscpu = []
        self.xaxistemp = []
        self.settingmemth = []
        self.settingcputh = []
        self.setpolling = []
        self.graphstart = datetime.now()
        self.shellexecution = []
        self.myCores = ['Core 0', 'Core 1']

        # Get sensitive data
        self.TOKEN = ""
        self.adminchatid = []
        self.pihole_passwd = ""

        if self.exist(os.path.dirname(os.path.realpath(__file__))
                      + os.sep
                      + 'tokens.py'):
            import tokens
            self.TOKEN = tokens.telegrambot
            self.adminchatid = tokens.adminchatid
            self.pihole_passwd = tokens.pihole_passwd

    def loadSettings(self):
        # load settings from file to replace default values in MyGlobals
        isRead, sendAlerts = self._getConfig('Alerts', 'sendAlerts', 'bool')
        self.sendAlerts = sendAlerts if isRead else False

        isRead, autoSend = self._getConfig('Alerts', 'autoSend', 'bool')
        self.autoSend = autoSend if isRead else False

        isRead, autoSendTime = self._getConfig('Alerts', 'autoSendTime', 'int')
        self.autoSendTime = autoSendTime if isRead else 30

        isRead, memorythreshold = self._getConfig('Graph', 'memth', 'int')
        self.memorythreshold = memorythreshold if isRead else 60

        isRead, usagethreshold = self._getConfig('Graph', 'cputh', 'int')
        self.usagethreshold = usagethreshold if isRead else 70

        isRead, GraphicHours = self._getConfig('Graph', 'length', 'int')
        self.GraphicHours = GraphicHours if isRead else 3 * 3600

        isRead, poll = self._getConfig('Bot', 'poll', 'int')
        self.poll = poll if isRead else 10

    def _getConfig(self, section, option, type):
        try:
            config = ConfigObj(self.path)
            if type == 'str':
                return True, config[section][option]
            elif type == 'int':
                return True, config[section].as_int(option)
            elif type == 'bool':
                return True, config[section].as_bool(option)
        except Exception:
            return False, None

    def setConfig(self, section, option, value):
        config = ConfigObj(self.path)
        config[section][option] = value

        if section == 'Graph':
            if option == 'length':
                self.GraphicHours = value
            elif option == 'cputh':
                self.usagethreshold = value
            elif option == 'memth':
                self.memorythreshold = value
        elif section == 'Alerts':
            if option == 'sendAlerts':
                self.sendAlerts = value
            elif option == 'autoSendTime':
                self.autoSendTime = value
            elif option == 'autoSend':
                self.autoSend = value
        elif section == 'Bot':
            if option == 'poll':
                self.poll = value

        try:
            config.write()
        except Exception:
            print("Something went wrong while updating the settings file")

    def exist(self, path):
        return os.path.exists(path)

    def createConfig(self):
        """
        Create a config file
        """
        config = ConfigObj(self.path)

        config['Graph'] = {
            'length': 12,
            'cputh': 90,
            'memth': 90
        }
        config['Alerts'] = {
            'sendAlerts': 1,
            'autoSend': 0,
            'autoSendTime': 1800
        }
        config['Bot'] = {
            'poll': 25200,
            'isEmbyPresent': 0,
            'isPiholePresent': 0,
            'otherMenu': 0,
            'myWebSiteMenu': 0,
            'webSiteURL': ""
        }

        try:
            config.write()
        except Exception:
            print("Something went wrong while creating the settings file")

    def getKeyboard(self, itemsList=[], addBackTouch=True):
        """
        This function gives you a specific keyboard
        """
        def chunks(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        keyboard = []
        if itemsList:
            if addBackTouch and "<- back" not in itemsList:
                itemsList.append("<- back")
            for line in chunks(itemsList, 3):
                keyboard.append(line)
        else:
            keyboard = []
        return keyboard

    def isAuthorizedId(self, chat_id):
        return chat_id in self.adminchatid

    def clearall(self, chat_id):
        if chat_id in self.shellexecution:
            self.shellexecution.remove(chat_id)
        if chat_id in self.settingmemth:
            self.settingmemth.remove(chat_id)
        if chat_id in self.setpolling:
            self.setpolling.remove(chat_id)

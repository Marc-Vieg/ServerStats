# -*- coding: utf-8 -*-

from configobj import ConfigObj
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

        self.sendAlerts = True
        self.autoSend = True
        self.autoSendTime = 1800  # seconds (30min)
        self.poll = 25200  # seconds (7h)

        # Get sensitive data
        self.TOKEN = ""
        self.adminchatid = []

        if self.exist(os.path.dirname(os.path.realpath(__file__))
                      + os.sep
                      + 'tokens.py'):
            import tokens
            self.TOKEN = tokens.telegrambot
            self.adminchatid = tokens.adminchatid

    def loadSettings(self):
        # load settings from file to replace default values in MyGlobals
        isRead, sendAlerts = self._getConfig('Alerts', 'sendAlerts', 'bool')
        self.sendAlerts = sendAlerts if isRead else True

        isRead, autoSend = self._getConfig('Alerts', 'autoSend', 'bool')
        self.autoSend = autoSend if isRead else True

        isRead, autoSendTime = self._getConfig('Alerts', 'autoSendTime', 'int')
        self.autoSendTime = autoSendTime if isRead else 1800

        isRead, poll = self._getConfig('Bot', 'poll', 'int')
        self.poll = poll if isRead else 25200

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

        if section == 'Alerts':
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

        config['Alerts'] = {
            'sendAlerts': 1,
            'autoSend': 1,
            'autoSendTime': 1800
        }
        config['Bot'] = {
            'poll': 25200,
        }

        try:
            config.write()
        except Exception:
            print("Something went wrong while creating the settings file")

    def isAuthorizedId(self, chat_id):
        return chat_id in self.adminchatid

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

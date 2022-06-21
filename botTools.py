# -*- coding: utf-8 -*-

import os


class BotTools:
    """
    This is a tools box object, which defines all method
    used by the bot.

    All method should return :

    - A boolean for the method status :
        * True if all is okay
        * False if error raised

    - A string or a tuple, for the result of the method:
        * tuple contains mainly a picture result on first item,
        and a boolean to indicate this is a send Picture instead of a
        send Message
    """
    def __init__(self, botConfig, botData):
        # self.bot = telepot.Bot(botConfig.TOKEN)
        self.botConfig = botConfig
        self.botData = botData
        self.sendPicture = True

# ############ Tools #############

    def example1(self):
        try:
            return True, "OK"
        except Exception:
            return False, "KO"

    def example2(self):
        try:
            path = os.path.abspath(os.path.dirname(__file__))
            return True, (open(path + '/docs/last2Hours.jpg', 'rb'),
                          self.sendPicture)
        except Exception:
            return False, "KO"

    def example3(self, value):
        try:
            return True, str(value)
        except Exception:
            return False, "KO"

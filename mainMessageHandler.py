# -*- coding: utf-8 -*-

from json import load
from pathlib import Path
from telepot.namedtuple import ReplyKeyboardMarkup
import telepot
import telepot.aio.helper


class MainMessageHandler(telepot.aio.helper.ChatHandler):
    """
    Message handler to run and reply to your command
    """
    def __init__(self, seed_tuple, botConfig, botData, botTools, **kwargs):
        super(MainMessageHandler, self).__init__(seed_tuple, **kwargs)
        self.botConfig = botConfig
        self.botData = botData
        self.botTools = botTools
        self.jsonConfig = None
        if not hasattr(self, 'actualSelection'):
            self.initializeHandlers()
        self.keyboardToSend = []
        self.actualMenu, self.lastMenu = [], []
        self.msgToSend, self.nextFunctionToCall = "", ""

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.isPictureToSend = False

        # Text messages
        if (content_type == 'text'
           and self.botConfig.isAuthorizedId(chat_id)):
            # Enter main menu
            if msg['text'] == "/start":
                self.msgToSend = "Welcome on board with MonitoBot\r \
                    What can I do for you ?"
                self.getMenu(self.jsonConfig)
                self.keyboardToSend = self.botConfig.getKeyboard(
                    self.actualMenu,
                    addBackTouch=False
                )

            if self.nextFunctionToCall:
                isOK, result = self.getFunction(
                    self.nextFunctionToCall,
                    msg['text']
                )

                if isinstance(result, tuple):
                    self.msgToSend, self.isPictureToSend = result

                if isinstance(result, str):
                    self.msgToSend = result

                if isOK:
                    self.nextFunctionToCall = ""

            else:
                if msg['text'] in self.actualMenu:
                    if msg['text'] == "<- back":
                        needBackOption = not (self.actualSelection
                                              in self.jsonConfig.keys())
                        self.getMenu(
                            self.jsonConfig,
                            back=True
                        )
                        self.msgToSend = "back"
                        self.keyboardToSend = self.botConfig.getKeyboard(
                            self.actualMenu,
                            needBackOption
                        )
                    else:
                        self.msgToSend = f"{msg['text']} menu"
                        self.getMenu(
                            self.jsonConfig,
                            msg['text']
                        )
                        self.keyboardToSend = self.botConfig.getKeyboard(
                            self.actualMenu
                        )
                else:
                    self.msgToSend = "Welcome on board with MonitoBot\r \
                        What can I do for you ?"
                    self.getMenu(self.jsonConfig)
                    self.keyboardToSend = self.botConfig.getKeyboard(
                        self.actualMenu,
                        addBackTouch=False
                    )

            if self.msgToSend:
                if self.isPictureToSend:
                    self.isPictureToSend = False
                    await self.sender.sendPhoto(self.msgToSend)
                else:
                    await self.sender.sendMessage(
                        text=self.msgToSend,
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=self.keyboardToSend
                        ),
                        disable_web_page_preview=True
                    )

    def initializeHandlers(self):
        """
        Load menu from JSON file
        """
        parentPath = str(Path(__file__).parent)
        try:
            with open(parentPath + "/menu.json") as jsonFile:
                self.jsonConfig = load(jsonFile)
        except Exception:
            self.msgToSend = "Cannot read menu.json file"

    def getMenu(self, jsonConfig, key=None, back=None):
        """
        Get a menu that navigate on json file and return a list of items
        This is a recursive method
        """
        if back:
            self.updateMenu(back=back)
        else:
            if key:
                for item in jsonConfig:
                    if isinstance(jsonConfig[item], dict):
                        if item == key:
                            list_menu = list(jsonConfig)
                            list_menu.extend(list(jsonConfig[item]))
                            if 'function' not in list_menu:
                                self.actualSelection = item

                            if 'function' in jsonConfig[item]:  # function
                                result = ""
                                if 'waiting values' in jsonConfig[item]:
                                    self.nextFunctionToCall = jsonConfig[item]
                                    result = jsonConfig[item]['waiting values']
                                else:
                                    isOK, result = self.getFunction(
                                        jsonConfig[item]
                                    )

                                if isinstance(result, tuple):
                                    self.msgToSend, self.isPictureToSend = result

                                if isinstance(result, str):
                                    self.msgToSend = result

                                self.updateMenu(
                                    list(jsonConfig.keys()),
                                    back
                                )
                            else:
                                self.updateMenu(
                                    list(jsonConfig[item].keys()),
                                    back
                                )
                        else:
                            if jsonConfig[item]:  # check not empty
                                self.getMenu(jsonConfig[item], key)
                            else:
                                continue
                    else:
                        continue
            else:
                if hasattr(self, 'actualSelection'):  # get actual menu
                    self.getMenu(jsonConfig, self.actualSelection)
                else:  # or return default menu
                    self.updateMenu(list(self.jsonConfig.keys()))

    def updateMenu(self, menu=None, back=None):
        """
        Add or remove '<- back' item
        """
        if back:
            if '<- back' in self.actualMenu:
                self.actualMenu.remove('<- back')
            if '<- back' in self.lastMenu:
                self.lastMenu.remove('<- back')
            tmp_menu = self.actualMenu
            self.actualMenu = self.lastMenu
            self.lastMenu = tmp_menu
        else:
            if '<- back' in self.actualMenu:
                self.actualMenu.remove('<- back')
            if '<- back' in self.lastMenu:
                self.lastMenu.remove('<- back')

            if self.actualMenu != menu:
                self.lastMenu = self.actualMenu
                self.actualMenu = menu

    def getFunction(self, function, args=""):
        """
        get and run function defined in json file
        """
        result = ""
        try:
            functionName = list(function['function'].keys())[0]
            items = function['function'][functionName].keys()

            # TODO: need to improve this part
            if 'args' in items:
                arguments = function['function'][functionName]['args']
            else:
                arguments = None

            if args:
                arguments[list(arguments.items())[0][0]] = args

        except KeyError:
            return f"There is no {functionName} function"

        methodToCall = getattr(self.botTools, functionName)

        if arguments:
            isOK, result = methodToCall(**arguments)
        else:
            isOK, result = methodToCall()

        return isOK, result

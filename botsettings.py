# -*- coding: utf-8 -*-
from telepot.namedtuple import ReplyKeyboardMarkup
from botglobalvars import MyGlobals
import botConfig as config

submenus = ['settinghoursth', 'setmem',
            'settingmemth', 'setcpu',
            'settingcputh', 'setpoll',
            'settingpollth']

myKeyboard = ReplyKeyboardMarkup(keyboard=[
    ['setmem', 'setcpu'],
    ['setpoll', 'Alerts On/Off'],
    ['Graph Length'],
    ['<- RETOUR']])

setKeyboard = ReplyKeyboardMarkup(keyboard=[
    ['70', '80'],
    ['Cancel']])

setPollKeyboard = ReplyKeyboardMarkup(keyboard=[
    ['10', '30'],
    ['60', '300'],
    ['Cancel']])

sethoursKeyboard = ReplyKeyboardMarkup(keyboard=[
    ['1', '2'],
    ['3', '6'],
    ['12', '24'],
    ['Cancel']])


def setgraphichours(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    MyGlobals.currentMenu = 'settinghoursth'
    bot.sendMessage(chat_id,
                    "How many hours to show in graphic ?",
                    reply_markup=sethoursKeyboard)


def settinggraphichours(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    if msg['text'] == 'Cancel':
        MyGlobals.currentMenu = 'Settings'
        bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
    else:
        try:
            if float(msg['text']) < 100 * 3600:
                config.setConfig('settings.ini', 'Graph', 'length',
                    round(float(msg['text']) * 3600))
                config.loadSettings('settings.ini')
                bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
                MyGlobals.currentMenu = 'Settings'
            else:
                1 / 0
        except:
            bot.sendMessage(chat_id,
                            "Please send a proper numeric value below 49 hours")


def setmem(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    MyGlobals.settingmemth.append(chat_id)
    bot.sendMessage(chat_id,
                    "Send me a new memory threshold to monitor?",
                    reply_markup=setKeyboard)
    MyGlobals.currentMenu = 'settingmemth'


def settingmemth(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    if msg['text'] == 'Cancel':
        MyGlobals.currentMenu = 'Settings'
        bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
    else:
        try:
            if int(msg['text']) < 100:
                config.setConfig('settings.ini', 'Graph', 'memth',
                            int(msg['text']))
                config.loadSettings('settings.ini')
                bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
                MyGlobals.currentMenu = 'Settings'
            else:
                1 / 0
        except:
            bot.sendMessage(chat_id,
                            "Please send a proper numeric value below 100.")


#cpu usage alert
def setcpu(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    MyGlobals.currentMenu = 'settingcputh'
    bot.sendMessage(chat_id,
                    "Send me a new cpu usage threshold to monitor?",
                    reply_markup=setKeyboard)


def settingcputh(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    if msg['text'] == 'Cancel':
        MyGlobals.currentMenu = 'Settings'
        bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
    else:
        try:
            if int(msg['text']) < 100:
                config.setConfig('settings.ini', 'Graph', 'cputh',
                            int(msg['text']))
                config.loadSettings('settings.ini')
                bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
                MyGlobals.currentMenu = 'Settings'
            else:
                1 / 0
        except:
            bot.sendMessage(chat_id,
                            "Please send a proper numeric value below 100.")


def setpoll(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    MyGlobals.currentMenu = 'settingpollth'
    bot.sendMessage(chat_id,
                    "Send me a new polling interval in seconds? (>= 10)",
                     reply_markup=setPollKeyboard)


def settingpollth(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    if msg['text'] == 'Cancel':
        MyGlobals.currentMenu = 'Settings'
        bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
    else:
        try:
            if int(msg['text']) >= 10:
                config.setConfig('settings.ini', 'Bot', 'poll',
                            int(msg['text']))
                config.loadSettings('settings.ini')
                bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
                MyGlobals.currentMenu = 'Settings'
            else:
                1 / 0
        except:
            bot.sendMessage(chat_id,
                            "Please send a proper numeric value >= 10")


def Alerts(bot, chat_id):
    bot.sendChatAction(chat_id, 'typing')
    #botconfig is not recognizing the string 'True' as boolean 1, it recognise 'true'...
    if MyGlobals.sendAlerts:
        config.setConfig('settings.ini', 'Alerts', 'sendAlerts', 0)
    else:
        config.setConfig('settings.ini', 'Alerts', 'sendAlerts', 1)
    MyGlobals.sendAlerts = config.getConfig('settings.ini',
                                'Alerts', 'sendAlerts', 'bool')
    if MyGlobals.sendAlerts:
        bot.sendMessage(chat_id,
                        "I'll send Alerts'",
                         disable_web_page_preview=True)
    else:
        bot.sendMessage(chat_id,
                        "I won't send Alerts",
                        disable_web_page_preview=True)


def main(bot, TOKEN, chat_id, msg):
    if msg['text'] == 'Settings':
        bot.sendMessage(chat_id,
                        str("Welcome to settings"),
                        reply_markup=myKeyboard)
        MyGlobals.currentMenu = 'Settings'
    elif msg['text'] == 'setmem':
        setmem(bot, chat_id, msg)
    elif MyGlobals.currentMenu == 'settingmemth':
        settingmemth(bot, chat_id, msg)
    elif msg['text'] == "setcpu" and MyGlobals.currentMenu == 'Settings':
        setcpu(bot, chat_id, msg)
    elif MyGlobals.currentMenu == 'settingcputh':
        settingcputh(bot, chat_id, msg)
    #set graph interval
    elif msg['text'] == 'setpoll' and MyGlobals.currentMenu == 'Settings':
        setpoll(bot, chat_id, msg)
    elif MyGlobals.currentMenu == 'settingpollth':
        settingpollth(bot, chat_id, msg)
    elif (msg['text'] == 'Graph Length'
          and MyGlobals.currentMenu == 'Settings'):
        setgraphichours(bot, chat_id, msg)
    elif MyGlobals.currentMenu == 'settinghoursth':
        settinggraphichours(bot, chat_id, msg)
    elif msg['text'] == 'Alerts On/Off':
        Alerts(bot, chat_id)
    elif msg['text'] == '<- RETOUR':
        MyGlobals.currentMenu = 'Main'
        bot.sendMessage(chat_id,
                        "Back to menu",
                        reply_markup=MyGlobals.mainKeyboard)
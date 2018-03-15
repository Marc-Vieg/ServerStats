# -*- coding: utf-8 -*-
from tokens import *
import botutils
from botglobalvars import MyGlobals
import botsettings as settings
import psutil
from subprocess import Popen, PIPE, STDOUT
import othersmenu
import time
import telepot
import botDatas
import botConfig as config



def FlushData(bot, chat_id):
    botDatas.Datas['timing'] = []
    botDatas.Datas['cpu'] = []
    botDatas.Datas['mem'] = []
    botDatas.Datas['temp'] = []
    bot.sendMessage(chat_id, "datas nettoyées")


stopmarkup = {'keyboard': [['Stop']]}
mainKeyboard = MyGlobals.mainKeyboard
hide_keyboard = {'hide_keyboard': True}


def clearall(chat_id):
    if chat_id in MyGlobals.shellexecution:
        shellexecution.remove(chat_id)
    if chat_id in MyGlobals.settingmemth:
        settingmemth.remove(chat_id)
    if chat_id in MyGlobals.setpolling:
        setpolling.remove(chat_id)
    if chat_id in MyGlobals.settorrenttype:
        settorrenttype.remove(chat_id)


class YourBot(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(YourBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        self._message_with_inline_keyboard = None

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        # Do your stuff according to `content_type` ...
        print(("Your chat_id:" + str(chat_id) + "chat_type : "
               + str(chat_type)))  # this will tell you your chat_id
        if chat_id in adminchatid:  # Store adminchatid variable in tokens.py
            #Text messages
            if content_type == 'text':
                if msg['text'] == '<- RETOUR':
                    bot.sendMessage(chat_id, "retour au menu principal",
                                    reply_markup=mainKeyboard)
                    MyGlobals.currentMenu = 'Main'
                elif ((MyGlobals.currentMenu == 'Settings')
                       or (MyGlobals.currentMenu in settings.submenus)):
                        settings.main(bot, TOKEN, chat_id, msg)
                elif ((msg['text'] == 'Others')
                       or (MyGlobals.currentMenu == 'Others')):
                    othersmenu.main(bot, chat_id, msg)
                elif ((msg['text'] == "Utils")
                       or (MyGlobals.currentMenu == 'Utils')):
                    botutils.main(bot, TOKEN, chat_id, msg)
                elif msg['text'] == 'FLUSH':
                    FlushData(bot, chat_id)
                elif msg['text'] == "Stop":
                    clearall(chat_id)
                    bot.sendMessage(chat_id,
                                    "All operations stopped.",
                                    reply_markup=mainKeyboard)
                #See if there is someone sshing the server
                elif msg['text'] == "/who":
                    p = Popen('telegram-send "`w`"',
                              shell=True, stdin=PIPE,
                              stdout=PIPE, stderr=STDOUT, close_fds=True)
                    output = p.stdout.read()
                    if output == b'':
                        bot.sendMessage(chat_id, "y'a un souci",
                                        disable_web_page_preview=True)
                #I like Fortunes
                elif msg['text'] == "/fortune":
                    p = Popen('fortune', shell=True,
                              stdin=PIPE, stdout=PIPE,
                              stderr=STDOUT, close_fds=True)
                    output = p.stdout.read()
                    bot.sendMessage(chat_id, output, reply_markup=mainKeyboard)
                #memory % limit for the alerts
                elif (msg['text'] == 'Settings'
                      or MyGlobals.currentMenu == 'Settings'):
                    settings.main(bot, TOKEN, chat_id, msg)
                elif chat_id in MyGlobals.shellexecution:
                    bot.sendChatAction(chat_id, 'typing')
                    bot.sendMessage(chat_id, "voila",
                                    disable_web_page_preview=True)
                elif msg['text'] == '<- RETOUR':
                    bot.sendMessage(chat_id, "retour au menu principal",
                                    reply_markup=mainKeyboard)


TOKEN = telegrambot
bot = YourBot(TOKEN)
bot.message_loop()


def main():
    if botDatas.charges():
        for adminid in adminchatid:
            bot.sendMessage(adminid, "dataset Chargé !")
        print("dataset chargé")
        print("controle : \n timing : "
              + str(len(botDatas.Datas['timing']))
              + "\n cpu : "
              + str(len(botDatas.Datas['cpu'])))
        print("\n mem : "
              + str(len(botDatas.Datas['mem']))
              + "\n temp : "
              + str(len(botDatas.Datas['temp'])))

    else:
        for adminid in adminchatid:
            bot.sendMessage(adminid, "erreur de chargement du dataset")
    MyGlobals.currentMenu = 'Main'
    for adminid in adminchatid:
        bot.sendMessage(adminid, "Demarrage de Main", reply_markup=mainKeyboard)
    tr = 0
    # Keep the program running.
    while 1:
        if tr == MyGlobals.poll:
            if MyGlobals.autoSend:
                for adminid in adminchatid:
                    bot.sendChatAction(adminid, 'typing')
                    botutils.memgraph(bot, adminid, 'all')
                    bot.sendMessage(adminid,
                                    "rapport de surveillance toutes les "
                                    + str(MyGlobals.poll) + " secondes")
            tr = 0
            memck = psutil.virtual_memory()
            mempercent = memck.percent
            usagepercent = psutil.cpu_percent(0.5)

            #on entretiens la liste des utilisations proc
            temperatures = botutils.recupTemp()
            z = 0
            somme = 0
            for core in MyGlobals.myCores:
                z += 1
                somme += temperatures[core]
            tempMoyenne = somme / z
            botDatas.appendData(usagepercent, mempercent, tempMoyenne)

            ##alert if memory is low
            if ((mempercent > MyGlobals.memorythreshold)
                                and MyGlobals.sendAlerts):
                memavail = "Available memory: %.2f GB" \
                           % (memck.available / 1000000000)
                for adminid in adminchatid:
                    bot.sendMessage(adminid, "CRITICAL! LOW MEMORY!\n"
                                    + memavail + '\n' + str(mempercent)
                                    + '% of memory used')
                    botutils.memgraph(bot, adminid, 'all')
            ##alert if cpu usage percent is high
            if ((usagepercent > MyGlobals.usagethreshold)
                                and MyGlobals.sendAlerts):
                for adminid in adminchatid:
                    bot.sendMessage(adminid, "CRITICAL! HIGH CPU!\n"
                                    + str(usagepercent) + '% of cpu used')
                    botutils.memgraph(bot, adminid, 'all')
        botDatas.save()
        time.sleep(10)  # 10 seconds
        tr += 10

# -*- coding: utf-8 -*-
from tokens import *
import botutils
from botglobalvars import MyGlobals
import botsettings as settings
import psutil
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
import othersmenu
import collections
import time
import telepot
import botpersist as persist


def FlushData(bot, chat_id):
    MyGlobals.Datas['timing'] = []
    MyGlobals.Datas['cpu'] = []
    MyGlobals.Datas['mem'] = []
    MyGlobals.Datas['temp'] = []
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
    if persist.Charges():
        for adminid in adminchatid:
            bot.sendMessage(adminid, "dataset Chargé !")
        print("dataset chargé")
        print("controle : \n timing : "
              + str(len(MyGlobals.Datas['timing']))
              + "\n cpu : "
              + str(len(MyGlobals.Datas['cpu'])))
        print("\n mem : "
              + str(len(MyGlobals.Datas['mem']))
              + "\n temp : "
              + str(len(MyGlobals.Datas['temp'])))
        print(str(MyGlobals.Datas))

    else:
        for adminid in adminchatid:
            bot.sendMessage(adminid, "erreur de chargement du dataset")
    MyGlobals.currentMenu = 'Main'
    for adminid in adminchatid:
        bot.sendMessage(adminid, "Demarrage de Main", reply_markup=mainKeyboard)
    tr = 0
    xx = 0
    xxx = 0
    xxtemp = 0
    # Keep the program running.
    while 1:
        if tr == MyGlobals.poll:
            if len(MyGlobals.Datas['timing']) > MyGlobals.LISTSMAX:
                pollq = collections.deque(MyGlobals.Datas['timing'])
                pollq.append(MyGlobals.poll)
                pollq.popleft()
                MyGlobals.Datas['timing'] = pollq
                MyGlobals.Datas['timing'] = list(MyGlobals.Datas['timing'])
            else:
                MyGlobals.Datas['timing'].append(MyGlobals.poll)
            #send graph if autosend
            if MyGlobals.surveillanceActive:
                for adminid in adminchatid:
                    bot.sendChatAction(adminid, 'typing')
                    tmperiod = "Last %.2f hours"\
                               % ((datetime.now()
                               - MyGlobals.graphstart).total_seconds() / 3600)
                    bot.sendPhoto(adminid,
                        botutils.plotbiggraph(MyGlobals.Datas,
                                              MyGlobals.xaxis, tmperiod))
                    bot.sendMessage(adminid,
                                    "rapport de surveillance toutes les "
                                    + str(MyGlobals.poll) + " secondes")
            tr = 0
            memck = psutil.virtual_memory()
            mempercent = memck.percent
            usagepercent = psutil.cpu_percent(0.5)
            #on entretiens la liste des memoires
            if len(MyGlobals.Datas['mem']) > MyGlobals.LISTSMAX:
                memq = collections.deque(MyGlobals.Datas['mem'])
                memq.append(mempercent)
                memq.popleft()
                MyGlobals.Datas['mem'] = memq
                MyGlobals.Datas['mem'] = list(MyGlobals.Datas['mem'])
            else:
                MyGlobals.xaxis.append(xx)
                xx += 1
                MyGlobals.Datas['mem'].append(mempercent)
            #on entretiens la liste des utilisations proc
            if len(MyGlobals.Datas['cpu']) > MyGlobals.LISTSMAX:
                usageq = collections.deque(MyGlobals.Datas['cpu'])
                usageq.append(usagepercent)
                usageq.popleft()
                MyGlobals.Datas['cpu'] = usageq
                MyGlobals.Datas['cpu'] = list(MyGlobals.Datas['cpu'])
            else:
                MyGlobals.xaxiscpu.append(xxx)
                xxx += 1
                MyGlobals.Datas['cpu'].append(usagepercent)
            #on entretiens la liste des temperatures
            temperatures = botutils.recupTemp()
            z = 0
            somme = 0
            for core in MyGlobals.myCores:
                z += 1
                somme += temperatures[core]
            tempMoyenne = somme / z
            #print("temp moyenne : %d" % tempMoyenne)
            if len(MyGlobals.Datas['temp']) > MyGlobals.LISTSMAX:
                tempq = collections.deque(MyGlobals.Datas['temp'])
                tempq.append(tempMoyenne)
                tempq.popleft()
                MyGlobals.Datas['temp'] = tempq
                MyGlobals.Datas['temp'] = list(MyGlobals.Datas['temp'])
            else:
                MyGlobals.xaxistemp.append(xxx)
                xxtemp += 1
                MyGlobals.Datas['temp'].append(tempMoyenne)
            #alerte si memoire faible
            if (mempercent > MyGlobals.memorythreshold
                and MyGlobals.alertsEnlabed is True):
                memavail = "Available memory: %.2f GB" \
                           % (memck.available / 1000000000)
                timep = 0
                for i in range(0, len(MyGlobals.Datas['timing'])):
                    timep += MyGlobals.Datas['timing'][i]
                if timep < 60:
                    tmperiod = " last %d secondes" % time
                if timep >= 60 and timep < 3600:
                    tmperiod = " last %d minutes" % (time / 60)
                if timep >= 3600:
                    tmperiod = " last " + str(MyGlobals.GraphicHours)\
                             + " hours"
                for adminid in adminchatid:
                    bot.sendMessage(adminid, "CRITICAL! LOW MEMORY!\n"
                                    + memavail + '\n' + str(mempercent)
                                    + '% of memory used')
                    bot.sendPhoto(adminid,
                        botutils.plotbiggraph(MyGlobals.Datas,
                                              MyGlobals.xaxis, tmperiod))
            #alerte si proc surchargé
            if (usagepercent > MyGlobals.usagethreshold
                and MyGlobals.alertsEnlabed is True):
                timep = 0
                for i in range(0, len(MyGlobals.Datas['timing'])):
                    timep += MyGlobals.Datas['timing'][i]
                if timep < 60:
                    tmperiod = " last %d secondes" % timep
                if timep >= 60 and timep < 3600:
                    tmperiod = " last %d minutes" % (timep / 60)
                if timep >= 3600:
                    tmperiod = " last " + str(MyGlobals.GraphicHours) + " hours"
                for adminid in adminchatid:
                    bot.sendMessage(adminid, "CRITICAL! HIGH CPU!\n"
                                    + str(usagepercent) + '% of cpu used')
                    bot.sendPhoto(adminid,
                            botutils.plotbiggraph(MyGlobals.Datas,
                                                  MyGlobals.xaxis,
                                                  tmperiod))
        persist.save()
        time.sleep(10)  # 10 seconds
        tr += 10

# -*- coding: utf-8 -*-
from telepot.namedtuple import ReplyKeyboardMarkup
from botglobalvars import MyGlobals
import os
import time
import shlex
import subprocess
from subprocess import Popen, PIPE, STDOUT
startupScript = '/usr/sbin/serverstatsbot.sh'

myKeyboard = ReplyKeyboardMarkup(keyboard=[
    ['Compile LineageOs'],
    ['Status', 'Restart Bot'],
    ['<- RETOUR']])


 #TODO: compile :don't send x alerts of cpu when compiling, I know it's hard
def compile(bot, chat_id):
    buildScript = dict()
    buildScript['path'] = '/home/build/buildScript'
    buildScript['name'] = 'buildscript.sh'
    command_line = str("sudo -i -u build . "
                   + buildScript['path'] + "/"
                   + buildScript['name'] + " > /tmp/lastCompilation.log")
    p = Popen(command_line, shell=True, stdin=PIPE, stderr=STDOUT, stdout=PIPE, close_fds=True)


#cpu usage alert
def restartBot(bot, chat_id, msg):
    MyGlobals.currentMenu = 'Restarting'
    bot.sendMessage(chat_id, "le bot redemarre", reply_markup=myKeyboard)
    command_line = str(startupScript + " start")
    args = shlex.split(command_line)
    pid = os.fork()
    if pid:
        print ("i am children ! restartin in 2 s")
        subprocess.Popen(args)
        time.sleep(5)
        os._exit(1)
    else:
        print("i am fatcher, retiring..")
        os._exit(0)


def compilStatus(bot, chat_id):
    command_line = str("tail -n5 /tmp/lastCompilation.log")
    p = Popen(command_line, shell=True, stdin=PIPE,
              stderr=STDOUT, stdout=PIPE, close_fds=True)
    output = p.stdout.read()
    bot.sendMessage(chat_id, output)


def main(bot, chat_id, msg):
    print((str("je suis dans " + __name__)))
    if msg['text'] == 'Others':
        bot.sendMessage(chat_id, str("fonctionalités diverses "),
                        reply_markup=myKeyboard)
        MyGlobals.currentMenu = 'Others'
    if (msg['text'] == 'Restart Bot'
        and MyGlobals.currentMenu == 'Others'):
        restartBot(bot, chat_id, msg)
    elif (msg['text'] == 'Compile LineageOs'
          and MyGlobals.currentMenu == 'Others'):
        if MyGlobals.isCompillinlling is False:
            if compile(bot, chat_id):
                bot.sendMessage(chat_id,
                                str("compilation lancée en processus enfant"),
                                reply_markup=myKeyboard)
            else:
                bot.sendMessage(chat_id,
                                str("il y a eu un probleme en lancant la"
                                + " compilation en processus enfant"),
                                reply_markup=myKeyboard)
        else:
            bot.sendndMessage(chat_id, "Une compillation est deja en cours !")
    elif (msg['text'] == 'Status'
          and MyGlobals.currentMenu == 'Others'):
            compilStatus(bot, chat_id)
    elif msg['text'] == '<- RETOUR':
        MyGlobals.currentMenu = 'Main'
        bot.sendMessage(chat_id,
                        "retour au menu principal",
                        reply_markup=MyGlobals.mainKeyboard)

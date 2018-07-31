# -*- coding: utf-8 -*-
import json
import time
import os
if __name__ != "__main__":
    from urllib.request import urlopen
from telepot.namedtuple import ReplyKeyboardMarkup
from botglobalvars import MyGlobals

url = "http://pi.hole/admin"

status_check = "%s/api.php?status" % url

summary_today = "%s/api.php?summary" % url

myKeyboard = ReplyKeyboardMarkup(keyboard=[
    ['Stats'],
    ['<- Back']])




def nativejson(data):
    return json.loads(data)


def request(input_url, method='GET'):
    response = urlopen(input_url)
    return nativejson(response.read().decode('utf-8'))


def check_status():
    response = request(status_check)
    return 'PiHole is ' + response['status']


def get_summary():
    response = request(summary_today)
    summary = 'Status: ' + response['status'] + '\n' + \
            'Domains being blocked: ' + response['domains_being_blocked'] + '\n' + \
            'Total Queries today: ' + response['dns_queries_today'] + '\n' + \
            'Ads blocked today: ' + response['ads_blocked_today'] + '\n' + \
            'Queries Blocked: ' + response['ads_percentage_today'] + '%'
    return summary


def main(bot, chat_id, msg):
    print((str("je suis dans " + __name__)))
    MyGlobals.currentMenu = 'pihole'
    if msg['text'] == 'PiHole':
        bot.sendMessage(chat_id, "Pi Hole :", reply_markup=myKeyboard)
    #if (msg['text'] == 'Status'
        #and MyGlobals.currentMenu == 'pihole'):
        #bot.sendMessage(chat_id, check_status(), reply_markup=myKeyboard)
    if (msg['text'] == 'Stats'
        and MyGlobals.currentMenu == 'pihole'):
        bot.sendMessage(chat_id, get_summary(), reply_markup=myKeyboard)
    elif msg['text'] == '<- Back':
        MyGlobals.currentMenu = 'Main'
        bot.sendMessage(chat_id, "Main Menu :",
                        reply_markup=MyGlobals.mainKeyboard)
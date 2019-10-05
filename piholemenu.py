# -*- coding: utf-8 -*-
import json
import time
import os
if __name__ != "__main__":
    from urllib.request import urlopen
from telepot.namedtuple import ReplyKeyboardMarkup
from botglobalvars import MyGlobals
import pihole as ph
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

url = "http://pi.hole/admin"
pihole = ph.PiHole("pi.hole")

pihole.refresh()
pihole.getVersion()
#connection with pihole seems ok

status_check = "%s/api.php?status" % url

summary_today = "%s/api.php?summary" % url

myKeyboard = ReplyKeyboardMarkup(keyboard=[
    ['Stats'],['Update ?'],['Graph'],
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
    
def update_format():
    response = pihole.getVersion()
    print(pihole.getGraphData())
    return "update available : " + str((response['core_update'] or response['web_update'] or response['FTL_update']))

def graph():
    datas = pihole.getGraphData()
    xads = list()
    xdomains = list()
    for i in datas['ads'].values():
        xads.append(i)
    for i in datas['domains'].values():
        xdomains.append(i)
    plt.figure()
    plt.subplot(211)
    plt.axis('auto')
    plt.xticks([])
    plt.title('Ads blocked')
    plt.plot(xads, "r", label="ads")
    plt.subplot(212)
    plt.axis('auto')
    plt.xticks([])
    plt.title('Domains requests')
    plt.plot(xdomains, "g", label="domains")
    plt.savefig('/tmp/pigraph.png')
    plt.close()
    f = open('/tmp/pigraph.png', 'rb')  # some file on local disk
    return f
    
def main(bot, chat_id, msg):
    print((str("je suis dans " + __name__)))
    MyGlobals.currentMenu = 'pihole'
    if msg['text'] == 'PiHole':
        bot.sendMessage(chat_id, "Pi Hole :", reply_markup=myKeyboard)
    if (msg['text'] == 'Stats'
        and MyGlobals.currentMenu == 'pihole'):
        bot.sendMessage(chat_id, get_summary(), reply_markup=myKeyboard)
    if (msg['text'] == 'Update ?'
        and MyGlobals.currentMenu == 'pihole'):
        bot.sendMessage(chat_id, update_format(), reply_markup=myKeyboard)
    if (msg['text'] == 'Graph'
        and MyGlobals.currentMenu == 'pihole'):
        bot.sendPhoto(chat_id,
                      graph())
    elif msg['text'] == '<- Back':
        MyGlobals.currentMenu = 'Main'
        bot.sendMessage(chat_id, "Main Menu :",
                        reply_markup=MyGlobals.mainKeyboard)
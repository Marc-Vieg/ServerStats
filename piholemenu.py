# -*- coding: utf-8 -*-
import time
import os
from tokens import pihole_passwd
from telepot.namedtuple import ReplyKeyboardMarkup
from botglobalvars import MyGlobals
import pihole as ph
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

pihole = ph.PiHole("pi.hole")
pihole.authenticate(pihole_passwd)
pihole.refresh()

myKeyboard = ReplyKeyboardMarkup(keyboard=[
    ['Stats', 'Devices'],['Update'],['Graph'],
    ['<- Back']])


def get_summary():
    response = pihole.refresh()
    summary = 'Status: ' + pihole.status + '\n' + \
            'Domains being blocked: ' + pihole.domain_count + '\n' + \
            'Total Queries today: ' + pihole.queries + '\n' + \
            'Ads blocked today: ' + pihole.blocked + '\n' + \
            'Queries Blocked: ' + pihole.ads_percentage + '%' + '\n' + \
            'forwarded: ' + pihole.forwarded + '\n' +  \
            'cached: ' + pihole.cached + '\n' +  \
            'total_clients: ' + pihole.total_clients + '\n' + \
            'unique_clients: ' + pihole.unique_clients + '\n' + '\n' 
    return summary

def get_devices():
    pihole.refresh()
    m = 'Top devices : \n\n'
    for name, nb in pihole.top_devices.items():
        name, address = name.split('|')
        m += "{0} ({1}) : {2}\n".format(name, address, nb)
    return m
    
def update_format():
    response = pihole.getVersion()
    component =""
    if (response['core_update'] or response['web_update'] or response['FTL_update']):
        for name, value in response.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
            if value=='True':
                component += " " + name.split("_")[0] 
        return "An update is available for :" + component
    else:
        return "Your Pi-Hole is up to date !"
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
    print((str( __name__)))
    MyGlobals.currentMenu = 'pihole'
    if msg['text'] == 'PiHole':
        bot.sendMessage(chat_id, "Pi Hole :", reply_markup=myKeyboard)
    if (msg['text'] == 'Stats'
        and MyGlobals.currentMenu == 'pihole'):
        bot.sendMessage(chat_id, get_summary(), reply_markup=myKeyboard)
    if (msg['text'] == 'Devices'
        and MyGlobals.currentMenu == 'pihole'):
        bot.sendMessage(chat_id, get_devices(), reply_markup=myKeyboard)
    if (msg['text'] == 'Update'
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
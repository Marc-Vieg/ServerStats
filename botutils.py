# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import operator
import psutil
from datetime import datetime
from datetime import timedelta
from telepot.namedtuple import ReplyKeyboardMarkup
from subprocess import Popen, PIPE, STDOUT
from botglobalvars import MyGlobals
import pyspeedtest

myKeyboard = ReplyKeyboardMarkup(keyboard=[
    ['stats', 'temp', 'speedtest'],
    ['Big Graph', 'logwatch'],
    ['Raid', 'Disks', 'IP'],
    ['<- RETOUR']])


def logwatch(bot, chat_id):
    command = str('logwatch --output stdout --format text |' +
                  'while IFS= read -r line;do telegram-send "$line";done')
    p = Popen(command, shell=True, stdin=PIPE, stderr=STDOUT,
            stdout=PIPE, close_fds=True)
    output = p.stdout.read()
    bot.sendMessage(chat_id, output)


def raidstatus():
    p = Popen('cat /proc/mdstat | grep md',
              shell=True, stdin=PIPE, stderr=STDOUT,
              stdout=PIPE, close_fds=True)
    output = str(p.stdout.read())
    return output


def memgraph(bot, chat_id, value):
    bot.sendChatAction(chat_id, 'typing')
    time = sum(MyGlobals.Datas['timing'])
    if time < 60:
        tmperiod = " last %d secondes" % time
    if time >= 60 and time < 3600:
        tmperiod = " last " + str(timedelta(seconds=
                    sum(MyGlobals.Datas['timing']))) + " minutes"
    if time >= 3600:
        tmperiod = " last " + str(MyGlobals.GraphicHours) + " hours"
    if value == 'all':
        bot.sendPhoto(chat_id,
                      plotbiggraph(MyGlobals.Datas, MyGlobals.xaxis, tmperiod))


def plotbiggraph(Datas, xaxis, tmperiod):
    xaxis = []
    j = 0
    for i in Datas['timing']:
        j += i
        xaxis.append(j)
    plt.xlabel(tmperiod)
    plt.ylabel('% Used')
    plt.title('Memory, Cpu and Temperature Usage Graph')
    #mem graph
    plt.text(0.1 * len(xaxis), MyGlobals.memorythreshold + 2,
             'Memory Threshold: ' + str(MyGlobals.memorythreshold) + ' %')
    #usage graph
    plt.text(0.1 * len(xaxis), MyGlobals.usagethreshold + 2,
             'Cpu Threshold: ' + str(MyGlobals.usagethreshold) + ' %')
    xaxis[0] = 0
    Datas['timing'][0] = 0
    memthresholdarr = []
    usagethresholdarr = []
    for xas in xaxis:
        memthresholdarr.append(MyGlobals.memorythreshold)
    for xas in xaxis:
        usagethresholdarr.append(MyGlobals.usagethreshold)
    plt.plot(xaxis, memthresholdarr, 'g--',
             xaxis, usagethresholdarr, 'b--')
    #mem
    Datas['mem'][0] = 0
    plt.plot(xaxis, Datas['mem'], 'g-', label="mem")
    #cpu
    Datas['cpu'][0] = 0
    plt.plot(xaxis, Datas['cpu'], 'b-', label="cpu")
    #temp
    Datas['temp'][0] = 0
    plt.plot(xaxis, Datas['temp'], 'r-.', label="°C")
    #plt.axis([0, j, 0, 100])

    plt.axis('auto')
    if j < 7200:
        plt.xlim(0, j)
    else:
        plt.xlim(j - (MyGlobals.GraphicHours * 3600), j)
    plt.ylim(0, 100)

    plt.savefig('/tmp/graph.png')
    plt.close()
    f = open('/tmp/graph.png', 'rb')  # some file on local disk
    return f


def stats(bot, chat_id):
    print("je suis dans botutils.stats()")
    bot.sendChatAction(chat_id, 'typing')
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boottime = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    timedif = "Online for: %.1f Hours" % \
              (((now - boottime).total_seconds()) / 3600)
    memtotal = "Total memory: %.2f GB " % (memory.total / 1000000000)
    memavail = "Available memory: %.2f GB" % (memory.available / 1000000000)
    memuseperc = "Used memory: " + str(memory.percent) + " %"
    diskused = "Disk used: " + str(disk.percent) + " %"
    cpupercent = "Cpu usage: " + str(psutil.cpu_percent(1)) + " %"
    pids = psutil.pids()
    pidsreply = ''
    cpusreply = ''
    procs = {}
    procscpu = {}
    for pid in pids:
        p = psutil.Process(pid)
        try:
            pmem = p.memory_percent()
            if pmem > 0.5:
                if p.name() in procs:
                    procs[p.name()] += pmem
                else:
                    procs[p.name()] = pmem
        except:
            print("exception calculating by process memory %")
    sortedprocs = sorted(procs.items(),
                  key=operator.itemgetter(1), reverse=True)
    for proc in sortedprocs:
        pidsreply += proc[0] + " " + ("%.2f " % proc[1]) + " % mem \n"
    for pid in pids:
        p = psutil.Process(pid)
        try:
            pcpu = p.cpu_percent(interval=0.01) / psutil.cpu_count()
            print((str(p.name()) + " " + str(pcpu)))
            if pcpu > 0.1:
                if p.name() in procscpu:
                    procscpu[p.name()] += pcpu
                else:
                    procscpu[p.name()] = pcpu
        except:
            print("exception calculating by process cpu usage %")
    sortedcpus = sorted(procscpu.items(),
                 key=operator.itemgetter(1), reverse=True)
    for proc in sortedcpus:
        cpusreply += proc[0] + " " + ("%.2f " % proc[1]) + " % cpu \n"
    reply = timedif + "\n" + \
            memtotal + "\n" + \
            memavail + "\n" + \
            memuseperc + "\n" + \
            diskused + "\n" + \
            cpupercent + "\n\n" + \
            pidsreply + "\n " + \
            cpusreply + "\n\n"
    bot.sendMessage(chat_id, reply, disable_web_page_preview=True)


def recupTemp():
#get temperatures from psutil, and retrun temeratures[]
#ex : print(temperatures['Core 0']) -> 45
    sensors_raw = psutil.sensors_temperatures()
    sensors_coretemp = str(sensors_raw['coretemp'])
    tmp = []
    testlabel = ''
    temperatures = dict()
    for labelneeded in MyGlobals.myCores:
        while testlabel != labelneeded:
            index = sensors_coretemp.find(labelneeded)
            tempString = sensors_coretemp
            tmp = tempString[index:]
            tmp = tempString.split("'")
            for testlabel in tmp:
                if testlabel == labelneeded:
                    tmpp = str(tmp)
                    indext = tmpp.find('current=')
                    indext += 8
                    tmpp = tmpp[indext:]
                    temperatures[testlabel] = int(tmpp.split('.')[0])
                    break
    return temperatures


def gettemp(bot, chat_id):
    temperatures = recupTemp()
    reply = "Temperatures : \n"
    for core in MyGlobals.myCores:
        reply += core + " : " + ("%d " % temperatures[core]) + "°C \n"
    bot.sendMessage(chat_id, reply, reply_markup=myKeyboard)


def getip(bot, chat_id):
    p = Popen('curl ifconfig.me', shell=True,
               stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
    output = p.stdout.read()
    output = output[:-1]
    bot.sendMessage(chat_id, str("Mon IP publique actuelle : "
                    + str(output)), reply_markup=myKeyboard)

def disks():
    print((str("je suis dans " + __name__ + ".disks")))
#code from pysysbot https://github.com/fabaff/pysysbot
#thank you fabaff !
    templ = "%-20s %8s %8s %8s %5s%% %s\n"
    disks = templ % ("Device", "Total", "Used", "Free", "Use ", "Mount")
    for part in psutil.disk_partitions(all=False):
        usage = psutil.disk_usage(part.mountpoint)
        disks = disks + templ % (part.device,
                        bytes2human(usage.total),
                        bytes2human(usage.used),
                        bytes2human(usage.free),
                        int(usage.percent),
                        part.mountpoint)
    #print(str(disks))
    return str(disks)


def bytes2human(n):
# Credits: http://code.activestate.com/recipes/578019
#thank you fabaff !
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def speedtest(bot, chat_id):
    bot.sendChatAction(chat_id, 'typing')
    st = pyspeedtest.SpeedTest()
    up = bytes2human(round(st.upload()/8))
    down = bytes2human(round(st.download()/8))
    ping = round(st.ping())
    return str("Up : " + str(up) +"\nDown : "+ str(down) + "\nPing : " + str(ping))


def main(bot, TOKEN, chat_id, msg):
    print((str("je suis dans " + __name__)))
    MyGlobals.currentMenu = 'Utils'
    if msg['text'] == 'Utils':
        bot.sendMessage(chat_id, str("Utilitaires"), reply_markup=myKeyboard)
        MyGlobals.currentMenu = 'Utils'
    elif msg['text'] == 'stats':
        stats(bot, chat_id)
    elif msg['text'] == 'Big Graph':
        memgraph(bot, chat_id, 'all')
    elif msg['text'] == 'IP':
        getip(bot, chat_id)
    elif msg['text'] == 'temp':
        gettemp(bot, chat_id)
    elif msg['text'] == 'logwatch':
        logwatch(bot, chat_id)
    elif msg['text'] == 'Raid':
        bot.sendMessage(chat_id, raidstatus(), reply_markup=myKeyboard)
    elif msg['text'] == 'Disks':
        bot.sendMessage(chat_id, disks(), reply_markup=myKeyboard)
    elif msg['text'] == 'speedtest':
        bot.sendMessage(chat_id, speedtest(bot, chat_id), reply_markup=myKeyboard)
    elif msg['text'] == '<- RETOUR':
        MyGlobals.currentMenu = 'Main'
        bot.sendMessage(chat_id, "retour au menu principal",
                        reply_markup=MyGlobals.mainKeyboard)


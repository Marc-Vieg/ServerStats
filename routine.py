# -*- coding: utf-8 -*-

import asyncio
from time import time
import psutil
import telepot


class Routine():
    """
    Routine class that describe routine action needed
    """
    def __init__(self, config, data, tools):
        self.botConfig = config
        self.botData = data
        self.botTools = tools
        self.bot = telepot.Bot(self.botConfig.TOKEN)

    def routine(self):
        t_start, t_next = 0, 0
        while True:
            if t_start == 0:
                t_start = time()
            t_next = time()
            if t_next - t_start >= self.botConfig.poll:
                asyncio.run(self.action())
                t_start, t_next = 0, 0

    async def action(self):
        """
        Here is actions needed to report
        """
        # Initiate IP surveillance
        lastIpCheck = round(time())
        self.botTools.ipCheck('0', lastIpCheck)

        if self.botConfig.autoSend:
            self.botTools.memgraph('all')
            for chatId in self.botConfig.adminchatid:
                self.bot.sendMessage(
                    chat_id=chatId,
                    text=f"""Survey report all
                         {str(self.botConfig.poll)} seconds"""
                )
        memck = psutil.virtual_memory()
        mempercent = memck.percent
        usagepercent = psutil.cpu_percent(0.5)

        # Maintain list of proc uses
        temperatures = self.botTools.gettemp(True)
        z = 0
        somme = 0
        for core in self.botConfig.myCores:
            z += 1
            somme += temperatures[1][core]
        tempMoyenne = somme / z
        self.botData.appendData(usagepercent, mempercent, tempMoyenne)

        # Alert if memory is low
        if ((mempercent > self.botConfig.memorythreshold)
           and self.botConfig.sendAlerts):
            memavail = "Available memory: %.2f GB" \
                    % (memck.available / 1000000000)
            for chatId in self.botConfig.adminchatid:
                self.bot.sendMessage(
                    chat_id=chatId,
                    text=f"CRITICAL! LOW MEMORY !\n{memavail}\n \
                         {str(mempercent)}% of memory used"
                )
            self.botTools.memgraph('all')

        # Alert if cpu usage percent is high
        if ((usagepercent > self.botConfig.usagethreshold)
           and self.botConfig.sendAlerts):
            for chatId in self.botConfig.adminchatid:
                self.bot.sendMessage(
                    chat_id=chatId,
                    text=f"CRITICAL! HIGH CPU !\n \
                         {str(usagepercent)} % of cpu used"
                )
            self.botTools.memgraph('all')

        # Check IP adress for those who have dynamic IP
        self.botTools.ipCheck(self.botConfig.MyIp, lastIpCheck)

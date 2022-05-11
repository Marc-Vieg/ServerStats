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
        if self.botConfig.autoSend:
            isOK, result = self.botTools.example()
            for chatId in self.botConfig.adminchatid:
                self.bot.sendMessage(
                    chat_id=chatId,
                    text=f"""Survey report all {str(self.botConfig.poll)} \
                         seconds\n
                         It's {result}"""
                )

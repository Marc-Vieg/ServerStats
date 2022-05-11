# -*- coding: utf-8 -*-

import asyncio
from multiprocessing import Process
import os
import telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
from botTools import BotTools
# bot tools
from botData import BotData
from botConfig import BotConfig
# Message handler
from mainMessageHandler import MainMessageHandler
from routine import Routine

TIMEOUT = 20 * 60


if __name__ == "__main__":
    # Get proc id
    pid = os.getpid()
    op = open(os.path.dirname(os.path.abspath(__file__)) + "/ssb.pid", "w")
    op.write(str(pid))
    op.close()

    # Init config
    config = BotConfig(os.path.dirname(os.path.abspath(__file__))
                       + "/settings.ini")
    config.loadSettings()
    data = BotData()
    tools = BotTools(config, data)

    # Run Bot
    bot = telepot.aio.DelegatorBot(config.TOKEN, [
        pave_event_space()(
            per_chat_id(), create_open,
            MainMessageHandler, config, data, tools,
            timeout=TIMEOUT
        )
    ])

    monitoring = Routine(config, data, tools)
    process = Process(
        target=monitoring.routine,
        daemon=True
    )
    process.start()

    # Message Handler
    loop = asyncio.get_event_loop()
    loop.create_task(MessageLoop(bot).run_forever())
    print('Listening ...')
    loop.run_forever()

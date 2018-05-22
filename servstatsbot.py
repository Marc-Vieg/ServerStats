# -*- coding: utf-8 -*-
import botfunction as funk
import os
import botConfig as config


if __name__ == "__main__":
    pid = os.getpid()
    op = open("ssb.pid", "w")
    op.write("%s" % pid)
    op.close()
    if not config.exist('settings.ini'):
        config.createConfig('settings.ini')
    config.loadSettings('settings.ini')
    funk.main()
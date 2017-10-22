# -*- coding: utf-8 -*-
import botfunction as funk
import os

if __name__ == "__main__":
    pid = os.getpid()
    op = open("ssb.pid", "w")
    op.write("%s" % pid)
    op.close()
    #__init__()
    funk.main()
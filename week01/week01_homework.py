#!/usr/bin/env python3

import datetime
import logging
import pathlib
import os
import re
from time import sleep


def make_log():
    today = datetime.date.today()
    logName = '/var/log/python-{}/xxxx.log'.format(today)
    log_BaseDir = re.match('(.*)xxxx(.log)', logName).group(1)

    if pathlib.Path(log_BaseDir).exists():
        if os.path.exists(logName):
            if not os.access(logName, os.W_OK):
                os.system("chmod u+w {}".format(logName))

        else:
            logfile = open(logName, 'w+')
            logfile.close()

    else:
        os.makedirs(log_BaseDir)
        logfile = open(logName, 'w+')
        logfile.close()

    logging.basicConfig(filename=logName,level=logging.DEBUG,datefmt="%Y-%m-%d %H:%M:%S",
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    logging.info("test logging")

if __name__ == '__main__':
    while True:
        make_log()
        sleep(1)

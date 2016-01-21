#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time

from optparse import OptionParser
sys.path.append('./TestLibs/')
from device import Device

def parse_option_args():
    """parse the option args"""
    optionParser = OptionParser()
    optionParser.add_option("-d", "--device",
            help="the test device from which we gathering Exceptions")
    optionParser.add_option("-t", "--time",
            help="the elapse time, in hours")

    option, args = optionParser.parse_args()

    return option

if __name__ == "__main__":
    opt = parse_option_args()
    TEST_DEVICE = opt.device if opt.device is not None else "8600176"
    ELAPSE_TIME = opt.time if opt.time is not None else 24

    LOOP_COUNT = ELAPSE_TIME * 30
    dev = Device(TEST_DEVICE)

    CMD = "logcat -v time -d |grep Percolata | grep Exception -B10 -A30"
    while LOOP_COUNT > 0:
        time.sleep(120)
        ret = dev.runCommand(CMD)
        with open('./dump/exception.log', 'wb') as out:
            print >>out, ret

        LOOP_COUNT -= 1



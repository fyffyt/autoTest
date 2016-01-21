#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

"""

import unittest
import re
import os
import sys
import time

import logging
import pexpect
import HTMLTestRunner
sys.path.append("./TestLibs/")
from server import RemoteServer
from optparse import OptionParser

def testAllinCurrent():
    """
    Load all test modules which are in the same dirPath of this script.

    If the test module files stored in other dir, we should change 'path'
    to the associated dirPath
    """
    path = os.path.abspath(os.path.dirname(sys.argv[0])) + '/TestScripts/'
    sys.path.append(path)
    files = os.listdir(path)
    test = re.compile(r"^tc_.*\.py\Z", re.IGNORECASE)
    files = filter(test.search, files)
    filenameToModuleName = lambda f: os.path.splitext(f)[0]
    moduleNames = map(filenameToModuleName, files)
    modules = map(__import__, moduleNames)
    count = 0

    print("="*100)
    for m in modules:
        count += 1
        print("TestCase %s: "%count, m)
    print("+"*100)

    load = unittest.defaultTestLoader.loadTestsFromModule
    return unittest.TestSuite(map(load, modules))

def parse_option_args():
    """parse the option args"""
    parser = OptionParser()
    parser.add_option("-L", "--level", help="logging level of testing")

    (options, args) = parser.parse_args()

    return options

if __name__ == "__main__":
    opt = parse_option_args()
    logging_levels = {"info": logging.INFO,
                "debug": logging.DEBUG,
                "warn": logging.WARN,
                "error": logging.ERROR,
                "critical": logging.CRITICAL,
                "fatal": logging.FATAL
            }
    LOGGING_LEVEL = logging_levels[opt.level] if opt.level is not None else logging.INFO

    with open("FSTest.html","wb") as ofile:
        fusionSensorTestSuite = testAllinCurrent()
        fusionSensorTestRunner = HTMLTestRunner.HTMLTestRunner(
                    stream = ofile,
                    title = "Percolata Test Report",
                    description = """
                        Test For FusionSensor2.0 with new data pipeline
                    """
                )
        fusionSensorTestRunner.run(fusionSensorTestSuite)

    dayStr = time.strftime("%Y-%m-%d", time.gmtime(time.time()))
    dp0 = RemoteServer("dp0")
    dp0.upload("FSTest.html", "/var/www/")
    dp0.upload("FSTest.html", "/var/www/FSTest_%s.html" % dayStr)
    dp0.close()


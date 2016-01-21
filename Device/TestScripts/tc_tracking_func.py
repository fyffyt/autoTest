#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test whether the tracking file can be generated.
"""

import unittest
import sys
import time

sys.path.append('../TestLibs/')
from device import Device
from config import ConfigManager
from context import ContextManager
from bs_logger import BSLogger


class TC_TRACKING_FUNC(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.mContext = ContextManager()
        self.mDev = Device(self.mContext.getTestDevice())
        self.monitor = self.mContext.getStorageMonitor(self.mDev)
        self.mCfg = ConfigManager(self.mDev)
        self.logger = BSLogger("log/tc_tracking_func.log")

    @classmethod
    def tearDownClass(self):
        self.mCfg.close()
        self.monitor.close()
        self.mDev.close()
        self.mContext.close()

    def test_tracking_generating(self):
        self.assertEqual(self.mDev.isFSRunning(), True, "Fusion Sensor is not running.")
        self.mCfg.setTrackingMode()
        timeStamp = time.time()
        time.sleep(25*60)

        #record warning messages to log while cpu/mem/sdcard usage exceed threhold
        self.mDev.sysmon(self.logger)

        print("Begin to check data at: %s" %\
                time.strftime("%Y-%m-%d-%H-%M-%S")
                )
        self.assertTrue(self.mDev.isNewDataOnDevice("tracking", timeStamp) or self.monitor.isNewTrackingUploaded(),
                    "Failed to find new tracking data"
                )
        print("tracking generating is approved")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test whether the cpu usage beyond the threshold.
"""

import unittest
import os
import sys
import time
import inspect

sys.path.append('../TestLibs/')
from device import Device
from config import ConfigManager
from bs_logger import BSLogger
from context import ContextManager

CWD = os.path.abspath(
	os.path.dirname(
		inspect.stack()[0][1]
		)
	)

class TC_AUDIO_FUNC_001(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.mContext = ContextManager()
        self.mDev = Device(self.mContext.getTestDevice())
        self.monitor = self.mContext.getStorageMonitor(self.mDev)
        self.mCfg = ConfigManager(self.mDev)
        self.logger = BSLogger(os.path.join(
            CWD,
            "log/tc_cpu_usage.log"
            )
        )

    @classmethod
    def tearDownClass(self):
        self.mCfg.close()
        self.monitor.close()
        self.mDev.close()
        self.mContext.close()

    def test_cpu_usage(self):
        self.assertEqual(self.mDev.isFSRunning(), True, "Fusion Sensor is not running.")
        self.mCfg.setTrackingMode()
        self.mCfg.setAudio(True)
        time.sleep(6*60)
        print("Begin to check data at: %s" %\
                time.strftime("%Y-%m-%d-%H-%M-%S")
                )
        self.assertTrue(self.mDev.isNewDataOnDevice("audio") or self.monitor.isNewAudioUploaded(),
                    "Failed to find new audio data"
                )
        print("Audio generating is approved")

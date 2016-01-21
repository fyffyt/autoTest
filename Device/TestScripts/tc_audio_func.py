#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test whether the audio file can be generated.
"""

import unittest
import sys
import time

sys.path.append('../TestLibs/')
from device import Device
from config import ConfigManager
from context import ContextManager
from bs_logger import BSLogger

class TC_AUDIO_FUNC_001(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.mContext = ContextManager()
        self.mDev = Device(self.mContext.getTestDevice())
        self.monitor = self.mContext.getStorageMonitor(self.mDev)
        self.mCfg = ConfigManager(self.mDev)
        self.logger = BSLogger("log/tc_audio_func.log")

    @classmethod
    def tearDownClass(self):
        self.mCfg.close()
        self.monitor.close()
        self.mDev.close()
        self.mContext.close()

    def test_audio_generating(self):
        self.assertEqual(self.mDev.isFSRunning(), True, "Fusion Sensor is not running.")
        self.mCfg.setTrackingMode()
        self.mCfg.setAudio(True)
        time.sleep(7*60)

        #record warning messages to log while cpu/mem/sdcard usage exceed threhold
        self.mDev.sysmon(self.logger)

        print("Begin to check data at: %s" %\
                time.strftime("%Y-%m-%d-%H-%M-%S")
                )
        self.assertTrue(self.mDev.isNewDataOnDevice("audio") or self.monitor.isNewAudioUploaded(),
                    "Failed to find new audio data"
                )
        print("Audio generating is approved")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test whether the audio file can be generated.
"""

import unittest
import sys
import time
import os
import inspect

sys.path.append('../TestLibs/')
from bs_logger import BSLogger

TEST_DEVICE = "8600176"
CWD = os.path.abspath(
	os.path.dirname(
		inspect.stack()[0][1]
		)
	)

class TC_BS_LOGGER(unittest.TestCase):
    @classmethod
    def setUpClass(self):
	print CWD
	self.logger = BSLogger(os.path.join(
		CWD,
		"log/tc_example.log"
		)
	)

    @classmethod
    def tearDownClass(self):
	pass

    def test_bs_logger(self):
        print("test BSLogger")
	self.logger.i("test BSLogger")

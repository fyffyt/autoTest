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
from gs import GSMonitor
from config import ConfigManager
from context import ContextManager

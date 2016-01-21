#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
import json
import os
import sys

sys.path.append('../TestLibs')
from gs import GSMonitor
from azure_storage import ASMonitor

class ContextManager(object):
    "context manager for test environment"
    def __init__(self):
        CWD = os.path.abspath(
            os.path.dirname(
                inspect.stack()[0][1]
                )
            )
        configName = os.path.join(CWD, '../TestConfig/config')
        with open(configName, 'rb') as conf:
            self.mCfg = json.load(conf)

    def getTestDevice(self):
        return self.mCfg['testDevice']

    def getStorageType(self):
        return self.mCfg['storage']

    def getStorageMonitor(self, dev):
        if self.getStorageType() == "google":
            return GSMonitor(dev)
        elif self.getStorageType() == "azure":
            return ASMonitor(dev)
        else:
            raise NotImplementedError("Not support %s storage service yet."
                    % self.getStorageType()
                    )

    def close(self):
        pass


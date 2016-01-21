#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

"""

import boto
import json
import requests
import hashlib
import os
import sys
import inspect

sys.path.append('../TestLibs')
from context import ContextManager
from azure_storage import AzureManager

class ConfigManager(object):
    """Afford method for config modification.
    This class is associated with instance of TestLibs.device.Device
    """
    def __init__(self, dev):
        self.dev = dev

    def close(self):
        pass

    def setInstallMode(self):
        newCfg = {'installation-mode': "yes"}
        self.dev.setDevCfg(newCfg)

    def setVideoMode(self):
        newCfg = {'capture-mode': "video", 'installation-mode': "no"}
        self.dev.setDevCfg(newCfg)

    def setLoiMode(self):
        newCfg = {'capture-mode': "loi", 'installation-mode': "no"}
        self.dev.setDevCfg(newCfg)

    def setZoneCountMode(self):
        newCfg = {'capture-mode': "zone-count", 'installation-mode': "no"}
        self.dev.setDevCfg(newCfg)

    def setTrackingMode(self):
        newCfg = {'capture-mode': "tracking", 'installation-mode': "no"}
        self.dev.setDevCfg(newCfg)

    def setAudio(self, signal):
        newCfg = dict(
                    audio = "true" if signal else "false"
                )
        self.dev.setDevCfg(newCfg)

    def setWifiSniff(self, signal):
        newCfg = {
                    'wifi-sniff-enable': "true" if signal else "false"
                }
        self.dev.setDevCfg(newCfg)

    def setVideoBkp(self, signal):
        newCfg = dict(
                   videoBackup = "true" if signal else "false"
                )
        self.dev.setDevCfg(newCfg)

    def setWifiAccess(self, seqNO, SSID, KEY):
        newCfg = {"WifiAccess":{
                        seqNO: {
                                "SSID": SSID,
                                "key": KEY,
                                "hiddenSSID": "no"
                            },
                        "AccessList":[
                                "1",
                                "2",
                                "3",
                                "4"
                            ]
                    }
                }
        self.dev.setDevCfg(newCfg)

class ConfigManager2(object):
    """Afford method for config modification.
    This class is associated with the target device's placement_name
    But only support the devices connected to ci-api
    """
    def __init__(self, devName):
        self.devName = devName
        self.mergeDict = lambda d1, d2: {k: d1[k] if not k in d2
                                    else self.mergeDict(d1[k], d2[k]) if (k in d1 and
                                        type(d1[k]).__name__ == 'dict' and
                                        type(d2[k]).__name__ == 'dict')
                                        else d2[k] for k in set(d1) | set(d2)}
        self.mContext = ContextManager()
        self.storageType = self.mContext.getStorageType()

    def close(self):
        pass

    def setInstallMode(self):
        newCfg = {'installation-mode': "yes"}
        self.setDevCfg(newCfg)

    def setVideoMode(self):
        newCfg = {'capture-mode': "video", 'installation-mode': "no"}
        self.setDevCfg(newCfg)

    def setLoiMode(self):
        newCfg = {'capture-mode': "loi", 'installation-mode': "no"}
        self.setDevCfg(newCfg)

    def setZoneCountMode(self):
        newCfg = {'capture-mode': "zone-count", 'installation-mode': "no"}
        self.setDevCfg(newCfg)

    def setTrackingMode(self):
        newCfg = {'capture-mode': "tracking", 'installation-mode': "no"}
        self.setDevCfg(newCfg)

    def setAudio(self, signal):
        newCfg = dict(
                    audio = "true" if signal else "false"
                )
        self.setDevCfg(newCfg)

    def setWifiSniff(self, signal):
        newCfg = {
                    'wifi-sniff-enable': "true" if signal else "false"
                }
        self.setDevCfg(newCfg)

    def setVideoBkp(self, signal):
        newCfg = dict(
                   videoBackup = "true" if signal else "false"
                )
        self.setDevCfg(newCfg)

    def setWifiAccess(self, seqNO, SSID, KEY):
        newCfg = {"WifiAccess":{
                        seqNO: {
                                "SSID": SSID,
                                "key": KEY,
                                "hiddenSSID": "no"
                            },
                        "AccessList":[
                                "1",
                                "2",
                                "3",
                                "4"
                            ]
                    }
                }
        self.setDevCfg(newCfg)

    def getDevCfg(self):
        if self.storageType == 'google':
            return self.getDevCfgFromGS()
        elif self.storageType == 'azure':
            return self.getDevCfgFromAS()
        else:
            raise NotImplementedError("Not support %s storage service yet."
                    % self.storageType
                    )

    def setDevCfg(self, newCfg):
        if self.storageType == 'google':
            self.setDevCfgToGS(newCfg)
        elif self.storageType == 'azure':
            self.setDevCfgToAS(newCfg)
        else:
            raise NotImplementedError("Not support %s storage service yet."
                    % self.storageType
                    )

    def getDevCfgFromGS(self):
        """get device config file from google storage, need config .boto in users' home dir
        @return a dict form config
        """
        gs_conn = boto.connect_gs()
        bucket = gs_conn.get_bucket("percolata-test")#T_T
        key = bucket.get_key(r"config/%s.json" % self.devName)
        devCfg = json.loads(key.get_contents_as_string())
        return devCfg

    def initAzureService(self):
        CWD = os.path.abspath(
            os.path.dirname(
                inspect.stack()[0][1]
                )
            )
        KEY_FILE = os.path.join(CWD, "../TestConfig/keys")
        with open(KEY_FILE, 'rb') as keyFile:
            keyDict = json.load(keyFile)
            azureNameKey = keyDict['azure']
            self.azureService = AzureManager(
                    azureNameKey['account_name'],
                    azureNameKey['account_key']
                    )

    def getDevCfgFromAS(self):
        """get device config file from azure storage, need keys file in ../TestConfig
        @return a dict form config
        """
        self.initAzureService()
        container = "percolata-test"

        remoteFilePath = "as://" + container + '/config/%s.json' % self.devName
        content = self.azureService.get_text_from_container(remoteFilePath)
        return json.loads(str(content, encoding="utf-8"))

    def setDevCfgToGS(self, newCfg):
        """set device config file on google storage, need config .boto in users' home dir
        @param newCfg: new device config items in json form
        e.g.
        {
            "devName": "8600067",
            "hostname": "https://phone:11222011@api.percolata.com",
            "softwareUpdate": {
                "updateURL": "https://phone:11222011@api.percolata.com"
            },
            "WifiAccess": {
                "1": {
                    "SSID": "Percolata-2G",
                    "hiddenSSID": "no",
                    "key": "&*^@374"
                }
            },
            "AccessList": [
                "1"
            ]
        }
        """
        gs_conn = boto.connect_gs()
        bucket = gs_conn.get_bucket("percolata-test")#T_T
        url = "https://ci-api.percolata.com/modify_config"#WARN: write IP inline
        key = bucket.get_key(r"config/%s.json" % self.devName)
        oldDevCfg = json.loads(key.get_contents_as_string())
        newDevCfg = self.mergeDict(oldDevCfg, newCfg)

        with open("./tmp_dev_cfg.json","wb+") as cfg:
            json.dump(newDevCfg, cfg, indent=4, separators=[',', ':'], sort_keys=True)
            cfg.flush()
            cfg.seek(0)
            md5 = self.getMD5(cfg.read())
            cfg.seek(0)
            r = requests.post(
                    url,
                    auth=('phone', '11222011'),
                    headers={'HOST': 'config.percolata.com'},
                    data={
                        'placement_name': self.devName,
                        'file_name': self.devName + '.json',
                        'md5': md5},
                    files={'file': cfg},
                    verify=False
                    )
            if not r.status_code == 200:
                raise RuntimeError("Failed to modify config with: %s" % r.content)

    def setDevCfgToAS(self, newCfg):
        """set device config file on google storage, need config .boto in users' home dir
        @param newCfg: new device config items in json form
        e.g.
        {
            "devName": "8600067",
            "hostname": "https://phone:11222011@api.percolata.com",
            "softwareUpdate": {
                "updateURL": "https://phone:11222011@api.percolata.com"
            },
            "WifiAccess": {
                "1": {
                    "SSID": "Percolata-2G",
                    "hiddenSSID": "no",
                    "key": "&*^@374"
                }
            },
            "AccessList": [
                "1"
            ]
        }
        """
        self.initAzureService()
        container = "percolata-test"
        url = "https://ci-api.percolata.com/modify_config"#WARN: write IP inline

        remoteFilePath = "as://" + container + '/config/%s.json' % self.devName

        oldDevCfg = self.getDevCfgFromAS()
        newDevCfg = self.mergeDict(oldDevCfg, newCfg)

        with open("./tmp_dev_cfg.json","wb+") as cfg:
            json.dump(newDevCfg, cfg, indent=4, separators=[',', ':'], sort_keys=True)
            cfg.flush()
            cfg.seek(0)
            md5 = self.getMD5(cfg.read())
            cfg.seek(0)
            r = requests.post(
                    url,
                    auth=('phone', '11222011'),
                    headers={'HOST': 'config.percolata.com'},
                    data={
                        'placement_name': self.devName,
                        'file_name': self.devName + '.json',
                        'md5': md5},
                    files={'file': cfg},
                    verify=False
                    )
            if not r.status_code == 200:
                raise RuntimeError("Failed to modify config with: %s" % r.content)

    def getMD5(self, content, system="hex"):
        """
        Args:
            content: content to be added md5
        Return:
            md5 string
        """
        m = hashlib.md5()
        m.update(content)
        if system == 'hex':
            return m.hexdigest()
        else:
            return m.digest()

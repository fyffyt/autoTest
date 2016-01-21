#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

"""

import re
import os
import time
import pexpect
import json
import boto

from device import Device

class GSMonitor(object):
    """monitor for google storage"""
    def __init__(self, dev=None):
        gs_conn = boto.connect_gs()

        self.device = dev
        if self.device is None:
            self.bucket = gs_conn.get_bucket("percolata-test")
            return

        hostname = self.device.getLocalCfg()['hostname']
        if hostname.__contains__("ci-api"):
            self.bucket = gs_conn.get_bucket("percolata-test")
        elif hostname.__contains__("api"):
            self.bucket = gs_conn.get_bucket("percolata-data")
        else:
            raise NotImplementedError("unsupported api" % hostname)

    def attachDev(self, dev):
        """set associate device for GSMonitor"""
        self.device = dev

    def close(self):
        pass

    def isNewVideoUploaded(self,
            timeline=time.time() - 20*60):
        """check whether new video data after timeline had been uploaded
        @param timeline: seconds since 1970.01.01.00.00.00
        """
        return self.isDataUploaded(
                    path="data/fragment/video/dump/",
                    placement=self.device.PlacementID,
                    timeline=timeline
                    ) or self.isDataUploaded(
                    path="data/combined/video/",
                    placement=self.device.PlacementID,
                    timeline=timeline
                    )

    def isNewLoiUploaded(self,
            timeline=time.time() - 20*60):
        """check whether new loi data after timeline had been uploaded
        @param timeline: seconds since 1970.01.01.00.00.00
        """

        return self.isDataUploaded(
                    path="data/fragment/loi/dump/",
                    placement=self.device.PlacementID,
                    timeline=timeline
                    ) or self.isDataUploaded(
                    path="data/combined/loi/",
                    placement=self.device.PlacementID,
                    timeline=timeline
                    )

    def isNewZoneCountUploaded(self,
            timeline=time.time() - 20*60):
        """check whether new zone-count data after timeline had been uploaded
        @param timeline: seconds since 1970.01.01.00.00.00
        """

        return self.isDataUploaded(
                    path="data/fragment/zone_count/dump/",
                    placement=self.device.PlacementID,
                    timeline=timeline
                    ) or self.isDataUploaded(
                    path="data/combined/zone_count/",
                    placement=self.device.PlacementID,
                    timeline=timeline
                    )

    def isNewTrackingUploaded(self,
            timeline=time.time() - 20*60):
        """check whether new tracking data after timeline had been uploaded
        @param timeline: seconds since 1970.01.01.00.00.00
        """

        return self.isDataUploaded(
                    path="data/fragment/tracking/dump/",
                    placement=self.device.PlacementID,
                    timeline=timeline
                    ) or self.isDataUploaded(
                    path="data/combined/tracking/",
                    placement=self.device.PlacementID,
                    timeline=timeline
                    )

    def isNewInstallUploaded(self,
            timeline=time.time() - 20*60):
        """check whether new install data after timeline had been uploaded
        @param timeline: seconds since 1970.01.01.00.00.00
        """
        return self.isDataUploaded(
                    path="data/fragment/install/dump/",
                    placement=self.device.PlacementID,
                    timeline=timeline
                    ) or self.isDataUploaded(
                    path="data/combined/install/",
                    placement=self.device.PlacementID,
                    timeline=timeline
                    )

    def isNewWifiUploaded(self,
            timeline=time.time() - 20*60):
        """check whether new wifi data after timeline had been uploaded
        @param timeline: seconds since 1970.01.01.00.00.00
        """
        return self.isDataUploaded(
                    path="data/fragment/wifi/dump/",
                    placement=self.device.PlacementID,
                    timeline=timeline
                    ) or self.isDataUploaded(
                    path="data/combined/wifi/",
                    placement=self.device.PlacementID,
                    timeline=timeline
                    )

    def isNewAudioUploaded(self,
            timeline=time.time() - 20*60):
        """check whether new audio data after timeline had been uploaded
        @param timeline: seconds since 1970.01.01.00.00.00
        """
        return self.isDataUploaded(
                    path="data/fragment/audio/dump/",
                    placement=self.device.PlacementID,
                    timeline=timeline
                    ) or self.isDataUploaded(
                    path="data/combined/audio/",
                    placement=self.device.PlacementID,
                    timeline=timeline
                    )

    def isDataUploaded(self, path, placement, timeline):
        """check whether new data after timeline had been uploadedi
        restrict: all files in gs dir are regular data files
        """
        dayStr = time.strftime("%Y-%m-%d", time.gmtime(timeline))
        _dayStr = time.strftime("%Y-%m-%d", time.gmtime(timeline+3600))#hander probably day changing
        timeStr = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime(timeline))

        if _dayStr != dayStr:
            _remoteFilterStr = path + placement + '/'\
                    + _dayStr + '/'
            _keys_list = list(self.bucket.list("%s" % _remoteFilterStr))
            _keys_list.sort()
            if _keys_list != []:
                return True

        remoteFilterStr = path + placement + '/'\
                + dayStr + '/'
        keys_list = list(self.bucket.list("%s" % remoteFilterStr))
        keys_list.sort()
        if keys_list != [] and \
                re.compile(r'\d{4}(-\d{2}){5}').search(keys_list[-1].name).group() >= timeStr:
            return True
        else:
            return False





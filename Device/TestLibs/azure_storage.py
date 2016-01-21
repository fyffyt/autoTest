#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import time
import json
from exceptions import *
import binascii
import inspect
from azure.storage.blob import BlobService
from azure.common import AzureHttpError, AzureConflictHttpError, AzureMissingResourceHttpError


from device import Device

class ASMonitor(object):
    """monitor for azure storage"""
    def __init__(self, dev=None):
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

        self.device = dev
        if self.device is None:
            self.container = "percolata-test"
            return

        hostname = self.device.getLocalCfg()['hostname']
        if hostname.__contains__("ci-api"):
            self.container = "percolata-test"
        elif hostname.__contains__("api"):
            self.container = "percolata-data"
        else:
            raise NotImplementedError("unsupported api" % hostname)

    def attachDev(self, dev):
        """set associate device for ASMonitor"""
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
            _remoteFilterStr = "as://" + self.container + '/' + path + placement + '/'\
                    + _dayStr + '/'
            _blob_list = self.azureService.get_list_of_remote_path(_remoteFilterStr)
            _blob_list.sort()
            if _blob_list != []:
                return True

        remoteFilterStr = "as://" + self.container + '/' + path + placement + '/'\
                + dayStr + '/'
        blob_list = self.azureService.get_list_of_remote_path(remoteFilterStr)
        blob_list.sort()
        if blob_list != [] and \
                re.compile(r'\d{4}(-\d{2}){5}').search(blob_list[-1].name).group() >= timeStr:
            return True
        else:
            return False


class AzureManager(object):
    REGEX_REMOTE_PATH = "as://([a-z0-9]+[a-z0-9\.-]*[a-z0-9]+)/(\S*)"
    INDEX = "as://"

    def __init__(self, account_name, account_key):
        """
        try:
            self.azure_worker = BlobService(account_name,account_key)
        except Exception as e:
            return 'error msg '+str(e)
        """
        self.azure_worker = BlobService(account_name, account_key)

    def create_container(self, container_name, public_access=False):
        """
        Container names must start with a letter or number, and can contain only letters, numbers, and the dash (-) character.
        Every dash (-) character must be immediately preceded and followed by a letter or number; consecutive dashes are not permitted in container names.
        All letters in a container name must be lowercase.
        Container names must be from 3 through 63 characters long.
        """
        if public_access:
            self.azure_worker.create_container(container_name, x_ms_blob_public_access='container')
        else:
            self.azure_worker.create_container(container_name)

    def delete_container(self, container_name):
        """
        delete container
        :param container_name:
        :return:
        """
        self.azure_worker.delete_container(container_name)

    def check_if_exists_file(self, remote_path):
        """
        Check if exists blob
        :param remote_path: eg. as://percolata-test/floader/file.txt
        :return: True or False
        """
        container_name, path = re.search(AzureManager.REGEX_REMOTE_PATH, remote_path).groups()
        try:
            self.azure_worker.get_blob_properties(container_name, path)
        except AzureMissingResourceHttpError:
            return False
        return True

    def upload_to_container_from_path(self, remote_path, source_path):
        # remote path is like percolata-test/config/8600125.json
        container_name, path = re.search(AzureManager.REGEX_REMOTE_PATH, remote_path).groups()
        self.azure_worker.put_block_blob_from_path(
                container_name,
                path,
                source_path
        )

    def upload_to_container_from_file(self, remote_path, fp):
        # remote path is like percolata-test/config/8600125.json
        # e.g. fp = open('uploads/image.png')
        container_name, path = re.search(AzureManager.REGEX_REMOTE_PATH, remote_path).groups()
        self.azure_worker.put_block_blob_from_file(
                container_name,
                path,
                fp
        )

    def upload_to_container_from_text(self, remote_path, text):
        # remote path is like percolata-test/config/8600125.json
        container_name, path = re.search(AzureManager.REGEX_REMOTE_PATH, remote_path).groups()
        self.azure_worker.put_block_blob_from_bytes(
                container_name,
                path,
                text
        )

    def upload_dir_to_container(self, remote_path, local_path):
        """
        eg.
            remote_path: as://percolata-test/test
            local_path; /tmp/folder
            then local folder /tmp/ will be uploaded to as://percolata-test/test/folder
        :param remote_path: eg. as://percolata-test/config
        :param local_path:
        :return:
        """
        local_path = os.path.abspath(local_path)
        base_folder = os.path.dirname(local_path)
        local_remote_path = []
        for root, sub_root, file_names in os.walk(local_path):
            for file_name in file_names:
                local_path = os.path.join(root, file_name)
                whole_remote_path = os.path.join( \
                        remote_path, \
                        re.search("%s(\S+)" % base_folder, local_path).groups()[0][1:] \
                    )
                local_remote_path.append([local_path, whole_remote_path])
        for paths in local_remote_path:
            self.upload_to_container_from_path(paths[1], paths[0])

    def download_to_local_path(self, remote_path, local_path):
        # remote path is like percolata-test/config/8600125.json
        container_name, path = re.search(AzureManager.REGEX_REMOTE_PATH, remote_path).groups()
        try:
            self.azure_worker.get_blob_to_path(
                    container_name,
                    path,
                    local_path
            )
        except AzureMissingResourceHttpError as e:
            raise NoSuchFileOnStorage(str(e))

    def get_text_from_container(self, remote_path):
        # remote path is like percolata-test/config/8600125.json
        container_name, path = re.search(AzureManager.REGEX_REMOTE_PATH, remote_path).groups()
        try:
            content = self.azure_worker.get_blob_to_bytes(
                    container_name,
                    path
            )
        except AzureMissingResourceHttpError as e:
            raise NoSuchFileOnStorage(str(e))
        return content

    def get_list_of_remote_path(self, remote_path):
        # remote path is like percolata-test/config/8600125.json
        # tmp_index = remote_path.find('/')
        # container_name =  remote_path[:tmp_index]
        # if '/' not in remote_path or remote_path.endswith('/'):
        #     path = '/'
        # else:
        #     path = remote_path[tmp_index+1:]
        container_name, path = re.search(AzureManager.REGEX_REMOTE_PATH, remote_path).groups()
        if path == "":
            path = None
        results = self.azure_worker.list_blobs(
                container_name,
                prefix=path
        )
        blobs_list = []
        for r in results:
            if r.name.endswith("/"):
                continue
            blobs_list.append(os.path.join(AzureManager.INDEX, container_name, r.name))
        return blobs_list

    def download_dir_to_local(self, remote_path, local_path):
        """
        1. download  directory to local
        eg.
            remote_path: as://percolata-test/test
            local_path; /tmp/
            then you will find percolata-test/test in local /tmp/test

        2. download a container to local
            remote_path: as://percolata-test/
            local_path; /tmp/
            then you will find percolata-test/test in local /tmp/percolata-test
        :param remote_path:
        :param local_path:
        :return:
        """
        for path in self.get_list_of_remote_path(remote_path):
            format_path = os.path.normpath(path)
            format_prefix_path = os.path.dirname(os.path.normpath(remote_path))
            match = re.match("%s/(\S*)$" % format_prefix_path, format_path)
            if match is None:
                raise InvalidStoragePath("download '%s' failed" % path)
            save_path = os.path.join(local_path, match.groups()[0])
            file_dir = os.path.dirname(save_path)
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            self.download_to_local_path(path, save_path)

    def delete_file_on_container(self, remote_path):
        # tmp_index = remote_path.find('/')
        # container_name =  remote_path[:tmp_index]
        # path = remote_path[tmp_index+1:]
        container_name, path = re.search(AzureManager.REGEX_REMOTE_PATH, remote_path).groups()
        try:
            self.azure_worker.delete_blob(container_name, path)
        except AzureMissingResourceHttpError as e:
            pass

    def delete_folder_on_container(self, remote_path):
        """
        delete folder on container
        :param remote_path: eg. as://percolata-test/folder
        :return:
        """
        for path in self.get_list_of_remote_path(remote_path):
            self.delete_file_on_container(path)

    def set_access_level(self, container_name, access_level):
        # if the access_level is 'blob',
        # Blob data within this container can be read via anonymous request,
        # but container data is not available. Clients cannot enumerate blobs within the container via anonymous request.
        self.azure_worker.set_container_acl(container_name, x_ms_blob_public_access='access_level')

    def get_file_md5(self, remote_path):
        """
        get md5 of file
        :param remote_path: eg. as://percolata-test/floder/file.txt
        :return: md5 string
        """
        container_name, path = re.search(AzureManager.REGEX_REMOTE_PATH, remote_path).groups()
        try:
            blob_properties = self.azure_worker.get_blob_properties(container_name, path)
        except AzureMissingResourceHttpError as e:
            raise NoSuchFileOnStorage(str(e))
        md5_base64 = blob_properties['content-md5']
        md5 = binascii.hexlify(md5_base64.decode("base64"))
        return md5

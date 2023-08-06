#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   upload_session.py
@Author  :   Raighne.Weng
@Version :   0.1.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Asset Upload Session
'''

import os
import mimetypes
import struct
from os.path import exists
from requests import request
import google_crc32c
from datature import error, logger
from datature.http.resource import RESTResource
from datature.rest.operation import Operation


class UploadSession(RESTResource):
    """Datature Asset Upload Session Class."""

    def __init__(self):
        self.assets = []
        self.file_name_map = {}

    def add(self, file_path: str):
        """Add asset to upload."""
        if not exists(file_path):
            raise error.Error("Could not find the Asset file")

        with open(file_path, 'rb') as file:
            contents = file.read()

            # calculate file crc32
            file_hash = google_crc32c.Checksum()
            file_hash.update(contents)

            # To fix the wrong crc32 caused by mac M1 clip
            crc32 = struct.unpack(">l", file_hash.digest())[0]

            # Prepare filename size and mime type
            filenmae = os.path.basename(file_path)
            size = os.path.getsize(file_path)
            mime = mimetypes.guess_type(filenmae)[0]

            file.close()

            if self.file_name_map.get(filenmae) is not None:
                raise error.Error("File already Exist")

            if (filenmae and size and crc32 and mime):
                metadata = {
                    "filename": filenmae,
                    "size": size,
                    "crc32c": crc32,
                    "mime": mime
                }
                self.assets.append(metadata)
                self.file_name_map[filenmae] = {"path": file_path}

                logger.log_info("Add asset:", metadata=metadata)
            else:
                raise error.Error("UnSupported Asset file")

    def start(self, early_return=True) -> dict:
        """Request server to get signed ur and upload file to gcp."""

        # check asset length
        if not self.assets:
            raise error.Error("Assets to upload is Empty")

        # call API to get signed url
        response = self.request("POST",
                                "/asset/uploadSession",
                                request_body={
                                    "cohorts": ["main"],
                                    "assets": self.assets
                                })

        op_link = response["op_link"]

        for asset_upload in response["assets"]:
            file_name = asset_upload["metadata"]["filename"]
            file_path = self.file_name_map.get(file_name)["path"]

            with open(file_path, 'rb') as file:
                contents = file.read()

                logger.log_info("Start Uploading" + file_path)

                # upload asset to GCP one by one
                request("PUT",
                        asset_upload["upload"]["url"],
                        headers=asset_upload["upload"]["headers"],
                        data=contents,
                        timeout=10)
                logger.log_info("Done Uploading" + file_path)

        if early_return:
            return {"op_link": op_link}

        return Operation.loop_retrieve(op_link)

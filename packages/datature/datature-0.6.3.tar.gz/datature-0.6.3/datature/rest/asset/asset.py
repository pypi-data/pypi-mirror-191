#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   asset.py
@Author  :   Raighne.Weng
@Version :   0.1.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Asset API
'''

from datature.http.resource import RESTResource
from datature.rest.asset.upload_session import UploadSession
from datature.rest.types import Pagination, AssetMetadata


class Asset(RESTResource):
    """Datature Annotation API Resource."""

    @classmethod
    def list(cls, pagination: Pagination = None) -> dict:
        """Get a list of assets

        :param pagination: the pagination of retuen list
        :return: response json data
        """
        return cls.request("GET", "/asset/list", query=pagination)

    @classmethod
    def retrieve(cls, asset_id: str) -> dict:
        """Get an asset

        :param asset_id: the id of asset
        :return: response json data
        """
        return cls.request("GET", f"/asset/{asset_id}")

    @classmethod
    def modify(cls, asset_id: str, asset_meta: AssetMetadata) -> dict:
        """Update an asset

        :param asset_id: the id of asset
        :param asset_meta: the metadata of asset
        :return: response json data
        """
        return cls.request("PUT",
                           f"/asset/{asset_id}",
                           request_body=asset_meta)

    @classmethod
    def delete(cls, asset_id: str) -> dict:
        """Delete a asset

        :param asset_id: the id of asset
        :return: response json data
        """
        return cls.request("DELETE", f"/asset/{asset_id}")

    @classmethod
    def upload_session(cls) -> dict:
        """Bulk update assets

        :return: UploadSession class
        """
        return UploadSession()

#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   tag.py
@Author  :   Raighne.Weng
@Version :   0.2.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Tag API
'''
from datature.http.resource import RESTResource


class Tag(RESTResource):
    """Datature Tag API Resource."""

    @classmethod
    def list(cls) -> dict:
        """List tags.

        :return: response json data
        """
        return cls.request("GET", "/tag/list")

    @classmethod
    def create(cls, name: str) -> dict:
        """Create a new tag.

        :return: response json data
        """
        return cls.request("POST", "/tag", request_body={"name": name})

    @classmethod
    def modify(cls, index: int, name: str) -> dict:
        """Update a tag.

        :return: response json data
        """
        return cls.request("PUT", f"/tag/{index}", request_body={"name": name})

    @classmethod
    def delete(cls, index: int) -> dict:
        """Delete a tag.

        :return: response json data
        """
        return cls.request("DELETE", f"/tag/{index}")

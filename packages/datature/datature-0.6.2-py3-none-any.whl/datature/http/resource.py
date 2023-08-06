#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   resource.py
@Author  :   Raighne.Weng
@Version :   0.1.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Base class for REST API resources
'''

from datature.http.requester import Requester


# pylint: disable=R0913,R0903
class RESTResource():
    """Datatue REST resource."""

    @classmethod
    def request(cls,
                method,
                url,
                query=None,
                request_body=None,
                request_headers=None,
                request_files=None):
        """Create a REST resource and make the http call."""

        response = Requester().request(method, url, query, request_body,
                                       request_headers, request_files)

        return response

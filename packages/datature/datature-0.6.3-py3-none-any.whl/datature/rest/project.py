#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   project.py
@Author  :   Raighne.Weng
@Version :   0.1.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Project API
'''

from datature.http.resource import RESTResource
from datature.rest.types import ProjectMetadata


class Project(RESTResource):
    """Datature Project API Resource."""

    @classmethod
    def retrieve(cls) -> dict:
        """Get a project.

        :return: response json data
        """
        return cls.request("GET", "/project")

    @classmethod
    def modify(cls, project: ProjectMetadata) -> dict:
        """Update a project.

        :return: response json data
        """
        return cls.request("PUT", "/project", request_body=project)

    @classmethod
    def quota(cls) -> dict:
        """Get project quota.

        :return: response json data
        """
        return cls.request("GET", "/project/quota")

    @classmethod
    def insight(cls) -> dict:
        """Get project insight.

        :return: response json data
        """
        return cls.request("GET", "/project/insight")

    @classmethod
    def users(cls) -> dict:
        """Get project users.

        :return: response json data
        """
        return cls.request("GET", "/project/users")

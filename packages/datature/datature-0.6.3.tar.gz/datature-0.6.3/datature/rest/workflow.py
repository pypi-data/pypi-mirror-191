#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   workflow.py
@Author  :   Raighne.Weng
@Version :   0.3.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Workflow API
'''

from datature.http.resource import RESTResource
from datature.rest.types import FlowMetadata


class Workflow(RESTResource):
    """Datature Workflow API Resource."""

    @classmethod
    def list(cls) -> dict:
        """List all workflows.

        :return: response json data
        """
        return cls.request("GET", "/workflow/list")

    @classmethod
    def retrieve(cls, flow_id: str) -> dict:
        """Get a workflow.

        :return: response json data
        """
        return cls.request("GET", f"/workflow/{flow_id}")

    @classmethod
    def modify(cls, flow_id: str, flow: FlowMetadata) -> dict:
        """Update a workflow.

        :return: response json data
        """
        return cls.request("PUT", f"/workflow/{flow_id}", request_body=flow)

    @classmethod
    def delete(cls, flow_id: str) -> dict:
        """Delete a workflow.

        :return: response json data
        """
        return cls.request("DELETE", f"/workflow/{flow_id}")

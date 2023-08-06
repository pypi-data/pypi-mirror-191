#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   artifact.py
@Author  :   Raighne.Weng
@Version :   0.4.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Artifact API
'''

from datature.http.resource import RESTResource


class Artifact(RESTResource):
    """Datature Artifact API Resource."""

    @classmethod
    def list(cls) -> dict:
        """List all artifacts.

        :return: response json data
        """
        return cls.request("GET", "/artifact/list")

    @classmethod
    def retrieve(cls, artifact_id: str) -> dict:
        """Get a artifact.

        :return: response json data
        """
        return cls.request("GET", f"/artifact/{artifact_id}")

    @classmethod
    def list_exported(cls, artifact_id: str) -> dict:
        """List artifact exported models.

        :return: response json data
        """
        return cls.request("GET", f"/artifact/{artifact_id}/models")

    @classmethod
    def export_model(cls, artifact_id: str, model_format: str) -> dict:
        """Create a export of artifact model.

        :return: response json data
        """
        return cls.request("POST",
                           f"/artifact/{artifact_id}/export",
                           request_body={"format": model_format})

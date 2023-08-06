#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   Deploy.py
@Author  :   Raighne.Weng
@Version :   0.5.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Deploy API
'''

from datature.http.resource import RESTResource
from datature.rest.types import DeploymentMetadata


class Deploy(RESTResource):
    """Datature Deploy API Resource."""

    @classmethod
    def list(cls) -> dict:
        """List all deployments.

        :return: response json data
        """
        return cls.request("GET", "/deploy/list")

    @classmethod
    def retrieve(cls, deploy_id: str) -> dict:
        """Retrieve a deployment.

        :deploy_id the id of the deployment
        :return: response json data
        """
        return cls.request("GET", f"/deploy/{deploy_id}")

    @classmethod
    def delete(cls, deploy_id: str) -> dict:
        """Delete a deployment by deploy_id.

        :deploy_id the id of the deployment
        :return: response json data
        """
        return cls.request("DELETE", f"/deploy/{deploy_id}")

    @classmethod
    def create(cls, deployment: DeploymentMetadata) -> dict:
        """create a deployment.

        :deployment the metadata of the deployment
        :return: response json data
        """
        return cls.request("POST",
                           "/deploy",
                           request_body={
                               "name": deployment.get("name"),
                               "modelId": deployment.get("model_id"),
                               "numInstances":
                               deployment.get("num_of_instances"),
                           })

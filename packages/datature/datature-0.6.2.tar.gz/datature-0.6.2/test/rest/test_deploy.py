#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   test_deploy.py
@Author  :   Raighne.Weng
@Version :   0.5.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Deploy API Test Cases
'''

import unittest
from unittest.mock import MagicMock
from datature.rest.deploy import Deploy


class TestDeploy(unittest.TestCase):
    """Datature Deploy API Resource Teset Cases."""

    def test_list(self):
        """Test list all deployments."""
        Deploy.request = MagicMock()

        Deploy.list()

        Deploy.request.assert_called_once_with("GET", "/deploy/list")

    def test_retrieve(self):
        """Test retrieve a deployment."""
        Deploy.request = MagicMock()

        Deploy.retrieve("deploy_id")

        Deploy.request.assert_called_once_with("GET", "/deploy/deploy_id")

    def test_delete(self):
        """Test delete a deployment."""
        Deploy.request = MagicMock()

        Deploy.delete("deploy_id")

        Deploy.request.assert_called_once_with("DELETE", "/deploy/deploy_id")

    def test_create(self):
        """Test create a deployment."""
        Deploy.request = MagicMock()

        Deploy.create({
            "name": "name",
            "model_id": "model_id",
            "num_of_instances": 1
        })

        Deploy.request.assert_called_once_with("POST",
                                               "/deploy",
                                               request_body={
                                                   "name": "name",
                                                   "modelId": "model_id",
                                                   "numInstances": 1
                                               })

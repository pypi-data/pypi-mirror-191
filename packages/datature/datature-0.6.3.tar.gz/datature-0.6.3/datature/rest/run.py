#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   run.py
@Author  :   Raighne.Weng
@Version :   0.6.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Run API
'''
from datature.http.resource import RESTResource
from datature.rest.types import RunSetupMetadata


class Run(RESTResource):
    """Datature Run API Resource."""

    @classmethod
    def list(cls) -> dict:
        """List trainings.

        :return: response json data
        """
        return cls.request("GET", "/run/list")

    @classmethod
    def retrieve(cls, run_id: str) -> dict:
        """Retrieve one training.

        :run_id: the id of the training.
        :return: response json data
        """
        return cls.request("GET", f"/run/{run_id}")

    @classmethod
    def kill(cls, run_id: str) -> dict:
        """Kill a training.

        :param run_id: the id of the training.
        :return: response json data
        """
        return cls.request("PUT",
                           f"/run/{run_id}",
                           request_body={"status": "killed"})

    @classmethod
    def delete(cls, run_id: int) -> dict:
        """Delete a Run.

        :param run_id: the id of the training.
        :return: response json data
        """
        return cls.request("DELETE", f"/run/{run_id}")

    @classmethod
    def start(cls, flow_id: str, setup: RunSetupMetadata) -> dict:
        """start a new training.

        :param flow_id: the id of the flow.
        :param setup: the metedata of the training.
        :return: response json data
        """
        return cls.request(
            "POST",
            "/run",
            request_body={
                "flowId": flow_id,
                "execution": {
                    "accelerator": {
                        "name": setup.get("accelerator").get("name"),
                        "count": setup.get("accelerator").get("count"),
                    },
                    "checkpoint": {
                        "strategy":
                        setup.get("checkpoint").get("strategy"),
                        "evaluationInterval":
                        setup.get("checkpoint").get("evaluation_interval"),
                        "metric":
                        setup.get("checkpoint").get("metric"),
                    },
                },
                "features": {
                    "preview": setup.get("preview")
                }
            })

    @classmethod
    def log(cls, log_id: str) -> dict:
        """Retrieve training logs.

        :param log_id: the id of the log.
        :return: response json data
        """
        return cls.request("GET", f"/run/log/{log_id}")

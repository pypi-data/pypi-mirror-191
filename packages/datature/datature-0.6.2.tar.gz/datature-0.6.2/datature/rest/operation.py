#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   operation.py
@Author  :   Raighne.Weng
@Version :   0.1.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Operation API
'''

import time
from datature.http.resource import RESTResource
from datature import error, logger
import datature


class Operation(RESTResource):
    """Datature Operation API Resource."""

    @classmethod
    def retrieve(cls, op_link: str) -> dict:
        """Get a operation.

        :param op_link: the operation link
        :return: response json data
        """
        return cls.request("GET", "/operation", query={"opLink": op_link})

    @classmethod
    def loop_retrieve(
            cls,
            op_link: str,
            loop_times: int = datature.OPERATION_LOOPING_TIMES) -> dict:
        """Loop query a operation.

        :param op_link: the operation link
        :param loop_times: the operation link
        :return: response json data
        """
        for _ in range(loop_times):
            response = cls.request("GET",
                                   "/operation",
                                   query={"opLink": op_link})

            logger.log_info("Operation status:", status=response["status"])

            if response["status"]["overview"] == "Finished":
                return response

            if response["status"]["overview"] == "Errored":
                logger.log_info("Operation error: please contacts our support")
                raise error.BadRequestError(
                    "Operation error: please contacts our support")

            time.sleep(datature.OPERATION_LOOPING_DELAY_SECONDS)
        return None

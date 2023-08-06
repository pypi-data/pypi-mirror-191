#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   annotation.py
@Author  :   Raighne.Weng
@Version :   0.1.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Annotation API
'''

from os.path import exists
from datature.error import Error
from datature.http.resource import RESTResource
from datature.rest.operation import Operation
from datature.rest.types import (AnnotationFormat, AnnotationMetadata,
                                 AnnotationExportOptions)


class Annotation(RESTResource):
    """Datature Annotation API Resource."""

    @classmethod
    def list(cls, asset_id: str) -> dict:
        """Get a list of annotations

        :param asset_id: the id of asset
        :return: response json data
        """
        return cls.request("GET", f"/annotation/list/{asset_id}")

    @classmethod
    def create(cls, annotation: AnnotationMetadata) -> dict:
        """Create an annotations

        :param annotation: AnnotationMetadata
        :return: response json data
        """

        return cls.request("POST",
                           "/annotation",
                           request_body={
                               "assetId": annotation.get("asset_id"),
                               "tag": annotation.get("tag"),
                               "boundType": annotation.get("bound_type"),
                               "bound": annotation.get("bound")
                           })

    @classmethod
    def retrieve(cls, annotation_id: str) -> dict:
        """Get an annotation

        :param annotation_id: the id of annotation
        :return: response json data
        """
        return cls.request("GET", f"/annotation/{annotation_id}")

    @classmethod
    def delete(cls, annotation_id: str) -> dict:
        """Delete an annotation

        :param annotation_id: the id of annotation
        :return: response json data
        """
        return cls.request("DELETE", f"/annotation/{annotation_id}")

    @classmethod
    def export(cls,
               annotation_format: AnnotationFormat,
               export_options: AnnotationExportOptions,
               early_return=True) -> dict:
        """Export all annotations

        :param annotation_format: the format of annotation
        :param export_options: the options of export
        :param early_return: if need wait server process
        :return: response json data
        """
        response = cls.request("POST",
                               "/annotation/export",
                               query={"format": annotation_format},
                               request_body={
                                   "options": {
                                       "splitRatio":
                                       export_options.get("split_ratio"),
                                       "seed":
                                       export_options.get("seed"),
                                       "normalized":
                                       export_options.get("normalized"),
                                       "shuffle":
                                       export_options.get("shuffle")
                                   }
                               })

        if early_return:
            return response

        op_link = response["op_link"]
        return Operation.loop_retrieve(op_link)

    @classmethod
    def retrieve_exported_file(cls, op_id: str) -> dict:
        """Retrieve exported download link

        :param op_id: the id of exported operation
        :return: response json data
        """
        return cls.request("GET", f"/annotation/export/{op_id}")

    @classmethod
    def upload(cls,
               annotation_format: AnnotationFormat,
               file_path: str,
               early_return=True) -> dict:
        """Import annotations


        :param annotation_format: the format of annotation
        :param file_path: the path of imported file
        :param early_return: if need wait server process
        :return: response json data
        """
        file_exists = exists(file_path)

        if not file_exists:
            raise Error("Could not find the Asset file")

        with open(file_path, "rb") as file:
            files = [('files', file)]

            response = cls.request(
                "POST",
                "/annotation/import",
                query={"format": annotation_format},
                request_files=files,
            )

            if early_return:
                return response

            op_link = response["op_link"]
            return Operation.loop_retrieve(op_link)

#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   types.py
@Author  :   Raighne.Weng
@Version :   0.6.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Types for Datature API resources.
'''

from dataclasses import dataclass
from enum import Enum


@dataclass
class ProjectMetadata:
    """Project metadata."""

    name: str


@dataclass
class AnnotationMetadata:
    """Annotation metadata."""

    asset_id: str
    tag: str
    bound_type: str
    bound: list


@dataclass
class AnnotationExportOptions:
    """Annotation exported options."""

    split_ratio: int
    seed: int
    normalized: bool = True
    shuffle: bool = True


@dataclass
class Pagination:
    """Pagination Params."""

    page: str
    limit: int = 10


@dataclass
class AssetMetadata:
    """Asset Metadata."""

    status: str


class AnnotationFormat(Enum):
    """Annotation CSV Format."""

    CSV_FOURCORNER = "csv_fourcorner"
    CSV_WIDTHHEIGHT = "csv_widthheight"
    COCO = "coco"
    PASCAL_VOC = "pascal_voc"
    YOLO_KERAS_PYTORCH = "yolo_keras_pytorch"
    YOLO_DARKNET = "yolo_darknet"
    POLYGON_SINGLE = "polygon_single"
    POLYGON_COCO = "polygon_coco"


@dataclass
class FlowMetadata:
    """Asset Metadata."""

    title: str


@dataclass
class DeploymentMetadata:
    """Asset Metadata."""

    name: str
    model_id: str
    num_of_instances: int = 1


@dataclass
class Accelerator:
    """Run Accelerator Metadata."""

    name: str
    count: int = 1


@dataclass
class Checkpoint:
    """Run Checkpoint Metadata."""

    strategy: str
    metric: str
    evaluation_interval: int = 1


@dataclass
class Limit:
    """Run Checkpoint Metadata."""

    metric: str
    value: int = 1


@dataclass
class RunSetupMetadata:
    """The settings to start a training."""

    accelerator: Accelerator
    checkpoint: Checkpoint
    preview: bool = True

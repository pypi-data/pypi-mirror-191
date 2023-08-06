#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   __init__.py
@Author  :   Raighne.Weng
@Version :   0.6.1
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   init module, include global configuration
'''

# Global Configuration
API_BASE_URL = "https://api.datature.io/v1"
OPERATION_LOOPING_DELAY_SECONDS = 15
HTTP_TIMEOUT_SECONDS = 120

# for max looping time
OPERATION_LOOPING_TIMES = 8

# Set to either 'debug' or 'info'
LOG_LEVEL = None

# pylint: disable=C0103
project_secret = None

# API resources
# pylint: disable=C0413
from datature.rest import *

#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   setip.py
@Author  :   Raighne.Weng
@Version :   0.6.2
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Setup module
'''

import setuptools

setuptools.setup(name="datature",
                 version="0.6.2",
                 author="Raighne Weng",
                 author_email="raighne@datature.io",
                 long_description_content_type="text/markdown",
                 description="Python bindings for the Datature API",
                 packages=setuptools.find_namespace_packages(),
                 python_requires=">=3.7",
                 install_requires=["requests", "google-crc32c", "pyhumps"])

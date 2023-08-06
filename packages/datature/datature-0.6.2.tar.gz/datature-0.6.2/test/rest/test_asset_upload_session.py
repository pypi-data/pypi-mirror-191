#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   test_asset_upload_session.py
@Author  :   Raighne.Weng
@Version :   0.1.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Asset Upload Session API Test Cases
'''

import unittest
from unittest.mock import MagicMock, patch
from test.fixture.data import upload_session_fixture
from datature.rest.asset.upload_session import UploadSession
from datature.error import Error


class TestAssetUploadSession(unittest.TestCase):
    """Datature Asset Upload Session API Resource Teset Cases."""

    def test_add_with_file_not_exist(self):
        """Test add asset to upload with ."""
        upload_session = UploadSession()
        try:
            upload_session.add("assetPath")
        # pylint: disable=W0703
        except Exception as exception:
            assert isinstance(exception, Error)

    @patch("datature.rest.asset.upload_session.mimetypes")
    @patch("datature.rest.asset.upload_session.os")
    @patch("datature.rest.asset.upload_session.struct")
    @patch("datature.rest.asset.upload_session.google_crc32c")
    @patch("datature.rest.asset.upload_session.exists")
    @patch("datature.rest.asset.upload_session.open")
    # pylint: disable=W0613,R0913,C0103
    def test_add_with_duplicated_file(self, patch_open, patch_exist,
                                      google_crc32c, struct, os, mimetypes):
        """Test add asset to upload with duplicated file."""
        upload_session = UploadSession()
        upload_session.file_name_map = {"assetName": {"path": "file_path"}}

        struct.unpack.return_value = [-384617082]
        os.path.basename.return_value = "assetName"
        os.path.getsize.return_value = 5613
        mimetypes.guess_type.return_value = ["image/jpeg"]

        try:
            upload_session.add("assetPath")
        # pylint: disable=W0703
        except Exception as exception:
            assert isinstance(exception, Error)

    @patch("datature.rest.asset.upload_session.mimetypes")
    @patch("datature.rest.asset.upload_session.os")
    @patch("datature.rest.asset.upload_session.struct")
    @patch("datature.rest.asset.upload_session.google_crc32c")
    @patch("datature.rest.asset.upload_session.exists")
    @patch("datature.rest.asset.upload_session.open")
    # pylint: disable=W0613,R0913,C0103
    def test_add_with_file_not_supported(self, patch_open, patch_exist,
                                         google_crc32c, struct, os, mimetypes):
        """Test add asset to upload with file not supported."""
        upload_session = UploadSession()

        struct.unpack.return_value = [-384617082]
        os.path.basename.return_value = "assetName"
        os.path.getsize.return_value = 5613
        mimetypes.guess_type.return_value = [""]

        try:
            upload_session.add("assetPath")
        # pylint: disable=W0703
        except Exception as exception:
            assert isinstance(exception, Error)

    @patch("datature.rest.asset.upload_session.mimetypes")
    @patch("datature.rest.asset.upload_session.os")
    @patch("datature.rest.asset.upload_session.struct")
    @patch("datature.rest.asset.upload_session.google_crc32c")
    @patch("datature.rest.asset.upload_session.exists")
    @patch("datature.rest.asset.upload_session.open")
    # pylint: disable=W0613,R0913,C0103
    def test_add_with_file(self, patch_open, patch_exist, google_crc32c,
                           struct, os, mimetypes):
        """Test add asset to upload with file."""
        upload_session = UploadSession()

        struct.unpack.return_value = [-384617082]
        os.path.basename.return_value = "assetName"
        os.path.getsize.return_value = 5613
        mimetypes.guess_type.return_value = ["image/jpeg"]

        upload_session.add("assetPath")

    def test_start_with_empty_assets(self):
        """Test start upload with empty assets ."""
        upload_session = UploadSession()

        try:
            upload_session.start()
        # pylint: disable=W0703
        except Exception as exception:
            assert isinstance(exception, Error)

    @patch("datature.rest.asset.upload_session.request")
    @patch("datature.rest.asset.upload_session.open")
    # pylint: disable=W0613
    def test_start_with_early_return(self, patch_open, patch_request):
        """Test start upload with empty assets ."""
        upload_session = UploadSession()
        upload_session.assets = [{
            "filename": "test.jpeg",
            "mime": "image/jpeg",
            "size": 5613,
            "crc32c": -384617082
        }]
        upload_session.file_name_map = {"test.jpeg": {"path": "file_path"}}
        upload_session.request = MagicMock()

        upload_session.request.side_effect = [
            upload_session_fixture.upload_assets_response
        ]

        upload_session.assets = [{
            "filename": "test.jpeg",
            "mime": "image/jpeg",
            "size": 5613,
            "crc32c": -384617082
        }]

        upload_session.start()

    @patch("datature.rest.asset.upload_session.Operation")
    @patch("datature.rest.asset.upload_session.request")
    @patch("datature.rest.asset.upload_session.open")
    # pylint: disable=W0613
    def test_start_with_no_early_return(self, patch_open, patch_request,
                                        operation):
        """Test start upload with empty assets ."""
        upload_session = UploadSession()
        upload_session.assets = [{
            "filename": "test.jpeg",
            "mime": "image/jpeg",
            "size": 5613,
            "crc32c": -384617082
        }]
        upload_session.file_name_map = {"test.jpeg": {"path": "file_path"}}
        upload_session.request = MagicMock()

        upload_session.request.side_effect = [
            upload_session_fixture.upload_assets_response
        ]

        upload_session.assets = [{
            "filename": "test.jpeg",
            "mime": "image/jpeg",
            "size": 5613,
            "crc32c": -384617082
        }]

        upload_session.start(early_return=False)

        operation.loop_retrieve.assert_called()

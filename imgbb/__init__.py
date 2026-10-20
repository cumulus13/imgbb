#!/usr/bin/env python3

# File: imgbb/__init__.py
# Author: Hadi Cahyadi <cumulus13@gmail.com>
# Date: 2026-10-21
# Description: ImgBB CLI and Library Package.
# License: MIT

"""ImgBB CLI and Library Package."""

from .core import ImgBBClient, upload_image

__version__ = "1.0.0"
__all__ = ["ImgBBClient", "upload_image"]
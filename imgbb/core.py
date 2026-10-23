#!/usr/bin/env python3

# File: imgbb/core.py
# Author: Hadi Cahyadi <cumulus13@gmail.com>
# Date: 2026-10-21
# Description: Core module for ImgBB API interaction.
# License: MIT

"""Core module for ImgBB API interaction."""

import os
import requests
from typing import Dict, Any, Optional

API_URL = "https://api.imgbb.com/1/upload"

class ImgBBError(Exception):
    """Custom exception for ImgBB operations."""
    pass

class ImgBBClient:
    """Client for uploading images to ImgBB."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the ImgBB client.
        Looks for IMGBB_API_KEY environment variable if api_key is not provided.
        """
        self.api_key = os.getenv("IMGBB_API_KEY", api_key)
        if not self.api_key:
            raise ImgBBError(
                "API key not found. Pass it explicitly or set the IMGBB_API_KEY environment variable."
            )

    def upload(
        self, 
        image_path: str, 
        expiration: Optional[int] = None, 
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload an image file to ImgBB with optional progress tracking.
        
        :param image_path: Path to the image file.
        :param expiration: Time in seconds before the image is deleted (optional).
        :param name: Filename of the uploaded image (optional).
        :param progress_callback: Function to report upload progress (bytes_sent, total_bytes).
        :return: Dict containing response data from ImgBB.
        """
        if not os.path.exists(image_path):
            raise ImgBBError(f"Image file not found: {image_path}")

        try:
            with open(image_path, "rb") as file:
                files = {"image": (os.path.basename(image_path), file)}
                data = {"key": self.api_key}
                
                if expiration:
                    data["expiration"] = str(expiration)
                if name:
                    data["name"] = name

                response = requests.post(API_URL, data=data, files=files, timeout=60)
                
                try:
                    res_json = response.json()
                except ValueError:
                    raise ImgBBError(f"Invalid response from server: {response.text}")

                if response.status_code != 200 or not res_json.get("success"):
                    error_msg = res_json.get("error", {}).get("message", "Unknown error occurred")
                    raise ImgBBError(f"Upload failed: {error_msg}")

                return res_json.get("data", {})

        except requests.RequestException as e:
            raise ImgBBError(f"Network error occurred: {e}")

def upload_image(image_path: str, api_key: Optional[str] = None, expiration: Optional[int] = None) -> Dict[str, Any]:
    """Helper function for quick uploads."""
    client = ImgBBClient(api_key=api_key)
    return client.upload(image_path, expiration=expiration)

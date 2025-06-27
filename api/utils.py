"""
api/utils.py
Author: bella918@bu.edu
Project: api/utils.py
Date: 2025-06-26

This module provides utility functions for the image processing application.
It includes functions to dynamically build image URLs based on the environment.

"""


from django.conf import settings

def build_image_url(request, image_field_url):
    """
    Build the full image URL depending on the environment.
    """
    if settings.DEBUG:
        return f"http://{request.get_host()}{image_field_url}"
    else:
        return image_field_url

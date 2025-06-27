"""
Author: bella918@bu.edu
Project: api/apps.py
Description: Django app configuration for the 'api' application.
Date: 2025-06-26
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Django configuration class for the 'api' app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

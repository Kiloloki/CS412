# File: apps.py
# Author: Bella WANG (bella918@bu.edu), 5/27/2025
# Description: App configuration for the "mini_fb" Django app.
#              Registers the app and sets default configurations.
from django.apps import AppConfig


class MiniFbConfig(AppConfig):
    """
    Configuration class for the mini_fb application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mini_fb'

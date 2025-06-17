# File: apps.py
# Author: bella918@bu.edu
# Date: 6/14/2025
# Description: Configuration class for the voter_analytics Django application.
#              Sets default auto field and application name.

from django.apps import AppConfig


class VoterAnalyticsConfig(AppConfig):
    """
    Configuration class for the VoterAnalytics application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voter_analytics'

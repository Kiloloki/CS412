"""
api/serializers.py

This module defines the serializers for the image processing application.
It provides serializers for UploadedImage, CropRegion, ProcessingLog, Tag, 
and UploadedImageTag models to enable JSON serialization for API endpoints.

Author: bella918@bu.edu
Project: api/serializers.py
Date: 2025-06-26
"""
from rest_framework import serializers
from .models import UploadedImage, CropRegion, ProcessingLog, Tag, UploadedImageTag

class UploadedImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the UploadedImage model.
    """
    class Meta:
        model = UploadedImage
        fields = '__all__'

class CropRegionSerializer(serializers.ModelSerializer):
    """
    Serializer for the CropRegion model.
    """
    class Meta:
        model = CropRegion
        fields = '__all__'

class ProcessingLogSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProcessingLog model.
    """
    class Meta:
        model = ProcessingLog
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tag model.
    """
    class Meta:
        model = Tag
        fields = '__all__'

class UploadedImageTagSerializer(serializers.ModelSerializer):
    """
    Serializer for the UploadedImageTag intermediate model.
    """
    class Meta:
        model = UploadedImageTag
        fields = '__all__'

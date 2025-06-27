"""
api/models.py

This module defines the database schema for the image processing application.
It includes models for uploaded images, cropping regions, processing logs, 
and a tagging system. Users can upload images, select crop regions, 
log processing operations, and assign tags to organize images.

Author: bella918@bu.edu
Date: 2025.6.17
"""

from django.db import models
from django.contrib.auth.models import User


class UploadedImage(models.Model):
    """
    Model representing an uploaded image and its optional processed version.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/')
    processed_image = models.ImageField(upload_to='processed/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} uploaded by {self.user or 'Anonymous'}"



class CropRegion(models.Model):
    """
    Model representing a rectangular region cropped from an uploaded image.

    """
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Crop for Image {self.image.id}"



class ProcessingLog(models.Model):
    """
    Model to log details of image processing tasks.
    """
    METHOD_CHOICES = [
        ('full', 'Full Image'),
        ('crop', 'Cropped Region'),
    ]
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField(null=True, blank=True)  # optional processing time
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.method.title()} processing of Image {self.image.id}"


class Tag(models.Model):
    """
    Model representing a unique keyword/tag for organizing images.
    """
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class UploadedImageTag(models.Model):
    """
    Intermediate model representing a many-to-many relationship 
    between images and tags.
    """
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('image', 'tag')

    def __str__(self):
        return f"Tag '{self.tag.name}' for Image {self.image.id}"

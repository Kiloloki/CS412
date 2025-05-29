# File: models.py
# Author: Bella WANG (bella918@bu.edu), 5/27/2025
# Description: Model definitions for the "mini_fb" Django app.
#              Defines the Profile model used to store user profile data.
from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    """
    Model representing a user profile.
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    email = models.EmailField()
    image_url = models.URLField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_status_messages(self):
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})
    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile.first_name} - {self.message[:30]}"
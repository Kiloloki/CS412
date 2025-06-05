# File: models.py
# Author: Bella WANG (bella918@bu.edu), 5/29/2025
# Description: Model definitions for the "mini_fb" Django app.
#              Includes the Profile and StatusMessage models.
#              Profile stores basic user information.
#              StatusMessage stores timestamped status updates linked to a Profile.
from django.db import models
from django.urls import reverse

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
        """
        Returns the full name of the profile.
        """
        return f"{self.first_name} {self.last_name}"
    
    def get_status_messages(self):
        """
        Returns a queryset of this profile's status messages, ordered by newest first.
        """
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        """
        Returns the absolute URL to this profile's detail page.
        """
        return reverse('show_profile', kwargs={'pk': self.pk})
    
class StatusMessage(models.Model):
    """
    Model representing a status message posted by a Profile.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string showing the profile's name and a preview of the message.
        """
        return f"{self.profile.first_name} - {self.message[:30]}"
    
    def get_images(self):
        return [si.image for si in self.statusimage_set.all()]
    

class Image(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/')
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"Image {self.id} for {self.profile}"


class StatusImage(models.Model):
    status_message = models.ForeignKey('StatusMessage', on_delete=models.CASCADE)
    image = models.ForeignKey('Image', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image {self.image.id} for Status {self.status_message.id}"
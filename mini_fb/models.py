# File: models.py
# Author: Bella WANG (bella918@bu.edu), 5/29/2025
# Description: Model definitions for the "mini_fb" Django app.
#              Includes the Profile and StatusMessage models.
#              Profile stores basic user information.
#              StatusMessage stores timestamped status updates linked to a Profile.
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User



class Profile(models.Model):
    """
    Model representing a user profile.
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    email = models.EmailField()
    image_url = models.URLField()
    image_file = models.ImageField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
    
    def get_friends(self):
        """
        Returns the friends to this profile's detail page.
        """
        friendships1 = Friend.objects.filter(profile1=self)
        friends1 = [friend.profile2 for friend in friendships1]

        friendships2 = Friend.objects.filter(profile2=self)
        friends2 = [friend.profile1 for friend in friendships2]

        return friends1 + friends2
    

    def add_friend(self, other):
        """
        add friend with two person.
        """
        if self == other:
            return

        if Friend.objects.filter(profile1=self, profile2=other).exists() or \
        Friend.objects.filter(profile1=other, profile2=self).exists():
            return 

        Friend.objects.create(profile1=self, profile2=other)
    
    def get_friend_suggestions(self):
        """
        return a list (or QuerySet) of possible friends for a Profile
        """
        all_profiles = Profile.objects.exclude(pk=self.pk)
        current_friends = self.get_friends()
        return all_profiles.exclude(pk__in=[p.pk for p in current_friends])
    
    def get_news_feed(self):
        """return a list (or QuerySet) of all StatusMessages for the profile on which 
        the method was called, as well as all of the friends of that profile.
        """
        from .models import StatusMessage
        friend_profiles = self.get_friends()
        all_profiles = friend_profiles + [self]

        return StatusMessage.objects.filter(profile__in=all_profiles).order_by('-timestamp')

    
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
        """
        Retrieve all images associated with this status message.

        Returns:
            list: A list of Image instances linked via StatusImage.
        """
        return [si.image for si in self.statusimage_set.all()]
    

class Image(models.Model):
    """
    Represents an uploaded image belonging to a user profile.
    """

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/')
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        """
        Return a string identifying the image and its owner.
        """
        return f"Image {self.id} for {self.profile}"


class StatusImage(models.Model):
    """
    Intermediate model linking status messages to uploaded images.
    """
    status_message = models.ForeignKey('StatusMessage', on_delete=models.CASCADE)
    image = models.ForeignKey('Image', on_delete=models.CASCADE)

    def __str__(self):
        """
        Return a string showing the relationship between image and status.
        """
        return f"Image {self.image.id} for Status {self.status_message.id}"
    
class Friend(models.Model):
    """Friends model to see the relationship"""
    profile1 = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='friendship_creator_set'
    )
    profile2 = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='friendship_receiver_set'
    )
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """
        Return a string showing the relationship between two people.
        """
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"
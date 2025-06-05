# File: form.py
# Author: Bella WANG (bella918@bu.edu), 5/29/2025
# Description: Defines Django ModelForm classes for the "mini_fb" app.
#              Includes forms for creating Profile and StatusMessage objects.

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    """
    Form for creating a new Profile instance.
    Includes fields for first name, last name, city, email, and image URL.
    """
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image_url']

class CreateStatusMessageForm(forms.ModelForm):
    """
    Form for creating a new StatusMessage instance.
    Includes a single field for the status message text.
    """
    class Meta:
        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):
    """
    Form for updating a new profile instance.
    Includes fields for city, email, and image_url.
    """
    class Meta:
        model = Profile
        fields = ['city', 'email', 'image_url']

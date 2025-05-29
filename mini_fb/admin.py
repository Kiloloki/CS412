# File: admin.py
# Author: Bella WANG (bella918@bu.edu), 5/27/2025
# Description: Admin configuration for the "mini_fb" Django app.
#              Registers the Profile model for Django admin interface.
from django.contrib import admin
from .models import StatusMessage

# Register your models here.
from .models import Profile

admin.site.register(Profile)
# register model

admin.site.register(StatusMessage)


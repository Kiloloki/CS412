#File: url.py
#Author: Bella WANG (bella918@bu.edu), 5/27/2025
#Description: URL configuration file for the "mini_fb" Django app.
#              Maps URL paths to corresponding view functions.

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
]
#File: url.py
#Author: Bella WANG (bella918@bu.edu), 5/29/2025
#Description: URL configuration file for the "mini_fb" Django app.
#              Maps URL paths to corresponding view functions.

from django.urls import path
from .views import (ShowNewsFeedView, ShowFriendSuggestionsView, AddFriendView, ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, UpdateStatusMessageView, DeleteStatusMessageView,)

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status'),
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile_page'),
    path('profile/<int:pk>/add_friend/<int:other_pk>/', AddFriendView.as_view(), name='add_friend'),
    path('profile/<int:pk>/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/<int:pk>/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),
]
#File: url.py
#Author: Bella WANG (bella918@bu.edu), 5/29/2025
#Description: URL configuration file for the "mini_fb" Django app.
#              Maps URL paths to corresponding view functions.

from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
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
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/confirmation/', TemplateView.as_view(template_name='mini_fb/logged_out.html'), name='logout_confirmation'),
]
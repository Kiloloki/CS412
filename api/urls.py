"""
api/urls.py

This module defines URL patterns for the image processing application.
It includes API endpoints, page routes, user authentication routes, 
and CRUD operations.

Author: bella918@bu.edu
Project: api/urls.py
Date: 2025-06-26
"""
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import HistoryListView

urlpatterns = [
    # Page views
    path('', views.home_view, name='home'),
    path('history/', HistoryListView.as_view(), name='history'),  
    path('search/', views.search_view, name='search'),

    # API
    path('api/upload/', views.upload_image, name='upload'),
    path('api/full_process/', views.process_full_image, name='full_process'),
    path('api/crop_process/', views.process_crop_region, name='crop_process'),

    path('api/add_tag/', views.add_tag_to_image, name='add_tag'),
    path('api/search_by_tag/', views.search_by_tag, name='search_by_tag'),


    path('api/delete_image/', views.delete_image, name='delete_image'), 

    # Authentication
    path('accounts/logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('accounts/register/', views.register_view, name='register'), 


    # Detail & Update
    path('image/<int:image_id>/', views.image_detail_view, name='image_detail'), 
    path('update_tag/<int:image_id>/', views.update_tag_view, name='update_tag'), 
]


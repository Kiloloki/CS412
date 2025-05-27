#File: url.py
#Author: Bella WANG (bella918@bu.edu), 5/23/2025
#Description: URL configuration file for the "Quote of the Day" Django app.
#              Maps URL paths to corresponding view functions.

from django.urls import path
from . import views


urlpatterns = [
    path(r'', views.quote, name='quote'),              # /
    path(r'quote/', views.quote, name='quote'),        # /quote
    path(r'show_all/', views.show_all, name='show_all'),
    path(r'about/', views.about, name='about'),
]

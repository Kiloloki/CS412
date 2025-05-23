#File: url.py
#Author: Bella WANG (bella918@bu.edu), 5/23/2025
#Description: URL configuration for the "Restaurant" Django app.
#              Maps URL paths to corresponding view functions.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('main/', views.main, name='main'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
]
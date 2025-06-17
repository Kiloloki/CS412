# File: urls.py
# Author: bella918@bu.edu
# Date: 6/14/2025
# Description: URL routing configuration for the voter_analytics app.
#              Maps URL paths to corresponding class-based views for listing,
#              viewing detail, and visualizing voter data.


from django.urls import path
from .views import VoterListView, VoterDetailView, VoterGraphsView

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter'),
    path('graphs/', VoterGraphsView.as_view(), name='graphs'),
]


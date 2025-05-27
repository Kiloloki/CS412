# File: views.py
# Author: Bella WANG (bella918@bu.edu), 5/27/2025
# Description: View definitions for the "mini_fb" Django app.
#              Includes class-based views to display individual profiles
#              and a list of all user profiles.
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView
from .models import Profile



# Create your views here.

class ShowProfilePageView(DetailView):
    """
    View to display a single user profile.

    Attributes:
        model (Profile): The model associated with this view.
        template_name (str): The path to the HTML template used to render the profile.
        context_object_name (str): The name used to refer to the profile in the template context.
    """
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class ShowAllProfilesView(ListView):
    """
    View to display a list of all user profiles.

    Attributes:
        model (Profile): The model associated with this view.
        template_name (str): The path to the HTML template used to render the profile list.
        context_object_name (str): The name used to refer to the profile list in the template context.
    """
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'




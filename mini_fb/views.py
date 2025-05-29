# File: views.py
# Author: Bella WANG (bella918@bu.edu), 5/29/2025
# Description: View definitions for the "mini_fb" Django app.
#              Includes class-based views for displaying individual profiles,
#              listing all profiles, creating new profiles, and posting status messages.
from django.shortcuts import render
from django.views.generic import DetailView,ListView
from .models import Profile, StatusMessage, Profile
from django.views.generic.edit import CreateView
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse



class ShowProfilePageView(DetailView):
    """
    View to display a single user profile.
    """
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class ShowAllProfilesView(ListView):
    """
    View to display a list of all user profiles.
    """
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class CreateProfileView(CreateView):
    """
    Create a new user profiles.
    """
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

class CreateStatusMessageView(CreateView):
    """
    Create a new status for a existing person.
    """
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        """
        Add the associated profile to the template context using the profile's primary key.
        """
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        """
        Set the profile of the status message before saving the form.
        """
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        """
        After successfully submitting the form, redirect to the profile's detail page.
        """
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})



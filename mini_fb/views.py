# File: views.py
# Author: Bella WANG (bella918@bu.edu), 5/27/2025
# Description: View definitions for the "mini_fb" Django app.
#              Includes class-based views to display individual profiles
#              and a list of all user profiles.
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView
from .models import Profile
from django.views.generic.edit import CreateView
from .forms import CreateProfileForm
from django.views.generic.edit import CreateView
from .models import StatusMessage, Profile
from .forms import CreateStatusMessageForm
from django.urls import reverse



# Create your views here.

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
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})



# File: views.py
# Author: Bella WANG (bella918@bu.edu), 5/29/2025
# Description: View definitions for the "mini_fb" Django app.
#              Includes class-based views for displaying individual profiles,
#              listing all profiles, creating new profiles, and posting status messages.
from django.shortcuts import render
from django.views.generic import DetailView,ListView
from .models import Profile, StatusMessage
from django.views.generic.edit import CreateView
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse
from .models import Image, StatusImage
from django.views.generic.edit import UpdateView
from .forms import UpdateProfileForm
from django.views.generic.edit import DeleteView
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


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
    def get_context_data(self, **kwargs):
        """
        Inject the UserCreationForm into the template context 
        so the user can create a Django account.
        """
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        # Reconstruct both forms from POST data
        self.object = None
        form = self.get_form()
        user_form = UserCreationForm(request.POST)

        if form.is_valid() and user_form.is_valid():
            # Create user
            user = user_form.save()
            login(self.request, user)

            # Create profile
            form.instance.user = user
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def get_success_url(self):
        """
        Redirect to the newly created profile page after success.
        """
        return reverse('show_profile_page', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs
    

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    """
    Create a new status for a existing person.
    """
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Prevent posting to other users' profiles.
        """
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        if profile.user != request.user:
            return HttpResponseForbidden("You cannot post to this profile.")
        return super().dispatch(request, *args, **kwargs)

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
        sm = form.save(commit=False)  
        sm.profile = Profile.objects.get(pk=self.kwargs['pk']) 
        sm.save()

        files = self.request.FILES.getlist('files')
        for f in files:
            image = Image(profile=sm.profile, image_file=f)
            image.save()
            si = StatusImage(status_message=sm, image=image)
            si.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        """
        After successfully submitting the form, redirect to the profile's detail page.
        """
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    


class UpdateProfileView(LoginRequiredMixin,UpdateView):
    """
    View to update an existing user profile.
    """
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        """
        Redirect to the updated profile's detail view.
        """
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
    def dispatch(self, request, *args, **kwargs):
        """
        Prevent users from updating other users' profiles.
        """
        obj = self.get_object()
        if obj.user != request.user:
            return HttpResponseForbidden("You are not allowed to edit this profile.")
        return super().dispatch(request, *args, **kwargs)
    

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    """
    View to delete a specific status message.
    """
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def dispatch(self, request, *args, **kwargs):
        """
        Prevent users from deleting messages that aren't theirs.
        """
        obj = self.get_object()
        if obj.profile.user != request.user:
            return HttpResponseForbidden("You cannot delete this.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """
        Redirect to the profile page after deletion.
        """
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})


class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    """
    View to update the content of a specific status message.
    """
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/update_status_form.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Prevent users from editing messages that aren't theirs.
        """
        obj = self.get_object()
        if obj.profile.user != request.user:
            return HttpResponseForbidden("You cannot edit this message.")
        return super().dispatch(request, *args, **kwargs)
    

    def get_success_url(self):
        """
        Redirect to the profile detail page after successful update.
        """
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class AddFriendView(LoginRequiredMixin,View):
    """
    View to add the friend.
    """

    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs['pk'])
        if profile.user != request.user:
            return HttpResponseForbidden("You cannot add friends to someone else's profile.")
        other = get_object_or_404(Profile, pk=kwargs['other_pk'])
        profile.add_friend(other)
        return redirect('show_profile_page', pk=profile.pk)
    

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    """
    Display a list of suggested friends for the given profile.
    """
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.user != request.user:
            return HttpResponseForbidden("You cannot view someone else's friend suggestions.")
        return super().dispatch(request, *args, **kwargs)

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    """
    Display a news feed for the given profile.
    """
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'


    def dispatch(self, request, *args, **kwargs):
        """
        Prevent users from viewing other users' news feeds.
        """
        profile = self.get_object()
        if profile.user != request.user:
            return HttpResponseForbidden("You cannot view someone else's news feed.")
        return super().dispatch(request, *args, **kwargs)
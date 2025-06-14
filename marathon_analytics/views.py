from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import Voter
from .forms import VoterFilterForm

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()
        form = VoterFilterForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data['party']:
                queryset = queryset.filter(party=form.cleaned_data['party'])
            if form.cleaned_data['min_year']:
                queryset = queryset.filter(date_of_birth__year__gte=form.cleaned_data['min_year'])
            if form.cleaned_data['max_year']:
                queryset = queryset.filter(date_of_birth__year__lte=form.cleaned_data['max_year'])
            if form.cleaned_data['voter_score'] is not None:
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])
            for election in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if form.cleaned_data.get(election):
                    kwargs = {election: True}
                    queryset = queryset.filter(**kwargs)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)
        return context

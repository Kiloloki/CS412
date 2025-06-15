from django.views.generic import ListView, DetailView, TemplateView
from .models import Voter
from .forms import VoterFilterForm

import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['party_affiliation']:
                queryset = queryset.filter(party_affiliation=cd['party_affiliation'])
            if cd['min_birth_year']:
                queryset = queryset.filter(date_of_birth__year__gte=cd['min_birth_year'])
            if cd['max_birth_year']:
                queryset = queryset.filter(date_of_birth__year__lte=cd['max_birth_year'])
            if cd['voter_score']:
                queryset = queryset.filter(voter_score=cd['voter_score'])
            if cd['v20state']:
                queryset = queryset.filter(v20state=True)
            if cd['v21town']:
                queryset = queryset.filter(v21town=True)
            if cd['v21primary']:
                queryset = queryset.filter(v21primary=True)
            if cd['v22general']:
                queryset = queryset.filter(v22general=True)
            if cd['v23town']:
                queryset = queryset.filter(v23town=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'


class VoterGraphsView(TemplateView):
    template_name = 'voter_analytics/graphs.html'

    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['party_affiliation']:
                queryset = queryset.filter(party_affiliation=cd['party_affiliation'])
            if cd['min_birth_year']:
                queryset = queryset.filter(date_of_birth__year__gte=cd['min_birth_year'])
            if cd['max_birth_year']:
                queryset = queryset.filter(date_of_birth__year__lte=cd['max_birth_year'])
            if cd['voter_score']:
                queryset = queryset.filter(voter_score=cd['voter_score'])
            for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if cd.get(field):
                    kwargs = {field: True}
                    queryset = queryset.filter(**kwargs)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['form'] = VoterFilterForm(self.request.GET)

        # Histogram: Year of Birth
        df = queryset.values_list('date_of_birth', flat=True)
        years = [d.year for d in df if d]
        fig1 = px.histogram(x=years, nbins=80, title=f"Voter distribution by Year of Birth (n={len(years)})")
        fig1.update_traces(marker_color='royalblue')
        context['birth_hist'] = plot(fig1, output_type='div')

        # Pie: Party Affiliation
        party_labels = sorted(set(queryset.values_list('party_affiliation', flat=True)))
        party_freqs = [queryset.filter(party_affiliation=p).count() for p in party_labels]

        fig2 = px.pie(
            names=party_labels,
            values=party_freqs,
            title=f"Voter distribution by Party Affiliation (n={sum(party_freqs)})"
        )
        context['party_pie'] = plot(fig2, output_type='div')

        # Bar: Vote Count by Election
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        vote_counts = [queryset.filter(**{e: True}).count() for e in elections]
        fig3 = go.Figure([go.Bar(x=elections, y=vote_counts, marker_color='royalblue')])
        fig3.update_layout(title=f"Vote Count by Election (n={len(queryset)})")
        context['election_bar'] = plot(fig3, output_type='div')

        return context
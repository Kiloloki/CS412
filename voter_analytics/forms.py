# File: forms.py
# Author: bella918@bu.edu
# Date: 6/14/2025
# Description: Django form definitions for filtering Voter records in the
#              voter_analytics application. Includes fields for party affiliation,
#              birth year range, voter score, and election participation.
from django import forms
from .models import Voter
from datetime import datetime

YEAR_CHOICES = [(str(y), str(y)) for y in range(1920, datetime.now().year + 1)]

class VoterFilterForm(forms.Form):
    """All fields are optional and used for generating customized reports or visualizations."""
    party_affiliation = forms.ChoiceField(
        required=False,
        choices=[('', 'Any')] + [(p, p) for p in ['D ', 'R ', 'U ', 'G ', 'L ']],  
        label='Party Affiliation'
    )
    min_birth_year = forms.ChoiceField(required=False, choices=[('', 'Any')] + YEAR_CHOICES, label='Born After')
    max_birth_year = forms.ChoiceField(required=False, choices=[('', 'Any')] + YEAR_CHOICES, label='Born Before')
    voter_score = forms.ChoiceField(
        required=False,
        choices=[('', 'Any')] + [(str(i), str(i)) for i in range(6)],
        label='Voter Score'
    )
    v20state = forms.BooleanField(required=False, label='Voted 2020 State Election')
    v21town = forms.BooleanField(required=False, label='Voted 2021 Town Election')
    v21primary = forms.BooleanField(required=False, label='Voted 2021 Primary')
    v22general = forms.BooleanField(required=False, label='Voted 2022 General Election')
    v23town = forms.BooleanField(required=False, label='Voted 2023 Town Election')

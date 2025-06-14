from django import forms

class VoterFilterForm(forms.Form):
    PARTY_CHOICES = [('D', 'Democrat'), ('R', 'Republican'), ('U', 'Unenrolled')]
    YEAR_CHOICES = [(y, y) for y in range(1900, 2006)]
    SCORE_CHOICES = [(i, i) for i in range(6)]

    party = forms.ChoiceField(choices=[('', 'Any')] + PARTY_CHOICES, required=False)
    min_year = forms.ChoiceField(choices=[('', 'Any')] + YEAR_CHOICES, required=False)
    max_year = forms.ChoiceField(choices=[('', 'Any')] + YEAR_CHOICES, required=False)
    voter_score = forms.ChoiceField(choices=[('', 'Any')] + SCORE_CHOICES, required=False)
    
    v20state = forms.BooleanField(required=False)
    v21town = forms.BooleanField(required=False)
    v21primary = forms.BooleanField(required=False)
    v22general = forms.BooleanField(required=False)
    v23town = forms.BooleanField(required=False)

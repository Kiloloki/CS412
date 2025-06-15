from django import forms
from .models import Voter
from datetime import datetime

# 提取年份范围供筛选使用
YEAR_CHOICES = [(str(y), str(y)) for y in range(1920, datetime.now().year + 1)]

class VoterFilterForm(forms.Form):
    party_affiliation = forms.ChoiceField(
        required=False,
        choices=[('', 'Any')] + [(p, p) for p in ['D ', 'R ', 'U ', 'G ', 'L ']],  # 自行按数据调整
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

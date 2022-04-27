from django import forms
from django.db import models
from .models import Project
from datetime import datetime


class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(
        initial=datetime.today(),
        widget=forms.SelectDateWidget(attrs={'class': 'form-control'}, empty_label=''),
        label='Дата начала',
    )
    end_date = forms.DateField(
        initial=datetime.today(),
        widget=forms.SelectDateWidget(attrs={'class': 'form-control'}, empty_label=''),
        label='Дата начала',
    )

    class Meta:
        model = Project
        exclude = ['slug']
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'project_link': forms.TextInput(attrs={'class': 'form-control'}),
            # 'start_date': forms.SelectDateWidget(attrs={'class': 'form-control'},),
            # 'end_date': forms.SelectDateWidget(attrs={'class': 'form-control'}, empty_label=''),
            'originator': forms.Select(attrs={'class': 'form-control'}),
            'executor': forms.Select(attrs={'class': 'form-control'}),
            'coexecutor': forms.Select(attrs={'class': 'form-control'}),
            'auditor': forms.Select(attrs={'class': 'form-control'}),
            'is_finished': forms.CheckboxInput(attrs={'class': 'form-check-input mt-2'})
        }

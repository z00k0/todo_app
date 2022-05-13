from django import forms
from .models import Project, Task
from datetime import datetime
from django.forms import inlineformset_factory, modelformset_factory


class ProjectForm(forms.ModelForm):
    project_start_date = forms.DateField(
        initial=datetime.today(),
        widget=forms.SelectDateWidget(attrs={'class': 'form-control'}, empty_label=''),
        label='Дата начала',
    )
    # project_end_date = forms.DateField(
    #     initial=datetime.today(),
    #     widget=forms.SelectDateWidget(attrs={'class': 'form-control'}, empty_label=''),
    #     label='Дата окончания',
    # )

    class Meta:
        model = Project
        exclude = ['slug', 'project_end_date', 'calendar_chart']

        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'project_link': forms.TextInput(attrs={'class': 'form-control'}),
            # 'start_date': forms.SelectDateWidget(attrs={'class': 'form-control'},),
            # 'end_date': forms.SelectDateWidget(attrs={'class': 'form-control'}, empty_label=''),
            'originator': forms.Select(attrs={'class': 'form-control'}),
            'executor': forms.Select(attrs={'class': 'form-control'}),
            'is_finished': forms.CheckboxInput(attrs={'class': 'form-check-input mt-2'})
        }


class TaskForm(forms.ModelForm):
    # task_start_date = forms.DateField(
    #     initial=datetime.today(),
    #     widget=forms.SelectDateWidget(attrs={'class': 'form-control'}, empty_label=''),
    #     label='Дата начала',
    # )
    # task_end_date = forms.DateField(
    #     initial=datetime.today(),
    #     widget=forms.SelectDateWidget(attrs={'class': 'form-control'}, empty_label=''),
    #     label='Дата окончания',
    # )

    class Meta:
        model = Task
        exclude = ['slug']
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'start_date': forms.SelectDateWidget(attrs={'class': 'form-control'},),
            # 'end_date': forms.SelectDateWidget(attrs={'class': 'form-control'}, empty_label=''),
            'originator': forms.Select(attrs={'class': 'form-control'}),
            'executor': forms.Select(attrs={'class': 'form-control'}),
            'is_finished': forms.CheckboxInput(attrs={'class': 'form-check-input mt-2'})
        }


TasksInlineFormSet = inlineformset_factory(
    Project,
    Task,
    form=TaskForm,
    # fields='__all__',
    exclude=('project', 'task_end_date', 'originator', 'executor'),
    extra=0,
    can_order=True,
)

TasksModelFormSet = modelformset_factory(
    Task,
    form=TaskForm,
    # fields='__all__',
    exclude=('project', 'task_end_date', 'originator', 'executor'),
    can_order=True,
    can_delete=True,
    extra=6
)
from django import forms
from django.db import models
from .models import Project, Task
from datetime import datetime
from django.forms import formset_factory, modelformset_factory, inlineformset_factory


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
        exclude = ['slug', 'project_end_date']
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
            # 'coexecutor': forms.Select(attrs={'class': 'form-control'}),
            # 'auditor': forms.Select(attrs={'class': 'form-control'}),
            'is_finished': forms.CheckboxInput(attrs={'class': 'form-check-input mt-2'})
        }


data = {
    'tasks-TOTAL_FORMS': '6',
    'tasks-INITIAL_FORMS': '6',
    'tasks-0-number': 1,
    'tasks-0-name': 'Встреча-знакомство, анкетирование',
    'tasks-0-duration': 5,
    'tasks-1-number': 2,
    'tasks-1-name': 'Обмерный план, планировочные решения',
    'tasks-1-duration': 4,
    'tasks-2-number': 3,
    'tasks-2-name': 'Утверждение планировки',
    'tasks-2-duration': 1,
    'tasks-3-number': 4,
    'tasks-3-name': 'Схемы размещения освещения, розеток и выключателей (1 вариант+2 корректировки)',
    'tasks-3-duration': 3,
    'tasks-4-number': 5,
    'tasks-4-name': 'Утверждение схем размещения освещения, розеток и выключателей',
    'tasks-4-duration': 1,
    'tasks-5-number': 6,
    'tasks-5-name': 'Уточнение листа опций видов работ',
    'tasks-5-duration': 1,

}

# AddTaskFormSet = modelformset_factory(
#     Task,
#     form=TaskForm,
#     # fields='__all__',
#     exclude=['slug', 'project', 'originator'],
#     can_delete=True,
#     max_num=20,
#     absolute_max=30,
# )
TasksInlineFormSet = inlineformset_factory(
    Project,
    Task,
    form=TaskForm,
    fields='__all__',
    extra=0,
    can_order=True,
    
)
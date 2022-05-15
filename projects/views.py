from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View, FormView

from .models import Project, Task
from .forms import ProjectForm, TasksInlineFormSet, TasksModelFormSet

import datetime

initial = [
    {'number': 1,
     'name': 'Встреча-знакомство, анкетирование',
     'duration': 5,
     'field_color': '#ff0000'},
    {'number': 2,
     'name': 'Обмерный план, планировочные решения',
     'duration': 4,
     'field_color': '#fce5cd'},
    {'number': 3,
     'name': 'Утверждение планировки',
     'duration': 1,
     'field_color': '#ffff00'},
    {'number': 4,
     'name': 'Схемы размещения освещения, розеток и выключателей (1 вариант+2 корректировки)',
     'duration': 3,
     'field_color': '#d9ffd3'},
    {'number': 5,
     'name': 'Утверждение схем размещения освещения, розеток и выключателей',
     'duration': 1,
     'field_color': '#93c47d'},
    {'number': 6,
     'name': 'Уточнение листа опций видов работ',
     'duration': 1,
     'field_color': '#c9daf8'}
]


class ProjectList(ListView):
    model = Project
    template_name = 'projects/projects.html'
    context_object_name = 'projects'
    allow_empty = True

    chart_range = []
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=14)
    while start < end:
        chart_range.append(start.strftime('%d.%m'))
        start += datetime.timedelta(days=1)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Проекты'
        context['chart_range'] = self.chart_range

        return context

    def get_queryset(self):
        return Project.objects.filter(is_finished=False)


class ProjectDetail(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    slug_url_kwarg = 'project_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Проект - ' + context['project'].name

        return context


class ProjectEdit(View):
    # form_class = ProjectForm
    template_name = 'projects/project_edit.html'
    context_object_name = 'project_edit'

    def get(self, request, project_slug, *args, **kwargs):
        project = get_object_or_404(Project, slug=project_slug)
        form = ProjectForm(instance=project)
        task_formset = TasksInlineFormSet(prefix='tasks', instance=project)

        return render(
            request,
            template_name=self.template_name,
            context={'project': project, 'form': form, 'task_formset': task_formset}
        )

    def post(self, request, project_slug, *args, **kwargs):
        project = get_object_or_404(Project, slug=project_slug)
        bound_form = ProjectForm(request.POST, instance=project)
        bound_formset = TasksInlineFormSet(request.POST, prefix='tasks', instance=project)
        if bound_form.is_valid() and bound_formset.is_valid():
            print('all valid')
            project_duration = 0
            instances = bound_formset.save(commit=False)
            start_date = project.project_start_date

            for instance in instances:
                instance.project = project
                instance.save()
            calendar = {}
            for task in project.tasks.all():
                project_duration += task.duration
                task.task_start_date = start_date
                task.task_end_date = start_date + datetime.timedelta(days=(task.duration - 1))
                start_date = task.task_end_date + datetime.timedelta(days=1)
                task.originator = project.originator
                task.executor = project.executor

                start = task.task_start_date
                end = task.task_end_date
                while start <= end:
                    calendar[start.strftime('%d.%m')] = [task.field_color, task.name]
                    start += datetime.timedelta(days=1)
            project.project_end_date = bound_form.cleaned_data['project_start_date'] + datetime.timedelta(
                days=project_duration)
            project.calendar_chart = calendar
            bound_form.save()
            bound_formset.save()
            return HttpResponseRedirect(reverse('projects:projects'))
        else:
            print(f'{bound_form.errors=}\n{bound_formset.errors=}')

            task_formset = TasksInlineFormSet(prefix='tasks', instance=project)
            form = ProjectForm(instance=project)
            return render(
                request,
                template_name=self.template_name,
                context={'project': project, 'form': form, 'task_formset': task_formset}
            )


class TaskSetCreate(View):
    # form_class = ProjectForm
    template_name = 'projects/taskset_create.html'
    context_object_name = 'project_create'

    # slug_url_kwarg = 'project_slug'

    def get(self, request, *args, **kwargs):
        form = ProjectForm()
        task_formset = TasksModelFormSet(prefix='tasks', initial=initial, queryset=Project.objects.none())
        return render(
            request,
            template_name=self.template_name,
            context={'form': form, 'task_formset': task_formset}  # 'project': project,
        )

    def post(self, request, *args, **kwargs):
        # project = get_object_or_404(Project, slug=project_slug)
        bound_form = ProjectForm(request.POST)
        bound_formset = TasksModelFormSet(data=request.POST, prefix='tasks')

        if bound_form.is_valid() and bound_formset.is_valid():
            print('all valid')
            project_duration = 0
            project = bound_form.save(commit=False)
            instances = bound_formset.save(commit=False)
            start_date = project.project_start_date
            for instance in instances:
                instance.project = project
                project_duration += instance.duration
                instance.task_start_date = start_date
                instance.task_end_date = start_date + datetime.timedelta(days=(instance.duration - 1))
                start_date = instance.task_end_date + datetime.timedelta(days=1)
                instance.originator = project.originator
                instance.executor = project.executor

            project.project_end_date = project.project_start_date + datetime.timedelta(
                days=project_duration)

            bound_form.save()
            bound_formset.save()
            return HttpResponseRedirect(reverse('projects:projects'))
        else:
            print(f'{bound_form.errors=}\n{bound_formset.errors=}\n{bound_formset.non_form_errors()=}')

            bound_formset = TasksModelFormSet(prefix='tasks', queryset=Project.objects.none(), initial=initial)
            form = ProjectForm()

            return render(
                request,
                template_name=self.template_name,
                context={'form': form, 'task_formset': bound_formset}  # 'project': project,
            )

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import Project, Task
from .forms import ProjectForm

from users.models import AppUser


class ProjectList(ListView):
    model = Project
    template_name = 'projects/projects.html'
    context_object_name = 'projects'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Проекты'

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


class AddProject(CreateView):
    form_class = ProjectForm
    template_name = 'projects/create_project.html'
    context_object_name = 'add_project'
    # print(dir(form_class.slug))
    success_url = reverse_lazy('projects:projects')#, kwargs={'project_slug': slug})



from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View, FormView
from django.forms import formset_factory, modelformset_factory, inlineformset_factory

from .models import Project, Task
from .forms import ProjectForm, TaskForm, TasksInlineFormSet  # AddTaskFormSet,

from users.models import AppUser
import datetime


class ProjectList(ListView):
    model = Project
    template_name = 'projects/projects.html'
    context_object_name = 'projects'
    allow_empty = True

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
    template_name = 'projects/project_create.html'
    context_object_name = 'add_project'

    # print(dir(form_class.slug))
    # success_url = reverse_lazy('projects:projects')#, kwargs={'project_slug': slug})


# class AddTaskSet(CreateView):

#     form_class = ProjectForm
#     task_formset = AddTaskFormSet(data=data, prefix='tasks', queryset=Task.objects.none())
#
#     template_name = 'projects/taskset_create.html'
#     context_object_name = 'add_task_set'
#
#     def get_context_data(self, **kwargs):
#         context = super(AddTaskSet, self).get_context_data(**kwargs)
#         if self.request.POST:
#             context['task_formset'] = AddTaskFormSet(self.request.POST, prefix='tasks', queryset=Task.objects.none())
#         else:
#             context['task_formset'] = self.task_formset  # AddTaskFormSet(data=data, prefix='tasks')
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         task_formset = context['task_formset']
#         # task_formset.auto_id = True
#         print(f'{self.task_formset=}')
#         print(f'1.{self.task_formset[0]=}')
#         print(f'{self.task_formset[0].is_valid()=}')
#         if self.task_formset[0].is_valid():
#             print(f"{self.task_formset[0].cleaned_data=}")
#         if form.is_valid():
#             print(f'{form.cleaned_data=}')
#             for form in self.task_formset:
#                 print(f"{dir(form.fields['id'].choices)=}")
#                 for choice in form.fields['id'].choices:
#                     print(f"{choice=}")
#                 print(f"{form.fields['id'].choices.choice=}")
#             if self.task_formset.is_valid():
#                 print(f'{task_formset.cleaned_data=}')
#                 print('formset valid')
#                 project = form.save()
#                 # for obj in task_formset.deleted_objects:
#                 #     obj.delete()
#                 print(f'2.{project=}')
#                 instances = task_formset.save(commit=False)
#                 print(f"3.{instances=}")
#                 for instance in instances:
#                     instance.project = project
#                     instance.save()
#                 return project.get_absolute_url()
#
#         print(f'{self.task_formset.non_form_errors()=}')
#         print(f'{self.task_formset.errors=}')
#         return self.render_to_response(context)


class AddTasksForProject(View):
    # form_class = ProjectForm
    template_name = 'projects/taskset_create.html'
    context_object_name = 'project_edit'

    # slug_url_kwarg = 'project_slug'

    def get(self, request, project_slug, *args, **kwargs):
        print(f'{project_slug=}')
        project = get_object_or_404(Project, slug=project_slug)
        form = ProjectForm(instance=project)
        task_formset = TasksInlineFormSet(prefix='tasks', instance=project)
        print(f"{request=}")
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
            for instance in instances:
                instance.project = project
                instance.save()
            for task in project.tasks.all():
                project_duration += task.duration
            project.project_end_date = bound_form.cleaned_data['project_start_date'] + datetime.timedelta(days=project_duration)
            bound_form.save()
        else:
            print(f'{bound_form.errors=}\n{bound_formset.errors=}')

        task_formset = TasksInlineFormSet(prefix='tasks', instance=project)
        form = ProjectForm(instance=project)
        print(f'{bound_formset.non_form_errors()=}')
        print(f'{bound_formset.errors=}')
        return render(
            request,
            template_name=self.template_name,
            context={'project': project, 'form': form, 'task_formset': task_formset}
        )

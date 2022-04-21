from django.shortcuts import render
from .models import Project, Task

from users.models import AppUser


def projects(request):
    project_list = Project.objects.all()

    return render(request, 'projects.html', {'project_list': project_list})

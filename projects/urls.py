from django.urls import path

from .views import ProjectList, ProjectDetail, AddProject, AddTasksForProject

app_name = 'projects'

urlpatterns = [
    path('projects/', ProjectList.as_view(), name='projects'),
    path('projects/create/', AddProject.as_view(), name='add_project'),
    path('projects/<slug:project_slug>/', ProjectDetail.as_view(), name='project'),
    path('projects/<slug:project_slug>/edit/', AddTasksForProject.as_view(), name='project_edit'),
    # path('tasks/create', AddTaskSet.as_view(), name='add_task_set'),
]

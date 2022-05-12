from django.urls import path

from .views import ProjectList, ProjectDetail, ProjectEdit, TaskSetCreate  # , ProjectCreate

app_name = 'projects'

urlpatterns = [
    path('projects/', ProjectList.as_view(), name='projects'),
    path('projects/create/', TaskSetCreate.as_view(), name='project_create'),
    path('projects/<slug:project_slug>/', ProjectDetail.as_view(), name='project'),
    path('projects/<slug:project_slug>/edit/', ProjectEdit.as_view(), name='project_edit'),
    # path('projects/<slug:project_slug>/create/', TaskSetCreate.as_view(), name='taskset_create'),
    # path('tasks/create', AddTaskSet.as_view(), name='add_task_set'),
]

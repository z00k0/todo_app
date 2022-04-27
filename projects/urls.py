from django.urls import path

from projects import views
from .views import ProjectList, ProjectDetail, AddProject

app_name = 'projects'

urlpatterns = [
    path('projects/', ProjectList.as_view(), name='projects'),
    path('projects/create/', AddProject.as_view(), name='add_project'),
    path('projects/<slug:project_slug>/', ProjectDetail.as_view(), name='project'),

]
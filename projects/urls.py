from django.urls import path
from .views import (
    project_list,
    create_project,
    create_plot,
    project_dashboard,
    edit_project
)

urlpatterns = [
    path(
        'projects/',
        project_list,
        name='project_list'
    ),

    path(
        'projects/create/',
        create_project,
        name='create_project'
    ),

    path(
        'projects/plots/create/',
        create_plot,
        name='create_plot'
    ),

    path(
        'projects/<int:project_id>/',
        project_dashboard,
        name='project_dashboard'
    ),

    path(
        'projects/edit/<int:project_id>/',
        edit_project,
        name='edit_project'
    ),
]
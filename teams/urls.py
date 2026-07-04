from django.urls import path
from .views import (
    team_list,
    create_team,
    team_dashboard,
    edit_team
)

urlpatterns = [
    path(
        'teams/',
        team_list,
        name='team_list'
    ),

    path(
        'teams/create/',
        create_team,
        name='create_team'
    ),

    path(
        'teams/<int:team_id>/',
        team_dashboard,
        name='team_dashboard'
    ),

    path(
        'teams/edit/<int:team_id>/',
        edit_team,
        name='edit_team'
    ),
]
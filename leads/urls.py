from django.urls import path
from .views import (
    lead_list,
    create_lead,
    lead_profile,
    edit_lead,
    convert_lead,
    get_lead_details,
)

urlpatterns = [
    path(
        'leads/',
        lead_list,
        name='lead_list'
    ),

    path(
        'leads/create/',
        create_lead,
        name='create_lead'
    ),

    path(
        'leads/<int:lead_id>/',
        lead_profile,
        name='lead_profile'
    ),

    path(
        'leads/edit/<int:lead_id>/',
        edit_lead,
        name='edit_lead'
    ),

    path(
    'leads/convert/<int:lead_id>/',
    convert_lead,
    name='convert_lead'
    ),

    path(
    "ajax/get-lead-details/",
    get_lead_details,
    name="get_lead_details",
    ),
]
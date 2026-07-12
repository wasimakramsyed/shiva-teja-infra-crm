from django.urls import path
from .views import (
    registration_dashboard,
    registration_list,
    create_registration,
    registration_profile,
)

urlpatterns = [
    path(
        'registrations/',
        registration_dashboard,
        name='registration_dashboard'
    ),

    path(
        'registrations/list/',
        registration_list,
        name='registration_list'
    ),

    path(
        'registrations/create/',
        create_registration,
        name='create_registration'
    ),
    path(
    "registrations/<int:registration_id>/",
    registration_profile,
    name="registration_profile",
),
]
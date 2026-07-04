from django.urls import path
from .views import (
    registration_list,
    create_registration
)

urlpatterns = [
    path(
        'registrations/',
        registration_list,
        name='registration_list'
    ),

    path(
        'registrations/create/',
        create_registration,
        name='create_registration'
    ),
]
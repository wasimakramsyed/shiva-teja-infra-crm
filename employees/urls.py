from django.urls import path
from .views import (
    employee_list,
    create_employee,
    employee_profile,
    edit_employee
)

urlpatterns = [
    path(
        'employees/',
        employee_list,
        name='employee_list'
    ),

    path(
        'employees/create/',
        create_employee,
        name='create_employee'
    ),

    path(
        'employees/<int:employee_id>/',
        employee_profile,
        name='employee_profile'
    ),

    path(
        'employees/edit/<int:employee_id>/',
        edit_employee,
        name='edit_employee'
    ),
]
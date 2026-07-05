from django.urls import path
from .views import (
    customer_list,
    create_customer,
    customer_profile,
    edit_customer
)

urlpatterns = [
    path(
        'customers/',
        customer_list,
        name='customer_list'
    ),

    path(
        'customers/create/',
        create_customer,
        name='create_customer'
    ),

    path(
        'customers/<int:customer_id>/',
        customer_profile,
        name='customer_profile'
    ),

    path(
        'customers/edit/<int:customer_id>/',
        edit_customer,
        name='edit_customer'
    ),
]
from django.urls import path
from .views import (
    payment_list,
    create_payment
)

urlpatterns = [
    path(
        'payments/',
        payment_list,
        name='payment_list'
    ),

    path(
        'payments/create/',
        create_payment,
        name='create_payment'
    ),
]
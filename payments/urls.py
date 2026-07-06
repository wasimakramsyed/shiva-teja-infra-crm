from django.urls import path
from .views import (
    payment_list,
    create_payment,
    payment_profile,
    edit_payment,
    generate_payment_receipt
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

    path(
        'payments/<int:payment_id>/',
        payment_profile,
        name='payment_profile'
    ),

    path(
        'payments/edit/<int:payment_id>/',
        edit_payment,
        name='edit_payment'
    ),
    path(
    'payments/receipt/<int:payment_id>/',
    generate_payment_receipt,
    name='generate_payment_receipt'
),
]
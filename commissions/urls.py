from django.urls import path
from .views import (
    commission_list,
    create_commission,
    commission_profile,
    edit_commission
)

urlpatterns = [
    path(
        'commissions/',
        commission_list,
        name='commission_list'
    ),

    path(
        'commissions/create/',
        create_commission,
        name='create_commission'
    ),

    path(
        'commissions/<int:commission_id>/',
        commission_profile,
        name='commission_profile'
    ),

    path(
        'commissions/edit/<int:commission_id>/',
        edit_commission,
        name='edit_commission'
    ),
]
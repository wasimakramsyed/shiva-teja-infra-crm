from django.urls import path

from .views import (
    commission_list,
    commission_profile,
    approve_commission,
    mark_commission_paid,
)

urlpatterns = [

    path(
        "commissions/",
        commission_list,
        name="commission_list"
    ),

    path(
        "commissions/<int:commission_id>/",
        commission_profile,
        name="commission_profile"
    ),

    path(
        "commissions/<int:commission_id>/approve/",
        approve_commission,
        name="approve_commission"
    ),

    path(
        "commissions/<int:commission_id>/mark-paid/",
        mark_commission_paid,
        name="mark_commission_paid"
    ),

]
from django.urls import path

from commissions.views.dashboard import commission_dashboard

from .views import (
    commission_list,
    commission_profile,
    approve_commission,
    mark_commission_paid,
    commission_request_list,
    generate_commission,
    commission_allocation,
    commission_request_profile,
)

urlpatterns = [
      path(
    "commissions/",
    commission_dashboard,
    name="commission_dashboard",
    ),
    
    path(
    "commissions/generated/",
    commission_list,
    name="commission_list",
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
    path(
        "commission-requests/",
        commission_request_list,
        name="commission_request_list",
    ),
    path(
        "commission-requests/<int:pk>/generate/",
        generate_commission,
        name="generate_commission",
    ),
    path(

    "allocation/<int:pk>/",

    commission_allocation,

    name="commission_allocation",

    ),
    path(
    "commission-request/<int:pk>/",
    commission_request_profile,
    name="commission_request_profile",
),

]
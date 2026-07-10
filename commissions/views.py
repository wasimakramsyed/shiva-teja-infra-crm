from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.db.models import Q
from django.contrib import messages

from .models import Commission
from .services.commission_service import CommissionService

from accounts.decorators import role_required


# ==========================================================
# Commission List
# ==========================================================

@role_required(["admin", "accounts", "manager"])
def commission_list(request):

    query = request.GET.get("q", "")
    status_filter = request.GET.get("status")

    commissions = Commission.objects.select_related(
        "booking",
        "customer",
        "employee",
        "team",
        "policy",
    )

    if query:

        commissions = commissions.filter(

            Q(commission_id__icontains=query) |

            Q(booking__booking_id__icontains=query) |

            Q(customer__customer_name__icontains=query)

        )

    if status_filter:

        commissions = commissions.filter(
            status=status_filter
        )

    return render(
        request,
        "commissions/commission_list.html",
        {
            "commissions": commissions,
            "query": query,
            "status_filter": status_filter,
        },
    )


# ==========================================================
# Commission Profile
# ==========================================================

@role_required(["admin", "accounts", "manager"])
def commission_profile(request, commission_id):

    commission = get_object_or_404(
        Commission,
        id=commission_id,
    )

    return render(
        request,
        "commissions/commission_profile.html",
        {
            "commission": commission,
        },
    )


# ==========================================================
# Approve Commission
# ==========================================================

@role_required(["admin", "accounts"])
def approve_commission(request, commission_id):

    commission = get_object_or_404(
        Commission,
        id=commission_id,
    )

    if commission.status != "generated":

        messages.warning(
            request,
            "Only generated commissions can be approved."
        )

        return redirect(
            "commission_profile",
            commission_id=commission.id
        )

    CommissionService.approve_commission(
        commission,
        request.user
    )

    messages.success(
        request,
        "Commission approved successfully."
    )

    return redirect(
        "commission_profile",
        commission_id=commission.id
    )


# ==========================================================
# Mark Commission Paid
# ==========================================================

@role_required(["admin", "accounts"])
def mark_commission_paid(request, commission_id):

    commission = get_object_or_404(
        Commission,
        id=commission_id,
    )

    if commission.status != "approved":

        messages.warning(
            request,
            "Only approved commissions can be marked as paid."
        )

        return redirect(
            "commission_profile",
            commission_id=commission.id
        )

    CommissionService.mark_paid(
        commission,
        request.user
    )

    messages.success(
        request,
        "Commission marked as paid."
    )

    return redirect(
        "commission_profile",
        commission_id=commission.id
    )
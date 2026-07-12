from django.shortcuts import (
    redirect,
    get_object_or_404,
)

from django.contrib import messages

from accounts.decorators import role_required

from commissions.models import CommissionRecord
from commissions.services.commission_service import CommissionService


@role_required(["admin", "accounts"])
def approve_commission(request, commission_id):

    commission = get_object_or_404(
        CommissionRecord,
        id=commission_id,
    )

    if commission.status != "generated":

        messages.warning(
            request,
            "Only generated commissions can be approved."
        )

        return redirect(
            "commission_profile",
            commission_id=commission.id,
        )

    CommissionService.approve_commission(
        commission,
        request.user,
    )

    messages.success(
        request,
        "Commission approved successfully."
    )

    return redirect(
        "commission_profile",
        commission_id=commission.id,
    )


@role_required(["admin", "accounts"])
def mark_commission_paid(request, commission_id):

    commission = get_object_or_404(
        CommissionRecord,
        id=commission_id,
    )

    if commission.status != "approved":

        messages.warning(
            request,
            "Only approved commissions can be marked as paid."
        )

        return redirect(
            "commission_profile",
            commission_id=commission.id,
        )

    CommissionService.mark_paid(
        commission,
        request.user,
    )

    messages.success(
        request,
        "Commission marked as paid."
    )

    return redirect(
        "commission_profile",
        commission_id=commission.id,
    )
from django.shortcuts import render
from django.db.models import Sum

from accounts.decorators import role_required
from commissions.models import (
    CommissionRecord,
    CommissionRequest,
)


@role_required(["admin", "accounts", "manager"])
def commission_dashboard(request):

    commissions = CommissionRecord.objects.all()

    requests = CommissionRequest.objects.filter(
        status="ready"
    )

    context = {

        "generated": commissions.filter(
            status="generated"
        ).count(),

        "approved": commissions.filter(
            status="approved"
        ).count(),

        "paid": commissions.filter(
            status="paid"
        ).count(),

        "pending_requests": requests.count(),

        "total_commission":
        commissions.aggregate(
            total=Sum("net_commission")
        )["total"] or 0,

        "pending_amount":
        commissions.exclude(
            status="paid"
        ).aggregate(
            total=Sum("net_commission")
        )["total"] or 0,

        "recent":
        commissions.order_by(
            "-created_at"
        )[:10],

    }

    return render(

        request,

        "commissions/dashboard.html",

        context,

    )
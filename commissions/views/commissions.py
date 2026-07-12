from django.shortcuts import (
    render,
    get_object_or_404,
)

from django.db.models import Sum

from accounts.decorators import role_required

from commissions.models import (
    CommissionRecord,
    CommissionAllocation,
    CommissionTimeline,
)


from django.db.models import Q
from projects.models import Project


@role_required(["admin", "accounts", "manager"])
def commission_list(request):

    query = request.GET.get("q", "")
    status = request.GET.get("status", "")
    project = request.GET.get("project", "")

    commissions = (
        CommissionRecord.objects
        .select_related(
            "customer",
            "project",
            "booking",
        )
        .order_by("-created_at")
    )

    if query:

        commissions = commissions.filter(

            Q(request__request_id__icontains=query) |

            Q(customer__customer_name__icontains=query) |

            Q(booking__booking_id__icontains=query)

        )

    if status:

        commissions = commissions.filter(
            status=status
        )

    if project:

        commissions = commissions.filter(
            project_id=project
        )

    context = {

        "commissions": commissions,

        "projects": Project.objects.all(),

        "query": query,

        "status": status,

        "project": project,

        "generated_count": commissions.filter(
            status="generated"
        ).count(),

        "approved_count": commissions.filter(
            status="approved"
        ).count(),

        "paid_count": commissions.filter(
            status="paid"
        ).count(),

        "total_commission":
        commissions.aggregate(
            total=Sum("net_commission")
        )["total"] or 0,

    }

    return render(

        request,

        "commissions/commission_list.html",

        context,

    )

@role_required(["admin", "accounts", "manager"])
def commission_profile(request, commission_id):

    commission = get_object_or_404(
        CommissionRecord,
        pk=commission_id,
    )

    allocations = (
        CommissionAllocation.objects
        .select_related("employee")
        .filter(
            commission=commission
        )
    )

    timeline = (
        CommissionTimeline.objects
        .filter(
            commission=commission
        )
        .order_by("created_at")
    )

    context = {

        "commission": commission,

        "allocations": allocations,

        "timeline": timeline,

    }

    return render(

        request,

        "commissions/commission_profile.html",

        context,

    )
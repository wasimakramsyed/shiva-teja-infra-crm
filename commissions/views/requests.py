from django.shortcuts import render
from django.db.models import Q

from accounts.decorators import role_required
from projects.models import Project

from commissions.models import CommissionRequest


@role_required(["admin", "accounts", "manager"])
def commission_request_list(request):

    query = request.GET.get("q", "")
    project = request.GET.get("project")
    status = request.GET.get("status")

    requests = (
        CommissionRequest.objects
        .select_related(
            "customer",
            "project",
            "plot",
            "employee",
            "team",
        )
        .filter(status="ready")
    )

    if query:

        requests = requests.filter(

            Q(request_id__icontains=query) |

            Q(customer__customer_name__icontains=query) |

            Q(booking__booking_id__icontains=query) |

            Q(plot__plot_number__icontains=query) |

            Q(project__project_name__icontains=query)

        )

    if project:

        requests = requests.filter(
            project_id=project
        )

    if status:

        requests = requests.filter(
            status=status
        )

    return render(

        request,

        "commissions/commission_request_list.html",

        {

            "requests": requests,

            "projects": Project.objects.all(),

            "query": query,

            "status": status,

        },

    )
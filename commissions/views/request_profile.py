from django.shortcuts import render

from accounts.decorators import role_required

from commissions.services.request_service import (
    CommissionRequestService,
)


@role_required(["admin", "accounts", "manager"])
def commission_request_profile(request, pk):

    request_obj = CommissionRequestService.get_request(pk)

    context = {

        "request_obj": request_obj,

    }

    return render(

        request,

        "commissions/commission_request_profile.html",

        context,

    )
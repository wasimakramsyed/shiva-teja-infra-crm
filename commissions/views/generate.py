from decimal import Decimal

from django.contrib import messages
from django.shortcuts import render, redirect

from accounts.decorators import role_required

from commissions.forms import CommissionGenerationForm
from commissions.services.generator_service import (
    CommissionGeneratorService,
)
from commissions.services.request_service import (
    CommissionRequestService,
)


@role_required(["admin", "accounts"])
def generate_commission(request, pk):

    commission_request = CommissionRequestService.get_request(pk)

    members = []

    if commission_request.team:
        members = commission_request.team.members.all()

    if request.method == "POST":

        form = CommissionGenerationForm(request.POST)

        if form.is_valid():

            if not members:
                messages.error(
                    request,
                    "No sales team assigned to this booking."
                )
                return render(
                    request,
                    "commissions/generate_commission.html",
                    {
                        "request_obj": commission_request,
                        "form": form,
                        "members": members,
                    },
                )

            allocations = []

            for member in members:

                percentage = request.POST.get(
                    f"percent_{member.id}",
                    "0"
                )

                allocations.append({
                    "employee": member,
                    "percentage": Decimal(str(percentage)),
                })

            try:

                CommissionGeneratorService.generate(

                    request=commission_request,

                    commission_percentage=form.cleaned_data[
                        "commission_percentage"
                    ],

                    tds_percentage=form.cleaned_data[
                        "tds_percentage"
                    ],

                    other_deduction=form.cleaned_data[
                        "other_deduction"
                    ],

                    remarks=form.cleaned_data[
                        "remarks"
                    ],

                    allocations=allocations,

                    generated_by=request.user,

                )

                messages.success(
                    request,
                    "Commission generated successfully."
                )

                return redirect(
                    "commission_request_list"
                )

            except Exception as e:

                messages.error(
                    request,
                    str(e)
                )

    else:

        form = CommissionGenerationForm()

    return render(

        request,

        "commissions/generate_commission.html",

        {

            "request_obj": commission_request,

            "form": form,

            "members": members,

        },

    )


@role_required(["admin", "accounts"])
def commission_allocation(request, pk):

    commission_request = (
        CommissionRequestService.get_request(pk)
    )

    members = []

    if commission_request.team:

        members = commission_request.team.members.all()

    return render(

        request,

        "commissions/allocation.html",

        {

            "request_obj": commission_request,

            "members": members,

        },

    )
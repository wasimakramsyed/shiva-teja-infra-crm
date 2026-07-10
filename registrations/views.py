from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError

from .models import Registration
from .forms import RegistrationForm

from accounts.decorators import role_required
from notifications.models import Notification

from registrations.services.registration_service import (
    RegistrationService
)


# ==========================================================
# Registration List
# ==========================================================
@role_required(["admin", "manager"])
def registration_list(request):

    registrations = Registration.objects.select_related(
        "booking"
    )

    return render(
        request,
        "registrations/registration_list.html",
        {
            "registrations": registrations
        }
    )


# ==========================================================
# Create Registration
# ==========================================================
@role_required(["admin", "manager"])
def create_registration(request):

    form = RegistrationForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == "POST":

        if form.is_valid():

            try:

                registration = (
                    RegistrationService.register_property(
                        form=form,
                        user=request.user
                    )
                )

                Notification.objects.create(
                    message=(
                        f"Registration "
                        f"{registration.registration_id} "
                        f"completed successfully."
                    )
                )

                messages.success(
                    request,
                    "Registration completed successfully."
                )

                return redirect(
                    "registration_list"
                )

            except ValidationError as e:

                messages.error(
                    request,
                    str(e)
                )

        else:

            messages.error(
                request,
                "Please correct the highlighted errors."
            )

    return render(
        request,
        "registrations/create_registration.html",
        {
            "form": form
        }
    )
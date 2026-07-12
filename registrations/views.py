from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import get_object_or_404
from accounts.decorators import role_required

from customers.models import Customer

from bookings.models import Booking

from notifications.models import Notification

from registrations.forms import RegistrationForm

from registrations.models import Registration

from registrations.services.registration_service import (
    RegistrationService,
)

# ==========================================================
# Registration List
# ==========================================================
@role_required(["admin", "manager"])
def registration_list(request):

    registrations = (

        Registration.objects

        .select_related(

            "booking",

            "customer",

            "booking__project",

        )

        .order_by(

            "-registration_date"

        )

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

                registration = form.save(commit=False)

                registration.created_by = request.user

                # -----------------------------------------
                # Link Customer Automatically
                # -----------------------------------------

                customer = Customer.objects.filter(
                    mobile_number=registration.booking.mobile_number
                ).first()

                if not customer:
                    raise ValidationError(
                        "Customer not found for this booking."
                    )

                registration.customer = customer

                registration.save()

                RegistrationService.register(

                    registration=registration,

                    created_by=request.user,

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


@role_required(["admin", "accounts", "manager"])
def registration_dashboard(request):

    today = timezone.now().date()

    context = {

        "total_registrations":
            Registration.objects.count(),

        "today_registrations":
            Registration.objects.filter(
                registration_date=today
            ).count(),

        "upcoming_registrations":
            Registration.objects.filter(
                registration_date__gt=today
            ).count(),

        "completed_registrations":
            Registration.objects.count(),

        "pending_registrations":
            Booking.objects.filter(
                status="fully_paid"
            ).exclude(
                registration__isnull=False
            ).count(),

        "registration_value":
            Registration.objects.aggregate(
                total=Sum("market_value")
            )["total"] or 0,

        "today_list":
            Registration.objects.filter(
                registration_date=today
            ).select_related(
                "booking",
                "customer"
            ).order_by("registration_date")[:10],

    }

    return render(

        request,

        "registrations/dashboard.html",

        context,

    )

@role_required(["admin", "accounts", "manager"])
def registration_profile(request, registration_id):

    registration = get_object_or_404(

        Registration.objects.select_related(

            "customer",
            "booking",
            "booking__project",
            "booking__plot",

        ),

        pk=registration_id,

    )

    timeline = registration.timeline.all()

    context = {

        "registration": registration,

        "timeline": timeline,

    }

    return render(

        request,

        "registrations/registration_profile.html",

        context,

    )
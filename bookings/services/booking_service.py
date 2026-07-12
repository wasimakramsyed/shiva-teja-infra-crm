from django.db import transaction
from django.core.exceptions import ValidationError
from bookings.services.activity_service import ActivityService
from bookings.models import Booking
from customers.models import Customer
from activities.activity_service import ActivityService as CRMActivityService
from leads.models import Lead
from projects.models import Plot


class BookingService:

    @staticmethod
    @transaction.atomic
    def create_booking(form, user):

        booking = form.save(commit=False)

        # -------------------------
        # Lock Plot
        # -------------------------

        plot = Plot.objects.select_for_update().get(
            id=booking.plot.id
        )

        if plot.status != "available":
            raise ValidationError(
                "This plot is already booked."
            )

        # -------------------------
        # Audit
        # -------------------------

        booking.created_by = user
        booking.updated_by = user

        # -------------------------
        # Lead Booking
        # -------------------------

        if booking.lead:

            lead = booking.lead

            booking.booking_source = "lead"

            booking.booked_client_name = lead.lead_name
            booking.mobile_number = lead.mobile_number

            booking.assigned_employee = lead.assigned_employee
            booking.assigned_team = lead.assigned_team

            lead.status = "converted"
            lead.save()
            ActivityService.log(
    booking=booking,
    activity="Lead Converted",
    description=f"Lead {lead.lead_name} converted into booking.",
    user=user
)

        # -------------------------
        # Direct Booking
        # -------------------------

        else:

            booking.booking_source = "walk_in"

        booking.save()
        ActivityService.log(
    booking=booking,
    activity="Booking Created",
    description=(
        f"Booking created for "
        f"{booking.booked_client_name}."
    ),
    user=user
)
        ActivityService.log(
    booking=booking,
    activity="Booking Created",
    description="New booking has been created.",
    user=user
)

        plot.status = "booked"
        plot.save()
        ActivityService.log(
    booking=booking,
    activity="Plot Reserved",
    description=f"Plot {plot.plot_number} reserved.",
    user=user
)

        customer, _ = Customer.objects.get_or_create(
            mobile_number=booking.mobile_number,
            defaults={
                "customer_name": booking.booked_client_name,
            },
        )

        CRMActivityService.create_activity(

            customer=customer,

            booking=booking,

            activity_type="booking",

            title="Booking Created",

            description=(
                f"Booking {booking.booking_id} created for "
                f"{booking.booked_client_name}."
            ),

            created_by=user,

            icon="fas fa-calendar-check",

            color="blue",

            is_system_generated=True,

        )

        return booking
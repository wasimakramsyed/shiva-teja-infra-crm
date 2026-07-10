from django.db import transaction
from django.core.exceptions import ValidationError
from commissions.services.commission_service import CommissionService
from bookings.services.activity_service import ActivityService
from customers.services.customer_service import CustomerService


class RegistrationService:

    @staticmethod
    @transaction.atomic
    def register_property(form, user):

        registration = form.save(commit=False)

        booking = registration.booking

        # -------------------------
        # Business Validations
        # -------------------------

        if booking.status != "fully_paid":

            raise ValidationError(
                "Only fully paid bookings can be registered."
            )

        if hasattr(booking, "registration"):

            raise ValidationError(
                "This booking is already registered."
            )

        # -------------------------
        # Save Registration
        # -------------------------

        registration.created_by = user
        registration.save()

        # -------------------------
        # Update Booking
        # -------------------------

        booking.status = "registered"
        booking.save()

        # -------------------------
        # Update Plot
        # -------------------------

        plot = booking.plot

        plot.status = "registered"
        plot.save()

        # -------------------------
        # Create Customer
        # -------------------------

        CustomerService.create_customer(
            registration
        )

        CommissionService.generate_commission(
            registration
        )

        # -------------------------
        # Timeline
        # -------------------------

        ActivityService.log(
            booking=booking,
            activity="Registration Completed",
            description="Property registration completed.",
            user=user
        )

        return registration
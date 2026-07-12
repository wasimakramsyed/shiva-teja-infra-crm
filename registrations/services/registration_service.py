from django.db import transaction

from activities.activity_service import ActivityService as CRMActivityService
from bookings.models import BookingActivity

from .timeline_service import RegistrationTimelineService


class RegistrationService:

    @staticmethod
    @transaction.atomic
    def register(

        registration,

        created_by,

    ):

        booking = registration.booking

        # -----------------------------------
        # Update Booking Status
        # -----------------------------------

        booking.status = "registered"

        booking.workflow_status = "registered"

        booking.save()

        # -----------------------------------
        # Booking Activity
        # -----------------------------------

        BookingActivity.objects.create(

            booking=booking,

            activity="Property Registered",

            description=(
                f"{registration.registration_id} created."
            ),

            created_by=created_by,

        )

        # -----------------------------------
        # Registration Timeline
        # -----------------------------------

        RegistrationTimelineService.create(

            registration=registration,

            activity="Registration Completed",

            created_by=created_by,

            remarks="Registration successfully completed.",

        )

        CRMActivityService.create_activity(

            customer=registration.customer,

            booking=booking,

            registration=registration,

            activity_type="registration",

            title="Registration Completed",

            description=(
                f"Registration {registration.registration_id} completed."
            ),

            created_by=created_by,

            icon="fas fa-certificate",

            color="purple",

            is_system_generated=True,

        )

        return registration

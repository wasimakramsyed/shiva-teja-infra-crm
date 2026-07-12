from django.shortcuts import get_object_or_404

from commissions.models import CommissionRequest


class CommissionRequestService:

    @staticmethod
    def get_request(request_id):

        commission_request = get_object_or_404(
            CommissionRequest.objects.select_related(
                "booking",
                "customer",
                "customer_property",
                "project",
                "plot",
                "employee",
                "team",
            ),
            pk=request_id,
        )

        if commission_request.status != "ready":

            raise ValueError(
                "This commission request has already been processed."
            )

        # Commission is created through the OneToOneField:
        # Commission.request = OneToOneField(...)
        if hasattr(commission_request, "commission"):

            raise ValueError(
                "Commission already generated."
            )

        return commission_request

    @staticmethod
    def create_request(customer_property):

        booking = customer_property.booking

        # Prevent duplicate commission requests
        if hasattr(booking, "commission_request"):

            return booking.commission_request

        commission_request = CommissionRequest.objects.create(

            booking=booking,

            customer=customer_property.customer,

            customer_property=customer_property,

            project=customer_property.project,

            plot=customer_property.plot,

            employee=booking.assigned_employee,

            team=booking.assigned_team,

            sale_amount=booking.booking_amount,

            booking_source=booking.booking_source,

            status="ready",

        )

        return commission_request
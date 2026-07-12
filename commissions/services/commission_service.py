from django.utils import timezone


class CommissionService:

    @staticmethod
    def approve_commission(commission, user):

        if commission.status != "generated":

            raise ValueError(
                "Only generated commissions can be approved."
            )

        commission.status = "approved"
        commission.approved_by = user
        commission.approved_at = timezone.now()

        commission.save(
            update_fields=[
                "status",
                "approved_by",
                "approved_at",
            ]
        )

        if hasattr(commission, "request"):

            booking = commission.request.booking

            if hasattr(booking, "workflow_status"):

                booking.workflow_status = "commission_approved"

                booking.save(
                    update_fields=[
                        "workflow_status",
                    ]
                )

        return commission

    @staticmethod
    def mark_paid(commission, user):

        if commission.status != "approved":

            raise ValueError(
                "Only approved commissions can be marked as paid."
            )

        commission.status = "paid"
        commission.paid_by = user
        commission.paid_at = timezone.now()

        commission.save(
            update_fields=[
                "status",
                "paid_by",
                "paid_at",
            ]
        )

        if hasattr(commission, "request"):

            booking = commission.request.booking

            if hasattr(booking, "workflow_status"):

                booking.workflow_status = "commission_paid"

                booking.save(
                    update_fields=[
                        "workflow_status",
                    ]
                )

        return commission
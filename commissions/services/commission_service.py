from decimal import Decimal
from django.utils import timezone

from commissions.models import (
    Commission,
    CommissionPolicy,
)

from bookings.services.activity_service import ActivityService
from notifications.models import Notification


class CommissionService:

    @staticmethod
    def generate_commission(registration):

        booking = registration.booking
        customer = booking.customer

        policy = CommissionPolicy.objects.filter(
            is_active=True
        ).first()

        if not policy:
            return None

        commission = Commission()

        commission.booking = booking
        commission.customer = customer
        commission.policy = policy

        commission.employee = booking.assigned_employee
        commission.team = booking.assigned_team

        commission.booking_value = booking.booking_amount

        # Employee Commission
        if policy.allow_employee and booking.assigned_employee:

            gross = (
                booking.booking_amount *
                policy.employee_percentage
            ) / Decimal("100")

            tds = (
                gross *
                policy.tds_percentage
            ) / Decimal("100")

            gst = Decimal("0")

            if policy.gst_applicable:

                gst = (
                    gross *
                    policy.gst_percentage
                ) / Decimal("100")

            commission.employee_percentage = policy.employee_percentage
            commission.employee_gross = gross
            commission.employee_tds = tds
            commission.employee_gst = gst
            commission.employee_net = gross - tds - gst

        # Team Commission
        if policy.allow_team and booking.assigned_team:

            gross = (
                booking.booking_amount *
                policy.team_percentage
            ) / Decimal("100")

            tds = (
                gross *
                policy.tds_percentage
            ) / Decimal("100")

            gst = Decimal("0")

            if policy.gst_applicable:

                gst = (
                    gross *
                    policy.gst_percentage
                ) / Decimal("100")

            commission.team_percentage = policy.team_percentage
            commission.team_gross = gross
            commission.team_tds = tds
            commission.team_gst = gst
            commission.team_net = gross - tds - gst

        commission.save()

        ActivityService.log(
            booking=booking,
            activity="Commission Generated",
            description=f"{commission.commission_id} generated."
        )

        Notification.objects.create(
            message=f"Commission {commission.commission_id} generated."
        )

        return commission

    @staticmethod
    def approve_commission(
        commission,
        user
    ):

        commission.status = "approved"
        commission.approved_by = user
        commission.approved_at = timezone.now()

        commission.save()

        ActivityService.log(
            booking=commission.booking,
            activity="Commission Approved",
            description=f"{commission.commission_id} approved.",
            user=user
        )

        Notification.objects.create(
            message=f"Commission {commission.commission_id} approved."
        )

    @staticmethod
    def mark_paid(
        commission,
        user
    ):

        commission.status = "paid"
        commission.paid_at = timezone.now()

        commission.save()

        ActivityService.log(
            booking=commission.booking,
            activity="Commission Paid",
            description=f"{commission.commission_id} paid.",
            user=user
        )

        Notification.objects.create(
            message=f"Commission {commission.commission_id} paid."
        )
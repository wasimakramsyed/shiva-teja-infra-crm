from django.db import transaction
from django.utils import timezone

from bookings.services.activity_service import ActivityService


class PaymentService:

    @staticmethod
    @transaction.atomic
    def receive_payment(form):

        payment = form.save(commit=False)

        booking = payment.booking

        # -----------------------------------
        # Generate Transaction ID
        # -----------------------------------

        if not payment.transaction_id:

            payment.transaction_id = (
                f"TXN{timezone.now().strftime('%Y%m%d%H%M%S')}"
            )

        payment.save()

        # -----------------------------------
        # Calculate Total Paid
        # -----------------------------------

        total_paid = booking.advance_amount

        total_paid += sum(
            p.amount
            for p in booking.payments.all()
        )

        booking.pending_amount = (
            booking.booking_amount -
            total_paid
        )

        if booking.pending_amount <= 0:

            booking.status = "fully_paid"

        else:

            booking.status = "partially_paid"

        booking.save()

        # -----------------------------------
        # Timeline
        # -----------------------------------

        ActivityService.log(
            booking=booking,
            activity="Payment Received",
            description=f"₹{payment.amount} received."
        )

        return payment
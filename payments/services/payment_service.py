from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from commissions.services.request_service import CommissionRequestService
from bookings.services.activity_service import ActivityService
from activities.activity_service import ActivityService as CRMActivityService
from customers.services.customer_service import CustomerService
from customers.models import Customer


class PaymentService:

    @staticmethod
    @transaction.atomic
    def receive_payment(form):

        payment = form.save(commit=False)

        booking = payment.booking

        # -----------------------------------
        # Calculate Current Paid Amount
        # -----------------------------------

        total_paid = booking.advance_amount + sum(
            p.amount for p in booking.payments.all()
        )

        remaining_amount = booking.booking_amount - total_paid

        # -----------------------------------
        # Prevent Fully Paid Booking
        # -----------------------------------

        if remaining_amount <= 0:

            raise ValidationError(
                "This booking is already fully paid. No more payments can be received."
            )

        # -----------------------------------
        # Prevent Over Payment
        # -----------------------------------

        if payment.amount > remaining_amount:

            raise ValidationError(
                f"Only ₹{remaining_amount} is pending for this booking."
            )

        # -----------------------------------
        # Generate Transaction ID
        # -----------------------------------

        if not payment.transaction_id:

            payment.transaction_id = (
                f"TXN{timezone.now().strftime('%Y%m%d%H%M%S')}"
            )

        payment.save()

        # -----------------------------------
        # Recalculate Paid Amount
        # -----------------------------------

        total_paid = booking.advance_amount + sum(
            p.amount for p in booking.payments.all()
        )

        booking.pending_amount = booking.booking_amount - total_paid

        # -----------------------------------
        # Booking Status
        # -----------------------------------

        if booking.pending_amount <= 0:

            booking.pending_amount = 0
            booking.status = "fully_paid"

            # Only if this field exists in your model
            if hasattr(booking, "workflow_status"):
                booking.workflow_status = "commission_ready"

            booking.save()

            # Create Customer only once
            if not hasattr(booking, "customer_property"):
                customer_property = CustomerService.create_customer(booking)
                CommissionRequestService.create_request(
                    customer_property
                )

        else:

            booking.status = "partially_paid"
            booking.save()

        # -----------------------------------
        # Timeline
        # -----------------------------------

        customer = getattr(
            getattr(booking, "customer_property", None),
            "customer",
            None,
        )

        if not customer:

            customer = Customer.objects.filter(
                mobile_number=booking.mobile_number
            ).first()

        if not customer:

            customer = Customer.objects.create(

                customer_name=booking.booked_client_name,

                mobile_number=booking.mobile_number,

            )

        CRMActivityService.create_activity(

            customer=customer,

            booking=booking,

            payment=payment,

            activity_type="payment",

            title="Payment Received",

            description=f"₹{payment.amount} received.",

            created_by=None,

            icon="fas fa-money-bill-wave",

            color="green",

            is_system_generated=True,

        )

        ActivityService.log(
            booking=booking,
            activity="Payment Received",
            description=f"₹{payment.amount} received."
        )

        return payment
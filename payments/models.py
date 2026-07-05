from django.db import models
from bookings.models import Booking
from customers.models import Customer
from django.db.models.signals import post_save
from django.dispatch import receiver


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    payment_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    payment_date = models.DateField()

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    payment_mode = models.CharField(
        max_length=50
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    receipt_number = models.CharField(
        max_length=30,
        unique=True
    )

    receipt_upload = models.FileField(
        upload_to='payment_receipts/',
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        if not self.payment_id:
            last_payment = Payment.objects.order_by(
                '-id'
            ).first()

            if last_payment:
                last_id = int(
                    last_payment.payment_id.replace(
                        'PAY',
                        ''
                    )
                )
                new_id = last_id + 1
            else:
                new_id = 1

            self.payment_id = f"PAY{new_id:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.payment_id


@receiver(post_save, sender=Payment)
def update_booking_payment(sender, instance, created, **kwargs):
    if created:
        booking = instance.booking

        total_paid = sum(
            payment.amount
            for payment in booking.payments.all()
        )

        booking.pending_amount = (
            booking.booking_amount - total_paid
        )

        if booking.pending_amount > 0:
            booking.status = 'partially_paid'
        else:
            booking.status = 'fully_paid'

        booking.save()


@receiver(post_save, sender=Payment)
def create_customer_on_full_payment(sender, instance, created, **kwargs):
    if created:
        booking = instance.booking

        if booking.pending_amount <= 0:
            Customer.objects.get_or_create(
                booking=booking,
                customer_name=booking.booked_client_name,
                mobile_number=booking.mobile_number
            )
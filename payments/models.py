from django.db import models
from bookings.models import Booking


class Payment(models.Model):
    PAYMENT_TYPES = [
        ('booking_amount', 'Booking Amount'),
        ('advance', 'Advance Payment'),
        ('installment', 'Installment'),
        ('final', 'Final Payment'),
        ('refund', 'Refund'),
    ]

    payment_id = models.CharField(max_length=20, unique=True)
    receipt_number = models.CharField(max_length=30, unique=True)

    payment_date = models.DateField()

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(max_digits=15, decimal_places=2)

    payment_mode = models.CharField(max_length=50)
    reference_number = models.CharField(max_length=100, blank=True, null=True)

    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPES
    )

    next_due_date = models.DateField(blank=True, null=True)
    next_due_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True
    )

    screenshot = models.FileField(upload_to='payment_docs/', blank=True, null=True)
    transaction_slip = models.FileField(upload_to='payment_docs/', blank=True, null=True)
    cheque_copy = models.FileField(upload_to='payment_docs/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
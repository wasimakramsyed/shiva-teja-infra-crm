from django.db import models
from bookings.models import Booking
from common.services.id_generator import IDGenerator

class Payment(models.Model):

    PAYMENT_MODE_CHOICES = [
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Bank Transfer", "Bank Transfer"),
        ("Cheque", "Cheque"),
        ("Demand Draft", "Demand Draft"),
    ]

    payment_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    receipt_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    transaction_id = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    payment_date = models.DateField()

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    payment_mode = models.CharField(
        max_length=30,
        choices=PAYMENT_MODE_CHOICES
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.payment_id:

            self.payment_id = IDGenerator.generate(
            model=Payment,
            field="payment_id",
            prefix="PAY"
            )

        if not self.receipt_number:

            self.receipt_number = IDGenerator.generate(
            model=Payment,
            field="receipt_number",
            prefix="RCPT"
            )

        if not self.transaction_id:

            self.transaction_id = IDGenerator.generate(
            model=Payment,
            field="transaction_id",
            prefix="TXN"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.payment_id
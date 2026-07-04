from django.db import models
from bookings.models import Booking
from django.db.models.signals import post_save
from django.dispatch import receiver
 

class Payment(models.Model):
    STATUS_CHOICES = [
        ('partial', 'Partial'),
        ('full', 'Full'),
    ]

    payment_id = models.CharField(
        max_length=20,
        unique=True
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

    receipt_number = models.CharField(
        max_length=30,
        unique=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='partial'
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.payment_id


@receiver(post_save, sender=Payment)
def update_booking_status(sender, instance, created, **kwargs):
    if created:
        total_paid = sum(
            payment.amount for payment in instance.booking.payments.all()
        )

        booking_amount = instance.booking.booking_amount

        if total_paid >= booking_amount:
            instance.booking.status = 'completed'
            instance.booking.save()

@receiver(post_save, sender=Payment)
def create_commission(sender, instance, created, **kwargs):
    if created:
        booking = instance.booking
        customer = booking.customer

        if customer.assigned_to:
            sale_value = booking.booking_amount
            commission_percentage = 5

            commission_amount = (
                sale_value * commission_percentage
            ) / 100

            tds = (commission_amount * 10) / 100
            net_commission = commission_amount - tds

            Commission.objects.create(
                receipt_number=f"COM-{instance.payment_id}",
                employee=customer.assigned_to,
                payment=instance,
                sale_value=sale_value,
                commission_percentage=commission_percentage,
                commission_amount=commission_amount,
                tds=tds,
                net_commission=net_commission
            )
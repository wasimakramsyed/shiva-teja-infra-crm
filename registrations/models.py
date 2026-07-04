from django.db import models
from bookings.models import Booking
from django.db.models.signals import post_save
from django.dispatch import receiver


class Registration(models.Model):
    registration_id = models.CharField(
        max_length=20,
        unique=True,
        default='REG-000'
    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='registration'
    )

    registration_date = models.DateField(
        auto_now_add=True
    )

    registrar_name = models.CharField(
        max_length=150,
        default='Default Registrar'
    )

    document_number = models.CharField(
        max_length=100,
        default='DOC-000'
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.registration_id


@receiver(post_save, sender=Registration)
def update_registration_status(sender, instance, created, **kwargs):
    if created:
        booking = instance.booking

        booking.status = 'registered'
        booking.save()

        plot = booking.plot
        plot.status = 'registered'
        plot.save()
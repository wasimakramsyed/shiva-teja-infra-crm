from django.db import models
from bookings.models import Booking


class Registration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    registration_number = models.CharField(max_length=30, unique=True)

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='registration'
    )

    registration_date = models.DateField()
    registrar_office = models.CharField(max_length=255)

    registration_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    registration_file = models.FileField(
        upload_to='registration_docs/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.registration_number
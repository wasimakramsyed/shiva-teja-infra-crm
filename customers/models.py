from django.db import models
from bookings.models import Booking
from common.services.id_generator import IDGenerator

class Customer(models.Model):
    REGISTRATION_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    OWNERSHIP_STATUS = [
        ('active', 'Active'),
        ('transferred', 'Transferred'),
        ('cancelled', 'Cancelled'),
    ]

    customer_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='customer'
    )

    customer_name = models.CharField(
        max_length=150
    )

    mobile_number = models.CharField(
        max_length=15
    )

    alternative_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    aadhaar = models.FileField(
        upload_to='customer_docs/',
        blank=True,
        null=True
    )

    pan = models.FileField(
        upload_to='customer_docs/',
        blank=True,
        null=True
    )

    photo = models.ImageField(
        upload_to='customer_photos/',
        blank=True,
        null=True
    )

    address_proof = models.FileField(
        upload_to='customer_docs/',
        blank=True,
        null=True
    )

    nominee_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    relationship = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    nominee_mobile = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_customers"
    )

    updated_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_customers"
    )
    registration_status = models.CharField(
        max_length=20,
        choices=REGISTRATION_STATUS,
        default='pending'
    )

    registration_date = models.DateField(
        blank=True,
        null=True
    )

    ownership_status = models.CharField(
        max_length=20,
        choices=OWNERSHIP_STATUS,
        default='active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.customer_id:

            self.customer_id = IDGenerator.generate(
            model=Customer,
            field="customer_id",
            prefix="CUS"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.customer_name
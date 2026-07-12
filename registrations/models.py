from django.db import models
from bookings.models import Booking
from customers.models import Customer
from accounts.models import User


class Registration(models.Model):

    registration_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="registration"
    )

    customer = models.OneToOneField(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registration"
    )

    registration_date = models.DateField()

    registrar_office = models.CharField(
        max_length=200
    )

    registration_number = models.CharField(
        max_length=100,
        unique=True
    )

    document_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    sale_deed_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    market_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    stamp_duty = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    registration_fee = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    # Documents

    sale_deed = models.FileField(
        upload_to="registrations/",
        blank=True,
        null=True
    )

    registration_copy = models.FileField(
        upload_to="registrations/",
        blank=True,
        null=True
    )

    ec_document = models.FileField(
        upload_to="registrations/",
        blank=True,
        null=True
    )

    tax_receipt = models.FileField(
        upload_to="registrations/",
        blank=True,
        null=True
    )

    other_document = models.FileField(
        upload_to="registrations/",
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.registration_id:
            last_registration = (
                Registration.objects
                .order_by("-id")
                .first()
            )

            if last_registration:

                last_id = int(
                    last_registration.registration_id.replace(
                        "REG",
                        ""
                    )
                )

                new_id = last_id + 1

            else:

                new_id = 1

            self.registration_id = f"REG{new_id:06d}"

        super().save(*args, **kwargs)

    def __str__(self):

        return self.registration_id


class RegistrationTimeline(models.Model):

    registration = models.ForeignKey(

        Registration,

        on_delete=models.CASCADE,

        related_name="timeline",

    )

    activity = models.CharField(

        max_length=200

    )

    remarks = models.TextField(

        blank=True,

        null=True,

    )

    created_by = models.ForeignKey(

        User,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return f"{self.registration.registration_id} - {self.activity}"
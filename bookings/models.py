from django.db import models
from django.core.exceptions import ValidationError
from leads.models import Lead
from projects.models import Project, Plot
from django.db.models.signals import post_save
from django.dispatch import receiver
from leads.models import Lead


class Booking(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('partially_paid', 'Partially Paid'),
        ('fully_paid', 'Fully Paid'),
        ('cancelled', 'Cancelled'),
        ('registered', 'Registered'),
    ]

    booking_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    booking_date = models.DateField()

    lead = models.ForeignKey(
    Lead,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='bookings'
)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    plot = models.ForeignKey(
        Plot,
        on_delete=models.CASCADE
    )

    booked_client_name = models.CharField(
    max_length=150,
    null=True,
    blank=True
)

    mobile_number = models.CharField(
    max_length=15,
    null=True,
    blank=True
)

    booking_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    advance_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    pending_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True
    )

    payment_mode = models.CharField(
        max_length=50
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    booking_remarks = models.TextField(
        blank=True,
        null=True
    )

    special_instructions = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='booked'
    )

    booking_form = models.FileField(
        upload_to='booking_docs/',
        blank=True,
        null=True
    )

    customer_photo = models.ImageField(
        upload_to='booking_docs/',
        blank=True,
        null=True
    )

    aadhaar = models.FileField(
        upload_to='booking_docs/',
        blank=True,
        null=True
    )

    pan = models.FileField(
        upload_to='booking_docs/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        if not self.booking_id:
            last_booking = Booking.objects.order_by(
                '-id'
            ).first()

            if last_booking:
                last_id = int(
                    last_booking.booking_id.replace(
                        'BOOK',
                        ''
                    )
                )
                new_id = last_id + 1
            else:
                new_id = 1

            self.booking_id = f"BOOK{new_id:03d}"

        self.pending_amount = (
            self.booking_amount - self.advance_amount
        )

        super().save(*args, **kwargs)

    def clean(self):
        if self.plot.status != 'available':
            raise ValidationError(
                "This plot is already booked or registered."
            )

    def __str__(self):
        return self.booking_id
    
    


@receiver(post_save, sender=Booking)
def update_plot_status(sender, instance, created, **kwargs):
    if created and instance.plot.status != 'booked':
        instance.plot.status = 'booked'
        instance.plot.save()
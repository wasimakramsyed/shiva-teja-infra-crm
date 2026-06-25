from django.db import models
from customers.models import Customer
from projects.models import Project, Plot
from django.db.models.signals import post_save
from django.dispatch import receiver


class Booking(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('registered', 'Registered'),
    ]

    booking_id = models.CharField(max_length=20, unique=True)
    booking_date = models.DateField()

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
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

    booking_amount = models.DecimalField(max_digits=15, decimal_places=2)

    payment_mode = models.CharField(max_length=50)
    reference_number = models.CharField(max_length=100, blank=True, null=True)

    booking_remarks = models.TextField(blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='booked'
    )

    booking_form = models.FileField(upload_to='booking_docs/', blank=True, null=True)
    customer_photo = models.ImageField(upload_to='booking_docs/', blank=True, null=True)
    aadhaar = models.FileField(upload_to='booking_docs/', blank=True, null=True)
    pan = models.FileField(upload_to='booking_docs/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.booking_id


@receiver(post_save, sender=Booking)
def update_plot_status(sender, instance, created, **kwargs):
    if created:
        instance.plot.status = 'booked'
        instance.plot.save()
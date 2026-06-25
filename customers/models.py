from django.db import models
from leads.models import Lead


class Customer(models.Model):
    lead = models.OneToOneField(
        Lead,
        on_delete=models.CASCADE,
        related_name='customer'
    )

    customer_name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=15)
    alternative_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    address = models.TextField()

    aadhaar = models.FileField(upload_to='customer_docs/', blank=True, null=True)
    pan = models.FileField(upload_to='customer_docs/', blank=True, null=True)
    photo = models.ImageField(upload_to='customer_photos/', blank=True, null=True)
    address_proof = models.FileField(upload_to='customer_docs/', blank=True, null=True)

    nominee_name = models.CharField(max_length=150, blank=True, null=True)
    relationship = models.CharField(max_length=100, blank=True, null=True)
    nominee_mobile = models.CharField(max_length=15, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name
from django.db import models
from bookings.models import Booking
from common.services.id_generator import IDGenerator
from projects.models import Project, Plot
from employees.models import Employee
from teams.models import Team
class Customer(models.Model):
    customer_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
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
    
class CustomerProperty(models.Model):

    REGISTRATION_STATUS = [
        ("pending", "Pending"),
        ("registered", "Registered"),
    ]

    COMMISSION_STATUS = [
        ("pending", "Pending"),
        ("generated", "Generated"),
        ("paid", "Paid"),
    ]

    OWNERSHIP_STATUS = [
        ("active", "Active"),
        ("transferred", "Transferred"),
        ("cancelled", "Cancelled"),
    ]

    property_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="properties"
    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="customer_property"
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT
    )

    plot = models.OneToOneField(
        Plot,
        on_delete=models.PROTECT
    )
    assigned_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    assigned_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    sale_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    paid_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    pending_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    commission_status = models.CharField(
        max_length=20,
        choices=COMMISSION_STATUS,
        default="pending"
    )

    registration_status = models.CharField(
        max_length=20,
        choices=REGISTRATION_STATUS,
        default="pending"
    )

    ownership_status = models.CharField(
        max_length=20,
        choices=OWNERSHIP_STATUS,
        default="active"
    )
    SALE_STATUS = [
        ("booked", "Booked"),
        ("fully_paid", "Fully Paid"),
        ("registered", "Registered"),
        ("cancelled", "Cancelled"),
    ]

    sale_status = models.CharField(
        max_length=20,
        choices=SALE_STATUS,
        default="booked"
    )
    payment_completed = models.BooleanField(
        default=True
    )
    remarks = models.TextField(
        blank=True,
        null=True
    )
    purchase_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.property_id:

            self.property_id = IDGenerator.generate(
                model=CustomerProperty,
                field="property_id",
                prefix="CPROP"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.customer_name} - {self.plot.plot_number}"
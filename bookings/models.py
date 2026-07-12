from django.db import models
from django.core.exceptions import ValidationError
from common.services.id_generator import IDGenerator
from leads.models import Lead
from projects.models import Project, Plot
from employees.models import Employee
from teams.models import Team
from accounts.models import User


class Booking(models.Model):

    STATUS_CHOICES = [
        ("booked", "Booked"),
        ("partially_paid", "Partially Paid"),
        ("fully_paid", "Fully Paid"),
        ("registered", "Registered"),
        ("cancelled", "Cancelled"),
    ]
    WORKFLOW_STATUS_CHOICES = [
        ("booked", "Booked"),
        ("commission_ready", "Commission Ready"),
        ("commission_generated", "Commission Generated"),
        ("commission_paid", "Commission Paid"),
        ("registered", "Registered"),
]

    BOOKING_SOURCE_CHOICES = [
        ("lead", "Lead"),
        ("walk_in", "Walk-in"),
        ("reference", "Reference"),
        ("online", "Online"),
    ]

    PAYMENT_MODE_CHOICES = [
        ("cash", "Cash"),
        ("upi", "UPI"),
        ("bank_transfer", "Bank Transfer"),
        ("cheque", "Cheque"),
        ("card", "Card"),
        ("demand_draft", "Demand Draft"),
    ]

    booking_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    booking_date = models.DateField()

    # -------------------------
    # Lead Information
    # -------------------------

    lead = models.ForeignKey(
        Lead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings"
    )

    booking_source = models.CharField(
        max_length=20,
        choices=BOOKING_SOURCE_CHOICES,
        default="walk_in"
    )

    # -------------------------
    # Permanent Ownership
    # -------------------------

    assigned_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings"
    )

    assigned_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings"
    )

    # -------------------------
    # Booking Details
    # -------------------------

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
        blank=True,
        null=True
    )

    mobile_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
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
        default=0
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE_CHOICES,
        default="cash"
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
        default="booked"
    )
    workflow_status = models.CharField(
        max_length=30,
        choices=WORKFLOW_STATUS_CHOICES,
        default="booked"
    )

    # -------------------------
    # Documents
    # -------------------------

    booking_form = models.FileField(
        upload_to="booking_docs/",
        blank=True,
        null=True
    )

    customer_photo = models.ImageField(
        upload_to="booking_docs/",
        blank=True,
        null=True
    )

    aadhaar = models.FileField(
        upload_to="booking_docs/",
        blank=True,
        null=True
    )

    pan = models.FileField(
        upload_to="booking_docs/",
        blank=True,
        null=True
    )

    # -------------------------
    # Audit
    # -------------------------

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_bookings"
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_bookings"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # -------------------------
    # Validation
    # -------------------------

    def clean(self):

        existing_booking = Booking.objects.filter(
        plot=self.plot
        ).exclude(
        pk=self.pk
        )

        if existing_booking.exists():

            raise ValidationError(
            "This plot is already booked."
            )

    # -------------------------
    # Save
    # -------------------------

    def save(self, *args, **kwargs):

    # Generate Booking ID
        if not self.booking_id:

            self.booking_id = IDGenerator.generate(
            model=Booking,
            field="booking_id",
            prefix="BOOK"
            )

    # Only calculate pending amount while creating booking
        if self._state.adding:

            self.pending_amount = (
            self.booking_amount -
            self.advance_amount
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.booking_id


class BookingActivity(models.Model):

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    activity = models.CharField(
        max_length=150
    )

    description = models.TextField(
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

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.booking.booking_id} - {self.activity}"
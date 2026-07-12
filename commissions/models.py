from django.db import models
from bookings.models import Booking
from customers.models import Customer, CustomerProperty
from projects.models import Project, Plot
from employees.models import Employee
from teams.models import Team
from common.services.id_generator import IDGenerator
from payments.models import Payment


class CommissionRequest(models.Model):

    STATUS_CHOICES = [
        ("ready", "Ready for Commission"),
        ("processing", "In Progress"),
        ("generated", "Commission Generated"),
        ("cancelled", "Cancelled"),
    ]

    request_id = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="commission_request"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    customer_property = models.OneToOneField(
        CustomerProperty,
        on_delete=models.CASCADE
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT
    )

    plot = models.ForeignKey(
        Plot,
        on_delete=models.PROTECT
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    sale_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    booking_source = models.CharField(
        max_length=20
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ready"
    )

    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commission_requests_created"
    )

    generated_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commission_requests_generated"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    generated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):

        if not self.request_id:

            self.request_id = IDGenerator.generate(
                model=CommissionRequest,
                field="request_id",
                prefix="STI-CR"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.request_id

class CommissionRecord(models.Model):

    STATUS_CHOICES = [
        ("generated", "Generated"),
        ("approved", "Approved"),
        ("released", "Released"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    record_id = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        db_index=True,
    )

    request = models.OneToOneField(
        "CommissionRequest",
        on_delete=models.CASCADE,
        related_name="record"
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.PROTECT,
        related_name="commission_records"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="commission_records",
    )

    customer_property = models.ForeignKey(
        CustomerProperty,
        on_delete=models.PROTECT,
        related_name="commission_records",
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name="commission_records"
    )

    plot = models.ForeignKey(
        Plot,
        on_delete=models.PROTECT,
        related_name="commission_records"
    )

    sale_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    gross_commission = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    tds_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    tds_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    other_deduction = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    net_commission = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="generated"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    generated_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_commission_records"
    )

    approved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_commission_records"
    )

    released_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="released_commission_records"
    )

    paid_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="paid_commission_records"
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    released_at = models.DateTimeField(
        null=True,
        blank=True
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    @property
    def total_allocated_percentage(self):
        return sum(
            allocation.percentage
            for allocation in self.allocations.all()
        )
    @property
    def total_allocated_amount(self):
        return sum(
            allocation.net_amount
            for allocation in self.allocations.all()
        )
    class Meta:
        ordering = ["-created_at"]
    def save(self, *args, **kwargs):

        if not self.record_id:

            self.record_id = IDGenerator.generate(
                model=CommissionRecord,
                field="record_id",
                prefix="STI-CMR"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.record_id
    
class CommissionAllocation(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
    ]

    allocation_id = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    commission = models.ForeignKey(
        "CommissionRecord",
        on_delete=models.CASCADE,
        related_name="allocations"
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="commission_allocations"
    )

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    gross_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    tds_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    net_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    class Meta:
        ordering = ["-created_at"]
    def save(self, *args, **kwargs):

        if not self.allocation_id:

            self.allocation_id = IDGenerator.generate(
                model=CommissionAllocation,
                field="allocation_id",
                prefix="STI-CA"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.allocation_id} - {self.employee}"
class CommissionTimeline(models.Model):

    timeline_id = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    commission = models.ForeignKey(
        CommissionRecord,
        on_delete=models.CASCADE,
        related_name="timeline"
    )

    ACTIVITY_CHOICES = [
        ("generated", "Generated"),
        ("approved", "Approved"),
        ("released", "Released"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    activity = models.CharField(
        max_length=20,
        choices=ACTIVITY_CHOICES,
        default="generated"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    class Meta:
        ordering = ["-created_at"]
    def save(self, *args, **kwargs):

        if not self.timeline_id:

            self.timeline_id = IDGenerator.generate(
                model=CommissionTimeline,
                field="timeline_id",
                prefix="STI-CT"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.timeline_id
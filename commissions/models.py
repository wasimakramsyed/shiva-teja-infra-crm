from django.db import models
from common.services.id_generator import IDGenerator

from accounts.models import User
from bookings.models import Booking
from customers.models import Customer
from employees.models import Employee
from teams.models import Team


# ==========================================================
# Commission Policy
# ==========================================================

class CommissionPolicy(models.Model):

    GENERATE_AFTER = [
        ("booking", "Booking"),
        ("full_payment", "Full Payment"),
        ("registration", "Registration"),
    ]

    policy_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    policy_name = models.CharField(
        max_length=100
    )

    effective_from = models.DateField()

    effective_to = models.DateField(
        blank=True,
        null=True
    )

    employee_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    team_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    allow_employee = models.BooleanField(
        default=True
    )

    allow_team = models.BooleanField(
        default=False
    )

    generate_after = models.CharField(
        max_length=30,
        choices=GENERATE_AFTER,
        default="registration"
    )

    tds_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10
    )

    gst_applicable = models.BooleanField(
        default=False
    )

    gst_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=18
    )

    approval_required = models.BooleanField(
        default=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_commission_policies"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.policy_id:

            self.policy_id = IDGenerator.generate(
                model=CommissionPolicy,
                field="policy_id",
                prefix="POL"
            )

        if self.is_active:

            CommissionPolicy.objects.exclude(
                pk=self.pk
            ).update(
                is_active=False
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.policy_name


# ==========================================================
# Commission
# ==========================================================

class Commission(models.Model):

    STATUS_CHOICES = [
        ("generated", "Generated"),
        ("approved", "Approved"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    commission_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="commission"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="commissions"
    )

    policy = models.ForeignKey(
        CommissionPolicy,
        on_delete=models.PROTECT,
        related_name="commissions"
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commissions"
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commissions"
    )

    booking_value = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    # Employee

    employee_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    employee_gross = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    employee_tds = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    employee_gst = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    employee_net = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    # Team

    team_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    team_gross = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    team_tds = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    team_gst = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    team_net = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="generated"
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_commissions"
    )

    approved_at = models.DateTimeField(
        blank=True,
        null=True
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True
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

    def save(self, *args, **kwargs):

        if not self.commission_id:

            self.commission_id = IDGenerator.generate(
                model=Commission,
                field="commission_id",
                prefix="COM"
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.commission_id
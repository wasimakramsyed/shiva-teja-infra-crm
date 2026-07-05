from django.db import models
from employees.models import Employee
from payments.models import Payment
from settings_config.models import CRMSettings


class Commission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('hold', 'Hold'),
    ]

    commission_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='commissions'
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='commissions'
    )

    commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    commission_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True
    )

    tds = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    net_commission = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    paid_date = models.DateField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        settings = CRMSettings.objects.first()

        if not self.commission_id:
            last_commission = Commission.objects.order_by(
                '-id'
            ).first()

            if last_commission:
                last_id = int(
                    last_commission.commission_id.replace(
                        'COM',
                        ''
                    )
                )
                new_id = last_id + 1
            else:
                new_id = 1

            self.commission_id = f"COM{new_id:03d}"

        # Dynamic commission calculation
        self.commission_amount = (
            self.payment.amount *
            self.commission_percentage
        ) / 100

        # Dynamic TDS from admin settings
        self.tds = (
            self.commission_amount *
            settings.tds_percentage
        ) / 100

        self.net_commission = (
            self.commission_amount - self.tds
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.commission_id
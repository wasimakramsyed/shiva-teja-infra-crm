from django.db import models
from employees.models import Employee
from payments.models import Payment


class Commission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
    ]

    receipt_number = models.CharField(max_length=30, unique=True)

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

    sale_value = models.DecimalField(max_digits=15, decimal_places=2)

    commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    commission_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    tds = models.DecimalField(
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
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.commission_amount = (
            self.sale_value * self.commission_percentage
        ) / 100

        self.net_commission = self.commission_amount - self.tds

        super().save(*args, **kwargs)

    def __str__(self):
        return self.receipt_number
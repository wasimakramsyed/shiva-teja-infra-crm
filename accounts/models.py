from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('sales', 'Sales Employee'),
        ('accounts', 'Accounts'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='sales'
    )

    mobile_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username
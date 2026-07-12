from random import randint
from datetime import timedelta
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
    
class OTP(models.Model):

    PURPOSE_CHOICES = [

        ("forgot_username", "Forgot Username"),

        ("forgot_password", "Forgot Password"),

    ]

    mobile_number = models.CharField(
        max_length=15
    )

    otp = models.CharField(
        max_length=6
    )

    purpose = models.CharField(
        max_length=30,
        choices=PURPOSE_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    verified = models.BooleanField(
        default=False
    )

    def is_expired(self):

        return timezone.now() > self.created_at + timedelta(minutes=5)

    @staticmethod
    def generate():
        return str(randint(100000, 999999))
from django.db import models


class Employee(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('resigned', 'Resigned'),
    ]

    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    father_spouse_name = models.CharField(max_length=100)

    mobile_number = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    address = models.TextField()
    designation = models.CharField(max_length=100)

    reporting_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    joining_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    aadhaar = models.FileField(upload_to='employee_docs/', blank=True, null=True)
    pan = models.FileField(upload_to='employee_docs/', blank=True, null=True)
    bank_account = models.CharField(max_length=30, blank=True, null=True)
    passbook = models.FileField(upload_to='employee_docs/', blank=True, null=True)
    photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.surname}"
from django.db import models


class Employee(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('resigned', 'Resigned'),
    ]

    DESIGNATION_CHOICES = [
        ('SA', 'Sales Advisor'),
        ('SO', 'Sales Officer'),
        ('ASM', 'Assistant Sales Manager'),
        ('SM', 'Sales Manager'),
        ('AGM', 'Assistant General Manager'),
        ('GM', 'General Manager'),
        ('DD', 'Deputy Director'),
        ('DIR', 'Director'),
        ('SD', 'Senior Director'),
        ('ED', 'Executive Director'),
        ('SED', 'Senior Executive Director'),
        ('VP', 'Vice President'),
        ('PRES', 'President'),
        ('MD', 'Managing Director'),
        ('CH', 'Chairman'),
    ]

    employee_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    father_spouse_name = models.CharField(max_length=100)

    mobile_number = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    address = models.TextField()

    designation = models.CharField(
        max_length=20,
        choices=DESIGNATION_CHOICES
    )

    reporting_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates'
    )

    joining_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    # Optional Documents
    aadhaar = models.FileField(
        upload_to='employee_docs/',
        blank=True,
        null=True
    )

    pan = models.FileField(
        upload_to='employee_docs/',
        blank=True,
        null=True
    )

    passbook = models.FileField(
        upload_to='employee_docs/',
        blank=True,
        null=True
    )

    photo = models.ImageField(
        upload_to='employee_photos/',
        blank=True,
        null=True
    )

    bank_account = models.CharField(
        max_length=30,
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
        if not self.employee_id:
            last_employee = Employee.objects.order_by(
                '-id'
            ).first()

            if last_employee:
                last_id = int(
                    last_employee.employee_id.replace(
                        'EMP',
                        ''
                    )
                )
                new_id = last_id + 1
            else:
                new_id = 1

            self.employee_id = f"EMP{new_id:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.surname}"
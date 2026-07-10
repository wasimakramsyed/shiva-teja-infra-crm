from django.db import models
from employees.models import Employee
from teams.models import Team
from projects.models import Project
from common.services.id_generator import IDGenerator

class Lead(models.Model):

    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
        ("negotiation", "Negotiation"),
        ("converted", "Converted"),
        ("lost", "Lost"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    lead_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    lead_name = models.CharField(
        max_length=150
    )

    mobile_number = models.CharField(
        max_length=15,
        unique=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    source = models.CharField(
        max_length=100
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads'
    )

    assigned_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        related_name='leads'
    )

    assigned_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        related_name='leads'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    follow_up_date = models.DateField(
        blank=True,
        null=True
    )

    next_follow_up = models.DateField(
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
        default='new'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.lead_id:

            self.lead_id = IDGenerator.generate(
            model=Lead,
            field="lead_id",
            prefix="LEAD"
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.lead_id} - {self.lead_name}"
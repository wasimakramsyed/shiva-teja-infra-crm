from django.db import models
from employees.models import Employee


class Team(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    team_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    team_name = models.CharField(
        max_length=100,
        unique=True
    )

    team_head = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        related_name='headed_teams'
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    members = models.ManyToManyField(
        Employee,
        related_name='teams'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.team_id:
            last_team = Team.objects.order_by(
                '-id'
            ).first()

            if last_team:
                last_id = int(
                    last_team.team_id.replace(
                        'TEAM',
                        ''
                    )
                )
                new_id = last_id + 1
            else:
                new_id = 1

            self.team_id = f"TEAM{new_id:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team_name} ({self.team_head})"
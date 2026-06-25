from django.db import models
from employees.models import Employee


class Team(models.Model):
    team_name = models.CharField(max_length=100, unique=True)

    team_head = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        related_name='headed_teams'
    )

    description = models.TextField(blank=True, null=True)

    members = models.ManyToManyField(
        Employee,
        related_name='teams'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team_name
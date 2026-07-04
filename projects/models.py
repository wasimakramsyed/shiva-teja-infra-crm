from django.db import models


class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('hold', 'On Hold'),
    ]

    project_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    project_name = models.CharField(
        max_length=200
    )

    location = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    total_plots = models.PositiveIntegerField()

    # Optional project value
    project_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True
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
        if not self.project_id:
            last_project = Project.objects.order_by(
                '-id'
            ).first()

            if last_project:
                last_id = int(
                    last_project.project_id.replace(
                        'PROJ',
                        ''
                    )
                )
                new_id = last_id + 1
            else:
                new_id = 1

            self.project_id = f"PROJ{new_id:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project_id} - {self.project_name}"


class Plot(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('registered', 'Registered'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='plots',
        blank=True,
        null=True
    )

    plot_number = models.CharField(
        max_length=50
    )

    plot_size = models.CharField(
        max_length=50
    )

    facing = models.CharField(
        max_length=50
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.plot_number} ({self.project.project_name if self.project else 'No Project'})"
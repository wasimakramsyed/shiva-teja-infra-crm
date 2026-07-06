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
        is_new = self.pk is None

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

        # Count existing plots
        existing_plots = self.plots.count()

        # Auto create missing plots
        if self.total_plots > existing_plots:
            for i in range(
                existing_plots + 1,
                self.total_plots + 1
            ):
                Plot.objects.create(
                    project=self,
                    plot_number=f"P{i:03d}",
                    plot_size="Not Assigned",
                    facing="Not Assigned",
                    status='available'
                )

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
        related_name='plots'
    )

    plot_number = models.CharField(
        max_length=50
    )

    plot_size = models.CharField(
        max_length=50,
        default="Not Assigned"
    )

    facing = models.CharField(
        max_length=50,
        default="Not Assigned"
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
        return (
            f"{self.plot_number} "
            f"({self.project.project_name})"
        )
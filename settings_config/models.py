from django.db import models


class CRMSettings(models.Model):
    tds_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10
    )

    gst_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=18
    )

    default_commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return "CRM Global Settings"
from django.db import models


class Vehicle(models.Model):
    """
    Register of company vehicles and machinery used for fuel tracking
    and efficiency analysis.
    """

    asset_identifier = models.CharField(
        max_length=150,
        unique=True,
        help_text="Vehicle plate number or machine name (e.g. KDJ 123A, Wheel Loader 1)"
    )

    assigned_operator = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="Driver or machine operator (stored as text)"
    )

    opening_odometer_reading = models.DecimalField(
        max_digits=12,
        decimal_places=1,
        help_text="Initial odometer or hour-meter reading"
    )

    closing_odometer_reading = models.DecimalField(
        max_digits=12,
        decimal_places=1,
        blank=True,
        null=True,
        help_text="Final odometer or hour-meter reading"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.asset_identifier
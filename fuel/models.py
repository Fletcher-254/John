from django.db import models

from vehicles.models import Vehicle


# ============================================================
# FUEL PURCHASE (STOCK IN)
# ============================================================

class FuelPurchase(models.Model):
    """
    Records every fuel purchase made by the company.
    This is the stock entering the company.
    """

    fuel_date = models.DateField()

    supplier = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    litres = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    receipt_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    receipt_file = models.FileField(
        upload_to="fuel/receipts/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-fuel_date", "-created_at"]

    def __str__(self):
        return f"{self.fuel_date} - {self.litres} L"


# ============================================================
# FUEL ISSUE (STOCK OUT)
# ============================================================

class FuelIssue(models.Model):
    """
    Records every fuel issue to a vehicle or machine.
    Used for efficiency calculations and stock reconciliation.
    """

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name="fuel_issues"
    )

    fuel_date = models.DateField()

    litres = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    odometer_reading = models.DecimalField(
        max_digits=12,
        decimal_places=1,
        help_text="Vehicle odometer or machine hour-meter reading at the time of fueling."
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "vehicle",
            "fuel_date",
            "created_at"
        ]

    def __str__(self):
        return (
            f"{self.vehicle.asset_identifier} | "
            f"{self.fuel_date} | "
            f"{self.litres} L"
        )
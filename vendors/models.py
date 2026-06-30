from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError


class Vendor(models.Model):
    """
    Companies or individuals the business deals with.
    """

    vendor_name = models.CharField(
        max_length=200,
        unique=True
    )

    service_type = models.CharField(
        max_length=150,
        help_text="Examples: Fuel Supplier, Hardware Supplier, Blasting, Transport"
    )

    contact_person = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        max_length=20
    )

    physical_address = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["vendor_name"]

    def __str__(self):
        return self.vendor_name


class VendorTransaction(models.Model):
    """
    Records every financial interaction with a vendor.

    Can represent:
    - Purchase of goods
    - Provision of services
    """

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("partial", "Partially Paid"),
        ("paid", "Paid"),
    )

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    transaction_date = models.DateField()

    invoice_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Leave blank if no invoice exists."
    )

    description = models.TextField(
        help_text="Products supplied or services rendered."
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Optional for services."
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Optional for services."
    )

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        help_text="Automatically calculated for goods. Enter manually for services."
    )

    amount_paid = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    balance_due = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        editable=False
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        editable=False
    )

    payment_date = models.DateField(
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-transaction_date"]

    def clean(self):

        # Quantity and unit price must either both exist or both be blank
        if (self.quantity is None) != (self.unit_price is None):
            raise ValidationError(
                "Quantity and unit price must either both be provided or both be left blank."
            )

        # Goods transaction
        if self.quantity is not None:

            if self.quantity <= 0:
                raise ValidationError({
                    "quantity": "Quantity must be greater than zero."
                })

            if self.unit_price <= 0:
                raise ValidationError({
                    "unit_price": "Unit price must be greater than zero."
                })

            expected_total = self.quantity * self.unit_price

        # Service transaction
        else:

            if self.total_amount <= 0:
                raise ValidationError({
                    "total_amount": "Total amount must be greater than zero."
                })

            expected_total = self.total_amount

        if self.amount_paid < 0:
            raise ValidationError({
                "amount_paid": "Amount paid cannot be negative."
            })

        if self.amount_paid > expected_total:
            raise ValidationError({
                "amount_paid": "Amount paid cannot exceed the total amount."
            })

    def save(self, *args, **kwargs):

        self.full_clean()

        # Automatically calculate total for goods
        if self.quantity is not None and self.unit_price is not None:
            self.total_amount = self.quantity * self.unit_price

        # Calculate balance
        self.balance_due = self.total_amount - self.amount_paid

        # Determine payment status
        if self.balance_due == Decimal("0.00"):
            self.payment_status = "paid"

        elif self.amount_paid == Decimal("0.00"):
            self.payment_status = "pending"

        else:
            self.payment_status = "partial"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vendor.vendor_name} - {self.transaction_date}"
from django.db import models


class Expense(models.Model):
    """
    Records operational expenses that have already been paid.
    Once created, an expense becomes a permanent accounting record.
    """

    CATEGORY_CHOICES = (
        ("office_supplies", "Office Supplies"),
        ("safety_equipment", "Safety Equipment"),
        ("transport", "Transport"),
        ("courier", "Courier Services"),
        ("communication", "Communication"),
        ("utilities", "Utilities"),
        ("maintenance", "Maintenance"),
        ("cleaning", "Cleaning"),
        ("government_fees", "Government Fees"),
        ("miscellaneous", "Miscellaneous"),
    )

    PAYMENT_METHOD_CHOICES = (
        ("cash", "Cash"),
        ("mpesa", "M-Pesa"),
        ("bank", "Bank Transfer"),
    )

    expense_date = models.DateField(
        help_text="Date the expense was incurred."
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField(
        help_text="Describe what was purchased or the service received."
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES
    )

    receipt_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Optional receipt or transaction reference."
    )

    receipt_image = models.ImageField(
        upload_to="expense_receipts/",
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

    class Meta:
        ordering = ["-expense_date", "-created_at"]

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.amount <= 0:
            raise ValidationError({
                "amount": "Amount must be greater than zero."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.expense_date} - {self.description} (KES {self.amount})"

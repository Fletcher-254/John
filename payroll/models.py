from django.db import models
from employees.models import Employee


# ==========================================================
# PAYROLL PERIOD
# ==========================================================

class PayrollPeriod(models.Model):
    """
    Defines a payroll period.

    Weekly  -> Casual employees (Monday - Sunday)
    Monthly -> Permanent employees
    """

    PERIOD_TYPES = (
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    )

    STATUS_CHOICES = (
        ("open", "Open"),
        ("closed", "Closed"),
    )

    period_type = models.CharField(
        max_length=20,
        choices=PERIOD_TYPES
    )

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open"
    )

    closed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-start_date"]
        unique_together = (
            "period_type",
            "start_date",
            "end_date",
        )

    def __str__(self):
        return (
            f"{self.get_period_type_display()} "
            f"{self.start_date} - {self.end_date}"
        )


# ==========================================================
# CASUAL PAYROLL
# ==========================================================

class CasualPayroll(models.Model):
    """
    One payroll record per casual employee per payroll week.
    """

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        limit_choices_to={"employment_type": "casual"},
        related_name="casual_payrolls"
    )

    payroll_period = models.ForeignKey(
        PayrollPeriod,
        on_delete=models.PROTECT,
        related_name="casual_payrolls"
    )

    days_worked = models.PositiveIntegerField()

    daily_wage = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    amount_due = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="pending"
    )

    mpesa_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = (
            "payment_status",
            "employee__full_name",
        )

        unique_together = (
            "employee",
            "payroll_period",
        )

    def __str__(self):
        return (
            f"{self.employee.employee_id} - "
            f"{self.payroll_period}"
        )


# ==========================================================
# PERMANENT PAYROLL
# ==========================================================

class PermanentPayroll(models.Model):
    """
    One payroll record per permanent employee per month.
    """

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        limit_choices_to={"employment_type": "permanent"},
        related_name="permanent_payrolls"
    )

    payroll_period = models.ForeignKey(
        PayrollPeriod,
        on_delete=models.PROTECT,
        related_name="permanent_payrolls"
    )

    monthly_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    allowances = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    overtime = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    bonuses = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    gross_pay = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    paye = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    sha = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    nssf = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    other_deductions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_deductions = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    net_pay = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="pending"
    )

    mpesa_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = (
            "payment_status",
            "employee__full_name",
        )

        unique_together = (
            "employee",
            "payroll_period",
        )

    def __str__(self):
        return (
            f"{self.employee.employee_id} - "
            f"{self.payroll_period}"
        )
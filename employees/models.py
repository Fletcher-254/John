from django.db import models
from django.core.exceptions import ValidationError


class Employee(models.Model):

    EMPLOYMENT_TYPES = (
        ("casual", "Casual"),
        ("permanent", "Permanent"),
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    full_name = models.CharField(
        max_length=200
    )

    national_id = models.CharField(
        max_length=20,
        unique=True
    )

    phone_number = models.CharField(
        max_length=20
    )

    passport_photo = models.ImageField(
        upload_to="employees/passports/",
        blank=True,
        null=True
    )

    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPES
    )

    job_role = models.CharField(
        max_length=100
    )

    date_employed = models.DateField()

    # Next of Kin
    next_of_kin_name = models.CharField(
        max_length=200
    )

    next_of_kin_phone = models.CharField(
        max_length=20
    )

    # Permanent employees only
    sha_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    nssf_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    monthly_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    # Casual employees only
    daily_wage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
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
        ordering = ["full_name"]

    def clean(self):
        """
        Enforce business rules depending on employment type.
        """

        if self.employment_type == "casual":

            if self.daily_wage is None:
                raise ValidationError({
                    "daily_wage": "Daily wage is required for casual employees."
                })

            if self.monthly_salary:
                raise ValidationError({
                    "monthly_salary": "Casual employees cannot have a monthly salary."
                })

        elif self.employment_type == "permanent":

            required = {}

            if not self.sha_number:
                required["sha_number"] = "SHA number is required."

            if not self.nssf_number:
                required["nssf_number"] = "NSSF number is required."

            if self.monthly_salary is None:
                required["monthly_salary"] = "Monthly salary is required."

            if self.daily_wage:
                required["daily_wage"] = "Permanent employees cannot have a daily wage."

            if required:
                raise ValidationError(required)

    def save(self, *args, **kwargs):

        self.full_clean()

        if not self.employee_id:

            last_employee = Employee.objects.order_by("-id").first()

            if last_employee:
                last_number = int(last_employee.employee_id.replace("EMP", ""))
                next_number = last_number + 1
            else:
                next_number = 1

            self.employee_id = f"EMP{next_number:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"
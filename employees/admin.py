from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "employee_id",
        "full_name",
        "employment_type",
        "job_role",
        "phone_number",
        "is_active",
    )

    list_filter = (
        "employment_type",
        "is_active",
        "job_role",
    )

    search_fields = (
        "employee_id",
        "full_name",
        "national_id",
        "phone_number",
        "next_of_kin_name",
    )

    readonly_fields = (
        "employee_id",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Employee Information",
            {
                "fields": (
                    "employee_id",
                    "full_name",
                    "passport_photo",
                    "national_id",
                    "phone_number",
                )
            },
        ),
        (
            "Employment Information",
            {
                "fields": (
                    "employment_type",
                    "job_role",
                    "date_employed",
                    "is_active",
                )
            },
        ),
        (
            "Next of Kin",
            {
                "fields": (
                    "next_of_kin_name",
                    "next_of_kin_phone",
                )
            },
        ),
        (
            "Permanent Employee Details",
            {
                "fields": (
                    "monthly_salary",
                    "sha_number",
                    "nssf_number",
                )
            },
        ),
        (
            "Casual Employee Details",
            {
                "fields": (
                    "daily_wage",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )



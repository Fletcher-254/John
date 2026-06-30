from django.contrib import admin

from .models import (
    PayrollPeriod,
    CasualPayroll,
    PermanentPayroll,
)


# ==========================================================
# PAYROLL PERIOD
# ==========================================================

@admin.register(PayrollPeriod)
class PayrollPeriodAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "period_type",
        "start_date",
        "end_date",
        "status",
        "closed_at",
    )

    list_filter = (
        "period_type",
        "status",
    )

    search_fields = (
        "start_date",
        "end_date",
    )

    ordering = (
        "-start_date",
    )

    readonly_fields = (
        "created_at",
        "closed_at",
    )


# ==========================================================
# CASUAL PAYROLL
# ==========================================================

@admin.register(CasualPayroll)
class CasualPayrollAdmin(admin.ModelAdmin):

    list_display = (
        "employee",
        "payroll_period",
        "days_worked",
        "daily_wage",
        "amount_due",
        "payment_status",
        "paid_at",
    )

    list_filter = (
        "payment_status",
        "payroll_period",
    )

    search_fields = (
        "employee__employee_id",
        "employee__full_name",
    )

    ordering = (
        "-payroll_period__start_date",
        "employee__full_name",
    )

    readonly_fields = (
        "created_at",
        "paid_at",
    )


# ==========================================================
# PERMANENT PAYROLL
# ==========================================================

@admin.register(PermanentPayroll)
class PermanentPayrollAdmin(admin.ModelAdmin):

    list_display = (
        "employee",
        "payroll_period",
        "gross_pay",
        "total_deductions",
        "net_pay",
        "payment_status",
        "paid_at",
    )

    list_filter = (
        "payment_status",
        "payroll_period",
    )

    search_fields = (
        "employee__employee_id",
        "employee__full_name",
    )

    ordering = (
        "-payroll_period__start_date",
        "employee__full_name",
    )

    readonly_fields = (
        "created_at",
        "paid_at",
    )

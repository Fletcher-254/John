from rest_framework import serializers

from .models import (
    PayrollPeriod,
    CasualPayroll,
    PermanentPayroll,
)


# ==========================================================
# PAYROLL PERIOD
# ==========================================================

class PayrollPeriodSerializer(serializers.ModelSerializer):

    class Meta:
        model = PayrollPeriod
        fields = "__all__"
        read_only_fields = (
            "id",
            "status",
            "closed_at",
            "created_at",
        )


# ==========================================================
# CASUAL PAYROLL
# ==========================================================

class CasualPayrollSerializer(serializers.ModelSerializer):

    employee_id = serializers.CharField(
        source="employee.employee_id",
        read_only=True
    )

    employee_name = serializers.CharField(
        source="employee.full_name",
        read_only=True
    )

    class Meta:
        model = CasualPayroll
        fields = (
            "id",
            "employee",
            "employee_id",
            "employee_name",
            "payroll_period",
            "days_worked",
            "daily_wage",
            "amount_due",
            "payment_status",
            "mpesa_reference",
            "paid_at",
            "created_at",
        )

        read_only_fields = (
            "id",
            "employee_id",
            "employee_name",
            "created_at",
        )


# ==========================================================
# PERMANENT PAYROLL
# ==========================================================

class PermanentPayrollSerializer(serializers.ModelSerializer):

    employee_id = serializers.CharField(
        source="employee.employee_id",
        read_only=True
    )

    employee_name = serializers.CharField(
        source="employee.full_name",
        read_only=True
    )

    class Meta:
        model = PermanentPayroll
        fields = (
            "id",
            "employee",
            "employee_id",
            "employee_name",
            "payroll_period",
            "monthly_salary",
            "allowances",
            "overtime",
            "bonuses",
            "gross_pay",
            "paye",
            "sha",
            "nssf",
            "other_deductions",
            "total_deductions",
            "net_pay",
            "payment_status",
            "mpesa_reference",
            "paid_at",
            "created_at",
        )

        read_only_fields = (
            "id",
            "employee_id",
            "employee_name",
            "created_at",
        )
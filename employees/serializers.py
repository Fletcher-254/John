from rest_framework import serializers
from .models import Employee


# -------------------------------------------------
# ADMIN SERIALIZER
# -------------------------------------------------
class EmployeeAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_id",
            "full_name",
            "national_id",
            "phone_number",
            "passport_photo",
            "employment_type",
            "job_role",
            "date_employed",
            "next_of_kin_name",
            "next_of_kin_phone",
            "is_active",
        ]
        read_only_fields = ["id", "employee_id"]

    def validate(self, data):
        employment_type = data.get(
            "employment_type",
            self.instance.employment_type if self.instance else None
        )

        if employment_type == "casual":
            if data.get("monthly_salary"):
                raise serializers.ValidationError({
                    "monthly_salary": "Casual employees cannot have a monthly salary."
                })

        if employment_type == "permanent":
            if data.get("daily_wage"):
                raise serializers.ValidationError({
                    "daily_wage": "Permanent employees cannot have a daily wage."
                })

        return data


# -------------------------------------------------
# MANAGER SERIALIZER
# Manager can update DAILY WAGE ONLY
# -------------------------------------------------
class EmployeeManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_id",
            "full_name",
            "employment_type",
            "daily_wage",
        ]
        read_only_fields = [
            "id",
            "employee_id",
            "full_name",
            "employment_type",
        ]

    def validate_daily_wage(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Daily wage must be greater than zero."
            )
        return value


# -------------------------------------------------
# DIRECTOR SERIALIZER
# Director can manage permanent staff payments
# -------------------------------------------------
class EmployeeDirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_id",
            "full_name",
            "employment_type",
            "monthly_salary",
            "sha_number",
            "nssf_number",
        ]
        read_only_fields = [
            "id",
            "employee_id",
            "full_name",
            "employment_type",
        ]

    def validate_monthly_salary(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Monthly salary must be greater than zero."
            )
        return value
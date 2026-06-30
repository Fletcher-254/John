from rest_framework import serializers

from .models import FuelPurchase, FuelIssue


# ============================================================
# FUEL PURCHASE
# ============================================================

class FuelPurchaseSerializer(serializers.ModelSerializer):
    """
    Used for creating and viewing fuel purchases.
    Receipt upload is mandatory.
    """

    class Meta:
        model = FuelPurchase
        fields = [
            "id",
            "fuel_date",
            "supplier",
            "litres",
            "cost",
            "receipt_reference",
            "receipt_file",
            "created_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
        )

    def validate_litres(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Litres must be greater than zero."
            )
        return value

    def validate_cost(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Cost must be greater than zero."
            )
        return value

    def validate(self, attrs):
        if not attrs.get("receipt_file"):
            raise serializers.ValidationError({
                "receipt_file": "Receipt or ETR upload is required."
            })

        return attrs


# ============================================================
# FUEL ISSUE
# ============================================================

class FuelIssueSerializer(serializers.ModelSerializer):
    """
    Used for recording and viewing fuel issues.
    Automatically updates the vehicle's latest odometer reading.
    """

    vehicle_name = serializers.CharField(
        source="vehicle.asset_identifier",
        read_only=True
    )

    class Meta:
        model = FuelIssue
        fields = [
            "id",
            "vehicle",
            "vehicle_name",
            "fuel_date",
            "litres",
            "odometer_reading",
            "remarks",
            "created_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "vehicle_name",
        )

    def validate_litres(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Litres must be greater than zero."
            )
        return value

    def validate_odometer_reading(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Odometer reading cannot be negative."
            )
        return value

    def validate(self, attrs):
        vehicle = attrs["vehicle"]
        reading = attrs["odometer_reading"]

        last_issue = (
            FuelIssue.objects
            .filter(vehicle=vehicle)
            .order_by("-fuel_date", "-created_at")
            .first()
        )

        if last_issue:
            if reading < last_issue.odometer_reading:
                raise serializers.ValidationError({
                    "odometer_reading":
                        "Odometer reading cannot be lower than the previous recorded reading."
                })
        else:
            if reading < vehicle.opening_odometer_reading:
                raise serializers.ValidationError({
                    "odometer_reading":
                        "Odometer reading cannot be lower than the opening odometer reading."
                })

        return attrs

    def create(self, validated_data):
        fuel_issue = FuelIssue.objects.create(**validated_data)

        vehicle = fuel_issue.vehicle

        # Update latest odometer reading on the vehicle
        vehicle.closing_odometer_reading = fuel_issue.odometer_reading
        vehicle.save(update_fields=["closing_odometer_reading"])

        return fuel_issue
from rest_framework import serializers

from .models import Vehicle


# =====================================================
# VEHICLE READ SERIALIZER
# =====================================================

class VehicleSerializer(serializers.ModelSerializer):
    """
    Used for listing and retrieving vehicle/machinery records.
    """

    class Meta:
        model = Vehicle
        fields = [
            "id",
            "asset_identifier",
            "assigned_operator",
            "opening_odometer_reading",
            "closing_odometer_reading",
            "remarks",
            "created_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
        )


# =====================================================
# VEHICLE CREATE SERIALIZER
# =====================================================

class VehicleCreateSerializer(serializers.ModelSerializer):
    """
    Used by admin to register a new vehicle or machine.
    """

    class Meta:
        model = Vehicle
        fields = [
            "asset_identifier",
            "assigned_operator",
            "opening_odometer_reading",
            "closing_odometer_reading",
            "remarks",
        ]

    def validate(self, data):
        """
        Basic consistency check for odometer readings.
        """

        opening = data.get("opening_odometer_reading")
        closing = data.get("closing_odometer_reading")

        if closing is not None and opening is not None:
            if closing < opening:
                raise serializers.ValidationError(
                    "Closing odometer reading cannot be less than opening reading."
                )

        return data
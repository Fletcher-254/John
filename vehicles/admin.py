from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    list_display = (
        "asset_identifier",
        "assigned_operator",
        "opening_odometer_reading",
        "closing_odometer_reading",
        "created_at",
    )

    search_fields = (
        "asset_identifier",
        "assigned_operator",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        ("Asset Details", {
            "fields": (
                "asset_identifier",
                "assigned_operator",
            )
        }),
        ("Odometer Readings", {
            "fields": (
                "opening_odometer_reading",
                "closing_odometer_reading",
            )
        }),
        ("System Info", {
            "fields": (
                "created_at",
            )
        }),
    )

    # -----------------------------------------
    # IMMUTABILITY RULES
    # -----------------------------------------

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
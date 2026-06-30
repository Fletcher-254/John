from django.contrib import admin

from .models import FuelPurchase, FuelIssue


# ==========================================================
# FUEL PURCHASE ADMIN
# ==========================================================

@admin.register(FuelPurchase)
class FuelPurchaseAdmin(admin.ModelAdmin):

    list_display = (
        "fuel_date",
        "supplier",
        "litres",
        "cost",
        "receipt_reference",
        "created_at",
    )

    list_filter = (
        "fuel_date",
        "supplier",
    )

    search_fields = (
        "supplier",
        "receipt_reference",
    )

    ordering = (
        "-fuel_date",
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False


# ==========================================================
# FUEL ISSUE ADMIN
# ==========================================================

@admin.register(FuelIssue)
class FuelIssueAdmin(admin.ModelAdmin):

    list_display = (
        "vehicle",
        "fuel_date",
        "litres",
        "odometer_reading",
        "created_at",
    )

    list_filter = (
        "fuel_date",
        "vehicle",
    )

    search_fields = (
        "vehicle__asset_identifier",
        "vehicle__assigned_operator",
    )

    ordering = (
        "-fuel_date",
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False

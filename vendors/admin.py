from django.contrib import admin

from .models import Vendor, VendorTransaction


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        "vendor_name",
        "service_type",
        "phone_number",
        "is_active",
        "created_at",
    )

    list_filter = (
        "service_type",
        "is_active",
    )

    search_fields = (
        "vendor_name",
        "contact_person",
        "phone_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "vendor_name",
    )

    fieldsets = (
        ("Vendor Information", {
            "fields": (
                "vendor_name",
                "service_type",
                "contact_person",
                "phone_number",
                "physical_address",
                "is_active",
            )
        }),
        ("Audit Information", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


@admin.register(VendorTransaction)
class VendorTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "vendor",
        "transaction_date",
        "invoice_number",
        "total_amount",
        "amount_paid",
        "balance_due",
        "payment_status",
    )

    list_filter = (
        "payment_status",
        "transaction_date",
    )

    search_fields = (
        "vendor__vendor_name",
        "invoice_number",
        "description",
    )

    readonly_fields = (
        "balance_due",
        "payment_status",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-transaction_date",
    )

    fieldsets = (
        ("Transaction Details", {
            "fields": (
                "vendor",
                "transaction_date",
                "invoice_number",
                "description",
            )
        }),
        ("Amounts", {
            "fields": (
                "quantity",
                "unit_price",
                "total_amount",
                "amount_paid",
                "balance_due",
            )
        }),
        ("Payment", {
            "fields": (
                "payment_status",
                "payment_date",
                "remarks",
            )
        }),
        ("Audit Information", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


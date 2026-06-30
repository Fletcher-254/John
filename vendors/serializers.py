from rest_framework import serializers

from .models import Vendor, VendorTransaction


# =====================================================
# VENDOR SERIALIZERS
# =====================================================

class VendorSerializer(serializers.ModelSerializer):
    """
    Used for listing and retrieving vendors.
    """

    class Meta:
        model = Vendor
        fields = [
            "id",
            "vendor_name",
            "service_type",
            "contact_person",
            "phone_number",
            "physical_address",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class VendorCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Used by the manager to create and update vendors.
    """

    class Meta:
        model = Vendor
        fields = [
            "vendor_name",
            "service_type",
            "contact_person",
            "phone_number",
            "physical_address",
            "is_active",
        ]


# =====================================================
# VENDOR TRANSACTION SERIALIZERS
# =====================================================

class VendorTransactionSerializer(serializers.ModelSerializer):
    """
    Used for listing and retrieving vendor transactions.
    """

    vendor_name = serializers.CharField(
        source="vendor.vendor_name",
        read_only=True
    )

    class Meta:
        model = VendorTransaction
        fields = [
            "id",
            "vendor",
            "vendor_name",
            "transaction_date",
            "invoice_number",
            "description",
            "quantity",
            "unit_price",
            "total_amount",
            "amount_paid",
            "balance_due",
            "payment_status",
            "payment_date",
            "remarks",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "balance_due",
            "payment_status",
            "created_at",
            "updated_at",
        )


class VendorTransactionCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Used by the manager to create and update vendor transactions.
    """

    class Meta:
        model = VendorTransaction
        fields = [
            "vendor",
            "transaction_date",
            "invoice_number",
            "description",
            "quantity",
            "unit_price",
            "total_amount",
            "amount_paid",
            "payment_date",
            "remarks",
        ]
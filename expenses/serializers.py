from rest_framework import serializers

from .models import Expense


# =====================================================
# EXPENSE SERIALIZER
# =====================================================

class ExpenseSerializer(serializers.ModelSerializer):
    """
    Used for listing and retrieving expense records.
    """

    category_display = serializers.CharField(
        source="get_category_display",
        read_only=True
    )

    payment_method_display = serializers.CharField(
        source="get_payment_method_display",
        read_only=True
    )

    class Meta:
        model = Expense
        fields = [
            "id",
            "expense_date",
            "category",
            "category_display",
            "description",
            "amount",
            "payment_method",
            "payment_method_display",
            "receipt_number",
            "receipt_image",
            "remarks",
            "created_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
        )


# =====================================================
# CREATE EXPENSE SERIALIZER
# =====================================================

class ExpenseCreateSerializer(serializers.ModelSerializer):
    """
    Used by the admin to record a new expense.
    """

    class Meta:
        model = Expense
        fields = [
            "expense_date",
            "category",
            "description",
            "amount",
            "payment_method",
            "receipt_number",
            "receipt_image",
            "remarks",
        ]
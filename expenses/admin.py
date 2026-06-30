from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):

    list_display = (
        "expense_date",
        "category",
        "description",
        "amount",
        "payment_method",
        "created_at",
    )

    list_filter = (
        "category",
        "payment_method",
        "expense_date",
    )

    search_fields = (
        "description",
        "receipt_number",
        "remarks",
    )

    readonly_fields = (
        "expense_date",
        "category",
        "description",
        "amount",
        "payment_method",
        "receipt_number",
        "receipt_image",
        "remarks",
        "created_at",
    )

    ordering = (
        "-expense_date",
        "-created_at",
    )

    def has_change_permission(self, request, obj=None):
        """
        Prevent editing of expense records.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of expense records.
        """
        return False
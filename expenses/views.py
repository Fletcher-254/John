from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.permissions import (
    IsAdmin,
    IsAdminManagerOrDirector,
)

from .models import Expense
from .serializers import (
    ExpenseSerializer,
    ExpenseCreateSerializer,
)


# =====================================================
# LIST ALL EXPENSES
# =====================================================

class ExpenseListView(APIView):
    permission_classes = [IsAdminManagerOrDirector]

    def get(self, request):
        expenses = Expense.objects.all()

        serializer = ExpenseSerializer(
            expenses,
            many=True
        )

        return Response(serializer.data)


# =====================================================
# CREATE EXPENSE
# =====================================================

class ExpenseCreateView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):

        serializer = ExpenseCreateSerializer(
            data=request.data
        )

        if serializer.is_valid():
            expense = serializer.save()

            return Response(
                ExpenseSerializer(expense).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =====================================================
# EXPENSE DETAIL
# =====================================================

class ExpenseDetailView(APIView):
    permission_classes = [IsAdminManagerOrDirector]

    def get(self, request, pk):

        try:
            expense = Expense.objects.get(pk=pk)

        except Expense.DoesNotExist:
            return Response(
                {"error": "Expense not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExpenseSerializer(expense)

        return Response(serializer.data)


# =====================================================
# TODAY'S EXPENSES
# =====================================================

class DailyExpenseView(APIView):
    permission_classes = [IsAdminManagerOrDirector]

    def get(self, request):

        today = timezone.localdate()

        expenses = Expense.objects.filter(
            expense_date=today
        )

        total = expenses.aggregate(
            total=Sum("amount")
        )["total"] or 0

        serializer = ExpenseSerializer(
            expenses,
            many=True
        )

        return Response({
            "date": today,
            "total": total,
            "expenses": serializer.data
        })


# =====================================================
# CURRENT MONTH EXPENSES
# =====================================================

class MonthlyExpenseView(APIView):
    permission_classes = [IsAdminManagerOrDirector]

    def get(self, request):

        today = timezone.localdate()

        expenses = Expense.objects.filter(
            expense_date__year=today.year,
            expense_date__month=today.month
        )

        total = expenses.aggregate(
            total=Sum("amount")
        )["total"] or 0

        serializer = ExpenseSerializer(
            expenses,
            many=True
        )

        return Response({
            "month": today.strftime("%B %Y"),
            "total": total,
            "expenses": serializer.data
        })


# =====================================================
# CURRENT YEAR EXPENSES
# =====================================================

class YearlyExpenseView(APIView):
    permission_classes = [IsAdminManagerOrDirector]

    def get(self, request):

        today = timezone.localdate()

        expenses = Expense.objects.filter(
            expense_date__year=today.year
        )

        total = expenses.aggregate(
            total=Sum("amount")
        )["total"] or 0

        serializer = ExpenseSerializer(
            expenses,
            many=True
        )

        return Response({
            "year": today.year,
            "total": total,
            "expenses": serializer.data
        })


# =====================================================
# MONTHLY SUMMARY
# =====================================================

class MonthlyExpenseSummaryView(APIView):
    permission_classes = [IsAdminManagerOrDirector]

    def get(self, request):

        summary = (
            Expense.objects
            .annotate(month=TruncMonth("expense_date"))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("-month")
        )

        return Response(summary)


# =====================================================
# YEARLY SUMMARY
# =====================================================

class YearlyExpenseSummaryView(APIView):
    permission_classes = [IsAdminManagerOrDirector]

    def get(self, request):

        summary = (
            Expense.objects
            .annotate(year=TruncYear("expense_date"))
            .values("year")
            .annotate(total=Sum("amount"))
            .order_by("-year")
        )

        return Response(summary)
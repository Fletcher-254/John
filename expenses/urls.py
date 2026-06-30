from django.urls import path

from .views import (
    ExpenseListView,
    ExpenseCreateView,
    ExpenseDetailView,
    DailyExpenseView,
    MonthlyExpenseView,
    YearlyExpenseView,
    MonthlyExpenseSummaryView,
    YearlyExpenseSummaryView,
)

urlpatterns = [

    # ==========================================
    # EXPENSE RECORDS
    # ==========================================

    path(
        "",
        ExpenseListView.as_view(),
        name="expense-list"
    ),

    path(
        "create/",
        ExpenseCreateView.as_view(),
        name="expense-create"
    ),

    path(
        "<int:pk>/",
        ExpenseDetailView.as_view(),
        name="expense-detail"
    ),

    # ==========================================
    # REPORTS
    # ==========================================

    path(
        "daily/",
        DailyExpenseView.as_view(),
        name="daily-expenses"
    ),

    path(
        "monthly/",
        MonthlyExpenseView.as_view(),
        name="monthly-expenses"
    ),

    path(
        "yearly/",
        YearlyExpenseView.as_view(),
        name="yearly-expenses"
    ),

    path(
        "monthly-summary/",
        MonthlyExpenseSummaryView.as_view(),
        name="monthly-expense-summary"
    ),

    path(
        "yearly-summary/",
        YearlyExpenseSummaryView.as_view(),
        name="yearly-expense-summary"
    ),
]
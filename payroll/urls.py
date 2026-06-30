from django.urls import path

from .views import (
    # Casual Payroll
    CasualPayrollListView,
    CasualPayrollDetailView,
    PayCasualEmployeeView,
    WeeklyPayrollSummaryView,

    # Permanent Payroll
    PermanentPayrollListView,
    PermanentPayrollDetailView,
    SavePermanentPayrollView,
    PayPermanentEmployeeView,
    MonthlyPayrollSummaryView,

    # Payroll History
    PayrollHistoryView,

    # Payroll Period
    ClosePayrollPeriodView,
)

urlpatterns = [

    # ==========================================================
    # CASUAL PAYROLL
    # ==========================================================

    path(
        "casual/",
        CasualPayrollListView.as_view(),
        name="casual-payroll-list"
    ),

    path(
        "casual/<int:pk>/",
        CasualPayrollDetailView.as_view(),
        name="casual-payroll-detail"
    ),

    path(
        "casual/<int:pk>/pay/",
        PayCasualEmployeeView.as_view(),
        name="pay-casual-employee"
    ),

    path(
        "casual/summary/",
        WeeklyPayrollSummaryView.as_view(),
        name="weekly-payroll-summary"
    ),

    # ==========================================================
    # PERMANENT PAYROLL
    # ==========================================================

    path(
        "permanent/",
        PermanentPayrollListView.as_view(),
        name="permanent-payroll-list"
    ),

    path(
        "permanent/<int:pk>/",
        PermanentPayrollDetailView.as_view(),
        name="permanent-payroll-detail"
    ),

    path(
        "permanent/<int:pk>/save/",
        SavePermanentPayrollView.as_view(),
        name="save-permanent-payroll"
    ),

    path(
        "permanent/<int:pk>/pay/",
        PayPermanentEmployeeView.as_view(),
        name="pay-permanent-employee"
    ),

    path(
        "permanent/summary/",
        MonthlyPayrollSummaryView.as_view(),
        name="monthly-payroll-summary"
    ),

    # ==========================================================
    # PAYROLL HISTORY
    # ==========================================================

    path(
        "history/",
        PayrollHistoryView.as_view(),
        name="payroll-history"
    ),

    # ==========================================================
    # PAYROLL PERIOD
    # ==========================================================

    path(
        "period/<int:pk>/close/",
        ClosePayrollPeriodView.as_view(),
        name="close-payroll-period"
    ),
]
from django.urls import path

from .views import (
    FuelPurchaseListView,
    FuelPurchaseCreateView,
    FuelPurchaseDetailView,
    FuelIssueListView,
    FuelIssueCreateView,
    FuelIssueDetailView,
    FuelDailySummaryView,
    FuelMonthlySummaryView,
    FuelReconciliationView,
    VehicleFuelEfficiencyView,
    FleetFuelEfficiencyView,
)

urlpatterns = [

    # ==========================================================
    # FUEL PURCHASES
    # ==========================================================

    path(
        "purchases/",
        FuelPurchaseListView.as_view(),
        name="fuel-purchase-list",
    ),

    path(
        "purchases/create/",
        FuelPurchaseCreateView.as_view(),
        name="fuel-purchase-create",
    ),

    path(
        "purchases/<int:pk>/",
        FuelPurchaseDetailView.as_view(),
        name="fuel-purchase-detail",
    ),


    # ==========================================================
    # FUEL ISSUES
    # ==========================================================

    path(
        "issues/",
        FuelIssueListView.as_view(),
        name="fuel-issue-list",
    ),

    path(
        "issues/create/",
        FuelIssueCreateView.as_view(),
        name="fuel-issue-create",
    ),

    path(
        "issues/<int:pk>/",
        FuelIssueDetailView.as_view(),
        name="fuel-issue-detail",
    ),


    # ==========================================================
    # REPORTS
    # ==========================================================

    path(
        "reports/daily/",
        FuelDailySummaryView.as_view(),
        name="fuel-daily-summary",
    ),

    path(
        "reports/monthly/",
        FuelMonthlySummaryView.as_view(),
        name="fuel-monthly-summary",
    ),

    path(
        "reports/reconciliation/",
        FuelReconciliationView.as_view(),
        name="fuel-reconciliation",
    ),


    # ==========================================================
    # FUEL EFFICIENCY
    # ==========================================================

    path(
        "efficiency/vehicle/<int:vehicle_id>/",
        VehicleFuelEfficiencyView.as_view(),
        name="vehicle-fuel-efficiency",
    ),

    path(
        "efficiency/fleet/",
        FleetFuelEfficiencyView.as_view(),
        name="fleet-fuel-efficiency",
    ),
]
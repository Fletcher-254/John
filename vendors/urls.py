from django.urls import path

from .views import (
    VendorListView,
    VendorCreateView,
    VendorDetailView,
    VendorUpdateView,
    VendorDeleteView,

    VendorTransactionListView,
    VendorTransactionCreateView,
    VendorTransactionDetailView,
    VendorTransactionUpdateView,
    VendorTransactionDeleteView,
)

urlpatterns = [

    # ==========================================
    # VENDORS
    # ==========================================

    path(
        "",
        VendorListView.as_view(),
        name="vendor-list"
    ),

    path(
        "create/",
        VendorCreateView.as_view(),
        name="vendor-create"
    ),

    path(
        "<int:pk>/",
        VendorDetailView.as_view(),
        name="vendor-detail"
    ),

    path(
        "<int:pk>/update/",
        VendorUpdateView.as_view(),
        name="vendor-update"
    ),

    path(
        "<int:pk>/delete/",
        VendorDeleteView.as_view(),
        name="vendor-delete"
    ),

    # ==========================================
    # VENDOR TRANSACTIONS
    # ==========================================

    path(
        "transactions/",
        VendorTransactionListView.as_view(),
        name="transaction-list"
    ),

    path(
        "transactions/create/",
        VendorTransactionCreateView.as_view(),
        name="transaction-create"
    ),

    path(
        "transactions/<int:pk>/",
        VendorTransactionDetailView.as_view(),
        name="transaction-detail"
    ),

    path(
        "transactions/<int:pk>/update/",
        VendorTransactionUpdateView.as_view(),
        name="transaction-update"
    ),

    path(
        "transactions/<int:pk>/delete/",
        VendorTransactionDeleteView.as_view(),
        name="transaction-delete"
    ),
]
from django.urls import path

from .views import (
    VehicleListView,
    VehicleCreateView,
    VehicleDetailView,
    VehicleUpdateView,
    VehicleDeleteView,
)

urlpatterns = [
    path("", VehicleListView.as_view(), name="vehicle-list"),
    path("create/", VehicleCreateView.as_view(), name="vehicle-create"),
    path("<int:pk>/", VehicleDetailView.as_view(), name="vehicle-detail"),
    path("<int:pk>/update/", VehicleUpdateView.as_view(), name="vehicle-update"),
    path("<int:pk>/delete/", VehicleDeleteView.as_view(), name="vehicle-delete"),
]
from django.urls import path

from .views import (
    CreateEmployeeView,
    ListEmployeesView,
    RetrieveEmployeeView,
    UpdateEmployeeView,
    SetDailyWageView,
    SetMonthlySalaryView,
    DeleteEmployeeView,
)

urlpatterns = [
    # Create employee (Admin)
    path(
        "employees/",
        CreateEmployeeView.as_view(),
        name="create-employee"
    ),

    # List all active employees
    path(
        "employees/list/",
        ListEmployeesView.as_view(),
        name="list-employees"
    ),

    # Retrieve one employee
    path(
        "employees/<int:pk>/",
        RetrieveEmployeeView.as_view(),
        name="retrieve-employee"
    ),

    # Update employee personal details (Admin)
    path(
        "employees/<int:pk>/update/",
        UpdateEmployeeView.as_view(),
        name="update-employee"
    ),

    # Set casual daily wage (Manager)
    path(
        "employees/<int:pk>/daily-wage/",
        SetDailyWageView.as_view(),
        name="set-daily-wage"
    ),

    # Set permanent monthly salary (Director)
    path(
        "employees/<int:pk>/monthly-salary/",
        SetMonthlySalaryView.as_view(),
        name="set-monthly-salary"
    ),

    # Delete employee (Director)
    path(
        "employees/<int:pk>/delete/",
        DeleteEmployeeView.as_view(),
        name="delete-employee"
    ),
]
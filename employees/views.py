from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Employee
from .serializers import (
    EmployeeAdminSerializer,
    EmployeeManagerSerializer,
    EmployeeDirectorSerializer,
)

from users.permissions import (
    IsAdmin,
    IsManager,
    IsDirector,
)


# =====================================================
# HELPER: RETURN THE CORRECT SERIALIZER FOR THE USER
# =====================================================

def get_serializer_for_user(user):
    if user.role == "admin":
        return EmployeeAdminSerializer

    if user.role == "manager":
        return EmployeeManagerSerializer

    if user.role == "director":
        return EmployeeDirectorSerializer

    return EmployeeAdminSerializer


# =====================================================
# CREATE EMPLOYEE
# ADMIN ONLY
# =====================================================

class CreateEmployeeView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request):

        serializer = EmployeeAdminSerializer(data=request.data)

        if serializer.is_valid():
            employee = serializer.save()
            return Response(
                EmployeeAdminSerializer(employee).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =====================================================
# LIST EMPLOYEES
# ADMIN / MANAGER / DIRECTOR
# =====================================================

class ListEmployeesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        serializer_class = get_serializer_for_user(request.user)

        employees = Employee.objects.filter(is_active=True)

        serializer = serializer_class(employees, many=True)

        return Response(serializer.data)


# =====================================================
# RETRIEVE ONE EMPLOYEE
# ADMIN / MANAGER / DIRECTOR
# =====================================================

class RetrieveEmployeeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):

        try:
            employee = Employee.objects.get(pk=pk, is_active=True)

        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer_class = get_serializer_for_user(request.user)

        serializer = serializer_class(employee)

        return Response(serializer.data)


# =====================================================
# UPDATE EMPLOYEE DETAILS
# ADMIN ONLY
# =====================================================

class UpdateEmployeeView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def patch(self, request, pk):

        try:
            employee = Employee.objects.get(pk=pk, is_active=True)

        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmployeeAdminSerializer(
            employee,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


# =====================================================
# SET DAILY WAGE
# MANAGER ONLY
# =====================================================

class SetDailyWageView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def patch(self, request, pk):

        try:
            employee = Employee.objects.get(pk=pk, is_active=True)

        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if employee.employment_type != "casual":
            return Response(
                {"error": "Only casual employees have a daily wage."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EmployeeManagerSerializer(
            employee,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


# =====================================================
# SET MONTHLY SALARY
# DIRECTOR ONLY
# =====================================================

class SetMonthlySalaryView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector]

    def patch(self, request, pk):

        try:
            employee = Employee.objects.get(pk=pk, is_active=True)

        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if employee.employment_type != "permanent":
            return Response(
                {"error": "Only permanent employees have a monthly salary."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EmployeeDirectorSerializer(
            employee,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


# =====================================================
# DELETE EMPLOYEE
# DIRECTOR ONLY
# =====================================================

class DeleteEmployeeView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector]

    def delete(self, request, pk):

        try:
            employee = Employee.objects.get(pk=pk)

        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        employee.delete()

        return Response(
            {"message": "Employee deleted successfully."},
            status=status.HTTP_200_OK
        )
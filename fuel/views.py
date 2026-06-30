from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .models import FuelPurchase, FuelIssue
from vehicles.models import Vehicle
from .serializers import (
    FuelPurchaseSerializer,
    FuelIssueSerializer,
)


# ============================================================
# FUEL PURCHASE LIST
# ============================================================

class FuelPurchaseListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        purchases = FuelPurchase.objects.all().order_by(
            "-fuel_date",
            "-created_at"
        )

        serializer = FuelPurchaseSerializer(
            purchases,
            many=True
        )

        return Response(serializer.data)


# ============================================================
# CREATE FUEL PURCHASE
# ============================================================

class FuelPurchaseCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        if request.user.role != "admin":
            return Response(
                {"error": "Only the admin can record fuel purchases."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = FuelPurchaseSerializer(
            data=request.data
        )

        if serializer.is_valid():

            purchase = serializer.save()

            return Response(
                FuelPurchaseSerializer(purchase).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ============================================================
# FUEL PURCHASE DETAIL
# ============================================================

class FuelPurchaseDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):

        purchase = get_object_or_404(
            FuelPurchase,
            pk=pk
        )

        serializer = FuelPurchaseSerializer(
            purchase
        )

        return Response(serializer.data)
    
    # ============================================================
# FUEL ISSUE LIST
# ============================================================

class FuelIssueListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        issues = (
            FuelIssue.objects
            .select_related("vehicle")
            .order_by("-fuel_date", "-created_at")
        )

        serializer = FuelIssueSerializer(
            issues,
            many=True
        )

        return Response(serializer.data)


# ============================================================
# CREATE FUEL ISSUE
# ============================================================

class FuelIssueCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        if request.user.role != "admin":
            return Response(
                {"error": "Only the admin can record fuel issues."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = FuelIssueSerializer(
            data=request.data
        )

        if serializer.is_valid():

            issue = serializer.save()

            return Response(
                FuelIssueSerializer(issue).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ============================================================
# FUEL ISSUE DETAIL
# ============================================================

class FuelIssueDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):

        issue = get_object_or_404(
            FuelIssue,
            pk=pk
        )

        serializer = FuelIssueSerializer(issue)

        return Response(serializer.data)
    
# ============================================================
# DAILY FUEL SUMMARY
# ============================================================

class FuelDailySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        today = timezone.localdate()

        purchased = (
            FuelPurchase.objects
            .filter(fuel_date=today)
            .aggregate(total=Sum("litres"))
        )["total"] or 0

        purchase_cost = (
            FuelPurchase.objects
            .filter(fuel_date=today)
            .aggregate(total=Sum("cost"))
        )["total"] or 0

        issued = (
            FuelIssue.objects
            .filter(fuel_date=today)
            .aggregate(total=Sum("litres"))
        )["total"] or 0

        return Response({
            "date": today,
            "fuel_purchased_litres": purchased,
            "fuel_issued_litres": issued,
            "fuel_remaining_litres": purchased - issued,
            "fuel_cost": purchase_cost,
        })


# ============================================================
# MONTHLY FUEL SUMMARY
# ============================================================

class FuelMonthlySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        today = timezone.localdate()

        purchased = (
            FuelPurchase.objects
            .filter(
                fuel_date__year=today.year,
                fuel_date__month=today.month
            )
            .aggregate(total=Sum("litres"))
        )["total"] or 0

        purchase_cost = (
            FuelPurchase.objects
            .filter(
                fuel_date__year=today.year,
                fuel_date__month=today.month
            )
            .aggregate(total=Sum("cost"))
        )["total"] or 0

        issued = (
            FuelIssue.objects
            .filter(
                fuel_date__year=today.year,
                fuel_date__month=today.month
            )
            .aggregate(total=Sum("litres"))
        )["total"] or 0

        return Response({
            "year": today.year,
            "month": today.strftime("%B"),
            "fuel_purchased_litres": purchased,
            "fuel_issued_litres": issued,
            "fuel_remaining_litres": purchased - issued,
            "fuel_cost": purchase_cost,
        })


# ============================================================
# FUEL RECONCILIATION
# ============================================================

class FuelReconciliationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        total_purchased = (
            FuelPurchase.objects
            .aggregate(total=Sum("litres"))
        )["total"] or 0

        total_cost = (
            FuelPurchase.objects
            .aggregate(total=Sum("cost"))
        )["total"] or 0

        total_issued = (
            FuelIssue.objects
            .aggregate(total=Sum("litres"))
        )["total"] or 0

        expected_balance = total_purchased - total_issued

        return Response({
            "total_fuel_purchased": total_purchased,
            "total_fuel_issued": total_issued,
            "expected_fuel_balance": expected_balance,
            "total_purchase_cost": total_cost,
        })

# ============================================================
# VEHICLE FUEL EFFICIENCY
# ============================================================

class VehicleFuelEfficiencyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, vehicle_id):

        issues = (
            FuelIssue.objects
            .filter(vehicle_id=vehicle_id)
            .select_related("vehicle")
            .order_by("fuel_date", "created_at")
        )

        if not issues.exists():
            return Response(
                {"error": "No fuel records found for this vehicle."},
                status=status.HTTP_404_NOT_FOUND
            )

        vehicle = issues.first().vehicle

        total_fuel = (
            issues.aggregate(total=Sum("litres"))["total"] or 0
        )

        start_reading = vehicle.opening_odometer_reading

        end_reading = (
            vehicle.closing_odometer_reading
            if vehicle.closing_odometer_reading is not None
            else issues.last().odometer_reading
        )

        distance = end_reading - start_reading

        if total_fuel == 0:
            efficiency = 0
        else:
            efficiency = round(distance / total_fuel, 2)

        return Response({
            "vehicle": vehicle.asset_identifier,
            "operator": vehicle.assigned_operator,
            "opening_odometer": start_reading,
            "closing_odometer": end_reading,
            "distance_travelled": distance,
            "fuel_used_litres": total_fuel,
            "fuel_efficiency": efficiency,
            "unit": "km/L (or units/L for machinery)"
        })


# ============================================================
# FLEET FUEL EFFICIENCY
# ============================================================

class FleetFuelEfficiencyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        vehicles = Vehicle.objects.all()

        results = []

        for vehicle in vehicles:

            issues = (
                FuelIssue.objects
                .filter(vehicle=vehicle)
                .order_by("fuel_date", "created_at")
            )

            if not issues.exists():
                continue

            total_fuel = (
                issues.aggregate(total=Sum("litres"))["total"] or 0
            )

            end_reading = (
                vehicle.closing_odometer_reading
                if vehicle.closing_odometer_reading is not None
                else issues.last().odometer_reading
            )

            distance = (
                end_reading -
                vehicle.opening_odometer_reading
            )

            if total_fuel == 0:
                efficiency = 0
            else:
                efficiency = round(distance / total_fuel, 2)

            results.append({
                "vehicle": vehicle.asset_identifier,
                "operator": vehicle.assigned_operator,
                "distance_travelled": distance,
                "fuel_used_litres": total_fuel,
                "fuel_efficiency": efficiency,
            })

        results.sort(
            key=lambda x: x["fuel_efficiency"],
            reverse=True
        )

        return Response(results)        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Vehicle
from .serializers import VehicleSerializer, VehicleCreateSerializer


# =====================================================
# LIST VEHICLES
# =====================================================

class VehicleListView(APIView):
    def get(self, request):
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)


# =====================================================
# CREATE VEHICLE (ADMIN ONLY)
# =====================================================

class VehicleCreateView(APIView):
    def post(self, request):

        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can create vehicles"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = VehicleCreateSerializer(data=request.data)

        if serializer.is_valid():
            vehicle = serializer.save()
            return Response(
                VehicleSerializer(vehicle).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =====================================================
# VEHICLE DETAIL
# =====================================================

class VehicleDetailView(APIView):
    def get(self, request, pk):

        vehicle = Vehicle.objects.filter(pk=pk).first()

        if not vehicle:
            return Response(
                {"error": "Vehicle not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)


# =====================================================
# UPDATE VEHICLE (ADMIN ONLY)
# =====================================================

class VehicleUpdateView(APIView):
    def patch(self, request, pk):

        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can update vehicles"},
                status=status.HTTP_403_FORBIDDEN
            )

        vehicle = Vehicle.objects.filter(pk=pk).first()

        if not vehicle:
            return Response(
                {"error": "Vehicle not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = VehicleCreateSerializer(
            vehicle,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(VehicleSerializer(vehicle).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =====================================================
# DELETE VEHICLE (ADMIN ONLY)
# =====================================================

class VehicleDeleteView(APIView):
    def delete(self, request, pk):

        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can delete vehicles"},
                status=status.HTTP_403_FORBIDDEN
            )

        vehicle = Vehicle.objects.filter(pk=pk).first()

        if not vehicle:
            return Response(
                {"error": "Vehicle not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        vehicle.delete()

        return Response(
            {"message": "Vehicle deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
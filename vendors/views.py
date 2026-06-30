from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.permissions import (
    IsManager,
    IsManagerOrDirector,
)

from .models import Vendor, VendorTransaction
from .serializers import (
    VendorSerializer,
    VendorCreateUpdateSerializer,
    VendorTransactionSerializer,
    VendorTransactionCreateUpdateSerializer,
)


# =====================================================
# VENDOR VIEWS
# =====================================================

class VendorListView(APIView):
    permission_classes = [IsManagerOrDirector]

    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)


class VendorCreateView(APIView):
    permission_classes = [IsManager]

    def post(self, request):
        serializer = VendorCreateUpdateSerializer(data=request.data)

        if serializer.is_valid():
            vendor = serializer.save()
            return Response(
                VendorSerializer(vendor).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailView(APIView):
    permission_classes = [IsManagerOrDirector]

    def get(self, request, pk):

        try:
            vendor = Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return Response(
                {"error": "Vendor not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = VendorSerializer(vendor)
        return Response(serializer.data)


class VendorUpdateView(APIView):
    permission_classes = [IsManager]

    def patch(self, request, pk):

        try:
            vendor = Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return Response(
                {"error": "Vendor not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = VendorCreateUpdateSerializer(
            vendor,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(VendorSerializer(vendor).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDeleteView(APIView):
    permission_classes = [IsManager]

    def delete(self, request, pk):

        try:
            vendor = Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return Response(
                {"error": "Vendor not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        vendor.delete()

        return Response(
            {"message": "Vendor deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


# =====================================================
# VENDOR TRANSACTION VIEWS
# =====================================================

class VendorTransactionListView(APIView):
    permission_classes = [IsManagerOrDirector]

    def get(self, request):

        transactions = VendorTransaction.objects.select_related(
            "vendor"
        ).all()

        serializer = VendorTransactionSerializer(
            transactions,
            many=True
        )

        return Response(serializer.data)


class VendorTransactionCreateView(APIView):
    permission_classes = [IsManager]

    def post(self, request):

        serializer = VendorTransactionCreateUpdateSerializer(
            data=request.data
        )

        if serializer.is_valid():
            transaction = serializer.save()

            return Response(
                VendorTransactionSerializer(transaction).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class VendorTransactionDetailView(APIView):
    permission_classes = [IsManagerOrDirector]

    def get(self, request, pk):

        try:
            transaction = VendorTransaction.objects.select_related(
                "vendor"
            ).get(pk=pk)

        except VendorTransaction.DoesNotExist:
            return Response(
                {"error": "Transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = VendorTransactionSerializer(transaction)

        return Response(serializer.data)


class VendorTransactionUpdateView(APIView):
    permission_classes = [IsManager]

    def patch(self, request, pk):

        try:
            transaction = VendorTransaction.objects.get(pk=pk)

        except VendorTransaction.DoesNotExist:
            return Response(
                {"error": "Transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = VendorTransactionCreateUpdateSerializer(
            transaction,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                VendorTransactionSerializer(transaction).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class VendorTransactionDeleteView(APIView):
    permission_classes = [IsManager]

    def delete(self, request, pk):

        try:
            transaction = VendorTransaction.objects.get(pk=pk)

        except VendorTransaction.DoesNotExist:
            return Response(
                {"error": "Transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        transaction.delete()

        return Response(
            {"message": "Transaction deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

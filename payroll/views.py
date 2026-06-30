from datetime import date, timedelta

from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from attendance.models import Attendance
from employees.models import Employee

from users.permissions import (
    IsManager,
    IsDirector,
)

from .models import (
    PayrollPeriod,
    CasualPayroll,
    PermanentPayroll,
)

from .serializers import (
    PayrollPeriodSerializer,
    CasualPayrollSerializer,
    PermanentPayrollSerializer,
)


# ==========================================================
# HELPERS
# ==========================================================

def current_week():
    """
    Monday -> Sunday
    """
    today = date.today()

    monday = today - timedelta(days=today.weekday())

    sunday = monday + timedelta(days=6)

    return monday, sunday


def current_month():
    """
    Returns first and last day of current month.
    """

    today = date.today()

    first = today.replace(day=1)

    if first.month == 12:
        last = first.replace(
            year=first.year + 1,
            month=1
        ) - timedelta(days=1)

    else:
        last = first.replace(
            month=first.month + 1
        ) - timedelta(days=1)

    return first, last


def get_or_create_week_period():

    monday, sunday = current_week()

    period, created = PayrollPeriod.objects.get_or_create(
        period_type="weekly",
        start_date=monday,
        end_date=sunday,
        defaults={
            "status": "open"
        }
    )

    return period


def get_or_create_month_period():

    start, end = current_month()

    period, created = PayrollPeriod.objects.get_or_create(
        period_type="monthly",
        start_date=start,
        end_date=end,
        defaults={
            "status": "open"
        }
    )

    return period


def calculate_days_worked(employee, period):

    return Attendance.objects.filter(
        employee=employee,
        is_present=True,
        date__range=(
            period.start_date,
            period.end_date
        )
    ).count()


def update_casual_payroll():

    period = get_or_create_week_period()

    employees = Employee.objects.filter(
        employment_type="casual",
        is_active=True
    )

    for employee in employees:

        payroll, created = CasualPayroll.objects.get_or_create(
            employee=employee,
            payroll_period=period,
            defaults={
                "days_worked": 0,
                "daily_wage": employee.daily_wage,
                "amount_due": 0
            }
        )

        # Never touch paid payrolls.
        if payroll.payment_status == "paid":
            continue

        payroll.days_worked = calculate_days_worked(
            employee,
            period
        )

        payroll.daily_wage = employee.daily_wage

        payroll.amount_due = (
            payroll.days_worked *
            payroll.daily_wage
        )

        payroll.save()


# ==========================================================
# CASUAL PAYROLL LIST
# Manager + Director
# ==========================================================

class CasualPayrollListView(APIView):

    def get_permissions(self):

        if self.request.user.role == "manager":
            return [IsManager()]

        if self.request.user.role == "director":
            return [IsDirector()]

        return super().get_permissions()

    def get(self, request):

        update_casual_payroll()

        period = get_or_create_week_period()

        payroll = CasualPayroll.objects.filter(
            payroll_period=period
        ).order_by(
            "payment_status",
            "employee__full_name"
        )

        serializer = CasualPayrollSerializer(
            payroll,
            many=True
        )

        return Response(serializer.data)
# ==========================================================
# CASUAL PAYROLL DETAIL
# Manager + Director
# ==========================================================

class CasualPayrollDetailView(APIView):

    def get_permissions(self):

        if self.request.user.role == "manager":
            return [IsManager()]

        if self.request.user.role == "director":
            return [IsDirector()]

        return super().get_permissions()

    def get(self, request, pk):

        update_casual_payroll()

        payroll = get_object_or_404(
            CasualPayroll,
            pk=pk
        )

        serializer = CasualPayrollSerializer(payroll)

        return Response(serializer.data)


# ==========================================================
# PAY CASUAL EMPLOYEE
# Manager Only
# ==========================================================

class PayCasualEmployeeView(APIView):

    permission_classes = [IsManager]

    def patch(self, request, pk):

        update_casual_payroll()

        payroll = get_object_or_404(
            CasualPayroll,
            pk=pk
        )

        if payroll.payment_status == "paid":
            return Response(
                {
                    "error": "This payroll has already been paid."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        payroll.payment_status = "paid"
        payroll.paid_at = timezone.now()

        # Placeholder until M-Pesa integration is added.
        payroll.mpesa_reference = request.data.get(
            "mpesa_reference",
            payroll.mpesa_reference
        )

        payroll.save()

        serializer = CasualPayrollSerializer(payroll)

        return Response(serializer.data)


# ==========================================================
# WEEKLY PAYROLL SUMMARY
# Manager + Director
# ==========================================================

class WeeklyPayrollSummaryView(APIView):

    def get_permissions(self):

        if self.request.user.role == "manager":
            return [IsManager()]

        if self.request.user.role == "director":
            return [IsDirector()]

        return super().get_permissions()

    def get(self, request):

        update_casual_payroll()

        period = get_or_create_week_period()

        payrolls = CasualPayroll.objects.filter(
            payroll_period=period
        )

        total_employees = payrolls.count()

        paid_count = payrolls.filter(
            payment_status="paid"
        ).count()

        pending_count = payrolls.filter(
            payment_status="pending"
        ).count()

        processing_count = payrolls.filter(
            payment_status="processing"
        ).count()

        failed_count = payrolls.filter(
            payment_status="failed"
        ).count()

        total_due = sum(
            payroll.amount_due
            for payroll in payrolls
        )

        total_paid = sum(
            payroll.amount_due
            for payroll in payrolls
            if payroll.payment_status == "paid"
        )

        total_pending = sum(
            payroll.amount_due
            for payroll in payrolls
            if payroll.payment_status != "paid"
        )

        return Response({
            "payroll_period": PayrollPeriodSerializer(period).data,
            "total_employees": total_employees,
            "paid_employees": paid_count,
            "pending_employees": pending_count,
            "processing_employees": processing_count,
            "failed_employees": failed_count,
            "total_amount_due": total_due,
            "total_amount_paid": total_paid,
            "total_amount_pending": total_pending,
        })
    
# ==========================================================
# PERMANENT PAYROLL LIST
# Director Only
# ==========================================================

class PermanentPayrollListView(APIView):

    permission_classes = [IsDirector]

    def get(self, request):

        period = get_or_create_month_period()

        payrolls = PermanentPayroll.objects.filter(
            payroll_period=period
        ).order_by(
            "employee__full_name"
        )

        serializer = PermanentPayrollSerializer(
            payrolls,
            many=True
        )

        return Response(serializer.data)


# ==========================================================
# PERMANENT PAYROLL DETAIL
# Director Only
# ==========================================================

class PermanentPayrollDetailView(APIView):

    permission_classes = [IsDirector]

    def get(self, request, pk):

        payroll = get_object_or_404(
            PermanentPayroll,
            pk=pk
        )

        serializer = PermanentPayrollSerializer(payroll)

        return Response(serializer.data)


# ==========================================================
# CREATE / UPDATE PERMANENT PAYROLL
# Director Only
# ==========================================================

class SavePermanentPayrollView(APIView):

    permission_classes = [IsDirector]

    def patch(self, request, pk):

        payroll = get_object_or_404(
            PermanentPayroll,
            pk=pk
        )

        if payroll.payment_status == "paid":
            return Response(
                {
                    "error": "Paid payroll cannot be modified."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PermanentPayrollSerializer(
            payroll,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            payroll = serializer.save()

            payroll.gross_pay = (
                payroll.monthly_salary +
                payroll.allowances +
                payroll.overtime +
                payroll.bonuses
            )

            payroll.total_deductions = (
                payroll.paye +
                payroll.sha +
                payroll.nssf +
                payroll.other_deductions
            )

            payroll.net_pay = (
                payroll.gross_pay -
                payroll.total_deductions
            )

            payroll.save()

            return Response(
                PermanentPayrollSerializer(payroll).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================================================
# PAY PERMANENT EMPLOYEE
# Director Only
# ==========================================================

class PayPermanentEmployeeView(APIView):

    permission_classes = [IsDirector]

    def patch(self, request, pk):

        payroll = get_object_or_404(
            PermanentPayroll,
            pk=pk
        )

        if payroll.payment_status == "paid":
            return Response(
                {
                    "error": "Employee has already been paid."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        payroll.payment_status = "paid"

        payroll.mpesa_reference = request.data.get(
            "mpesa_reference",
            payroll.mpesa_reference
        )

        payroll.paid_at = timezone.now()

        payroll.save()

        return Response(
            PermanentPayrollSerializer(payroll).data
        )

# ==========================================================
# MONTHLY PAYROLL SUMMARY
# DIRECTOR ONLY
# ==========================================================

class MonthlyPayrollSummaryView(APIView):

    permission_classes = [IsDirector]

    def get(self, request):

        period = get_or_create_month_period()

        payrolls = PermanentPayroll.objects.filter(
            payroll_period=period
        )

        total_employees = payrolls.count()

        paid_count = payrolls.filter(
            payment_status="paid"
        ).count()

        pending_count = payrolls.filter(
            payment_status="pending"
        ).count()

        processing_count = payrolls.filter(
            payment_status="processing"
        ).count()

        failed_count = payrolls.filter(
            payment_status="failed"
        ).count()

        total_gross = sum(
            payroll.gross_pay
            for payroll in payrolls
        )

        total_deductions = sum(
            payroll.total_deductions
            for payroll in payrolls
        )

        total_net = sum(
            payroll.net_pay
            for payroll in payrolls
        )

        total_paid = sum(
            payroll.net_pay
            for payroll in payrolls
            if payroll.payment_status == "paid"
        )

        total_pending = sum(
            payroll.net_pay
            for payroll in payrolls
            if payroll.payment_status != "paid"
        )

        return Response({
            "payroll_period": PayrollPeriodSerializer(period).data,
            "total_employees": total_employees,
            "paid_employees": paid_count,
            "pending_employees": pending_count,
            "processing_employees": processing_count,
            "failed_employees": failed_count,
            "total_gross_pay": total_gross,
            "total_deductions": total_deductions,
            "total_net_pay": total_net,
            "total_paid": total_paid,
            "total_pending": total_pending,
        })


# ==========================================================
# PAYROLL HISTORY
# MANAGER + DIRECTOR
# ==========================================================

class PayrollHistoryView(APIView):

    def get_permissions(self):

        if self.request.user.role == "manager":
            return [IsManager()]

        if self.request.user.role == "director":
            return [IsDirector()]

        return super().get_permissions()

    def get(self, request):

        casual_history = CasualPayroll.objects.filter(
            payment_status="paid"
        ).order_by("-paid_at")

        permanent_history = PermanentPayroll.objects.filter(
            payment_status="paid"
        ).order_by("-paid_at")

        return Response({
            "casual_payroll": CasualPayrollSerializer(
                casual_history,
                many=True
            ).data,
            "permanent_payroll": PermanentPayrollSerializer(
                permanent_history,
                many=True
            ).data,
        })


# ==========================================================
# CLOSE PAYROLL PERIOD
# SYSTEM USE
# ==========================================================

class ClosePayrollPeriodView(APIView):

    permission_classes = [IsDirector]

    def patch(self, request, pk):

        period = get_object_or_404(
            PayrollPeriod,
            pk=pk
        )

        if period.status == "closed":
            return Response(
                {
                    "error": "Payroll period is already closed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        period.status = "closed"
        period.closed_at = timezone.now()
        period.save()

        return Response(
            PayrollPeriodSerializer(period).data
        )
           
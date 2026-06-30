from datetime import date, datetime
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Attendance, SystemAlert
from .serializers import AttendanceSerializer
from employees.models import Employee


# -----------------------------
# HELPER: CUT-OFF CHECK
# -----------------------------
def is_after_cutoff():
    now = timezone.localtime()
    cutoff = now.replace(hour=10, minute=0, second=0, microsecond=0)
    return now >= cutoff


# -----------------------------
# ADMIN: MARK ATTENDANCE
# -----------------------------
class AttendanceMarkView(APIView):
    def post(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Only admin can mark attendance'}, status=403)

        if is_after_cutoff():
            return Response(
                {'error': 'Attendance is locked after 10:00 AM'},
                status=400
            )

        employee_id = request.data.get('employee_id')
        is_present = request.data.get('is_present')
        note = request.data.get('note', '')

        if employee_id is None or is_present is None:
            return Response({'error': 'employee_id and is_present required'}, status=400)

        employee = Employee.objects.filter(id=employee_id).first()
        if not employee:
            return Response({'error': 'Employee not found'}, status=404)

        if employee.employment_type != 'casual':
            return Response({'error': 'Only casual employees are marked here'}, status=400)

        today = date.today()

        # Prevent overwrite (IMMUTABILITY RULE)
        if Attendance.objects.filter(employee=employee, date=today).exists():
            return Response({'error': 'Attendance already recorded and locked'}, status=400)

        attendance = Attendance.objects.create(
            employee=employee,
            date=today,
            is_present=is_present,
            note=note,
            recorded_by=request.user
        )

        return Response(AttendanceSerializer(attendance).data, status=201)


# -----------------------------
# VIEW: TODAY ATTENDANCE
# -----------------------------
class AttendanceTodayView(APIView):
    def get(self, request):
        records = Attendance.objects.filter(date=date.today())
        serializer = AttendanceSerializer(records, many=True)
        return Response(serializer.data)


# -----------------------------
# VIEW: YESTERDAY ATTENDANCE
# -----------------------------
class AttendanceYesterdayView(APIView):
    def get(self, request):
        yesterday = date.today() - timezone.timedelta(days=1)
        records = Attendance.objects.filter(date=yesterday)
        serializer = AttendanceSerializer(records, many=True)
        return Response(serializer.data)


# -----------------------------
# INTERNAL ALERT GENERATION (MANUAL / TASK HOOK)
# -----------------------------
class AttendanceAlertCheckView(APIView):
    """
    This can later be triggered by a scheduler (9:30 / 10:00)
    """
    def post(self, request):
        today = date.today()

        total_casual = Employee.objects.filter(employment_type='casual').count()
        marked = Attendance.objects.filter(date=today).count()

        if marked == 0:
            SystemAlert.objects.create(
                title="Attendance not started",
                message="No attendance has been recorded yet for today.",
                alert_type="reminder",
                date=today
            )
            return Response({'message': 'Reminder alert created'}, status=201)

        if marked < total_casual:
            SystemAlert.objects.create(
                title="Incomplete attendance",
                message=f"{total_casual - marked} employees not marked yet.",
                alert_type="missing_attendance",
                date=today
            )
            return Response({'message': 'Missing attendance alert created'}, status=201)

        return Response({'message': 'Attendance complete'}, status=200)


# -----------------------------
# ALERT LIST (DASHBOARD)
# -----------------------------
class SystemAlertListView(APIView):
    def get(self, request):
        alerts = SystemAlert.objects.all().order_by('-created_at')
        return Response([
            {
                "id": a.id,
                "title": a.title,
                "message": a.message,
                "type": a.alert_type,
                "date": a.date,
                "is_resolved": a.is_resolved
            }
            for a in alerts
        ])

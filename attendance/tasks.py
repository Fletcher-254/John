from celery import shared_task
from django.utils import timezone
from datetime import date

from employees.models import Employee
from .models import Attendance, SystemAlert


@shared_task
def attendance_reminder_task():
    today = date.today()

    if Attendance.objects.filter(date=today).exists():
        return "Attendance already started"

    SystemAlert.objects.create(
        title="Attendance Reminder",
        message="No attendance has been recorded yet for today.",
        alert_type="reminder",
        date=today
    )

    return "Reminder alert created"


@shared_task
def attendance_cutoff_check_task():
    today = date.today()

    total_casual = Employee.objects.filter(employment_type='casual').count()
    marked = Attendance.objects.filter(date=today).count()

    if marked < total_casual:
        SystemAlert.objects.create(
            title="Incomplete Attendance",
            message=f"{total_casual - marked} employees not marked today.",
            alert_type="missing_attendance",
            date=today
        )
        return "Missing attendance alert created"

    return "Attendance complete"
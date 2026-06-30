from django.urls import path
from .views import (
    AttendanceMarkView,
    AttendanceTodayView,
    AttendanceYesterdayView,
    AttendanceAlertCheckView,
    SystemAlertListView
)

urlpatterns = [
    # Mark single attendance (ADMIN ONLY)
    path('mark/', AttendanceMarkView.as_view(), name='attendance-mark'),

    # View today’s attendance (ALL ROLES READ)
    path('today/', AttendanceTodayView.as_view(), name='attendance-today'),

    # View yesterday’s attendance (ALL ROLES READ)
    path('yesterday/', AttendanceYesterdayView.as_view(), name='attendance-yesterday'),

    # Manual trigger for system alert checks (for testing)
    path('alerts/check/', AttendanceAlertCheckView.as_view(), name='attendance-alert-check'),

    # View system alerts (dashboard)
    path('alerts/', SystemAlertListView.as_view(), name='attendance-alerts'),
]
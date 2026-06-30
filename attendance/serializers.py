from rest_framework import serializers
from .models import Attendance, SystemAlert


# -----------------------------
# ATTENDANCE SERIALIZER
# -----------------------------
class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_id_display = serializers.CharField(source='employee.employee_id', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id',
            'employee',
            'employee_name',
            'employee_id_display',
            'date',
            'is_present',
            'note',
            'recorded_by',
            'recorded_at'
        ]
        read_only_fields = ['id', 'recorded_by', 'recorded_at']


# -----------------------------
# SYSTEM ALERT SERIALIZER
# -----------------------------
class SystemAlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemAlert
        fields = [
            'id',
            'title',
            'message',
            'alert_type',
            'date',
            'is_resolved',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
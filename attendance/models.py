from django.db import models
from django.utils import timezone


class Attendance(models.Model):
    # Only casual employees are eligible (enforced at model + view level)
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        limit_choices_to={'employment_type': 'casual'}
    )

    # Daily attendance key
    date = models.DateField(default=timezone.now)

    # Presence flag
    is_present = models.BooleanField()

    # Optional operational notes (lateness, early leave, issues)
    note = models.TextField(blank=True, null=True)

    # Audit trail (who recorded it)
    recorded_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attendance_records'
    )

    recorded_at = models.DateTimeField(auto_now_add=True)

    # Enforce: one record per employee per day
    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date', 'employee']

    def __str__(self):
        return f"{self.employee.name} - {self.date}"
    
    

class SystemAlert(models.Model):
    ALERT_TYPES = (
        ('reminder', 'Reminder'),
        ('warning', 'Warning'),
        ('missing_attendance', 'Missing Attendance'),
        ('cutoff', 'Cutoff Alert'),
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)

    date = models.DateField(default=timezone.now)

    is_resolved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alert_type} - {self.date}"
from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()

class Activity(models.Model):
    # ... choices ...
    ACTIVITY_TYPE_CHOICES = [
        ('PARADE', 'Parade'),
        ('DRILL', 'Drill & Training'),
        ('CAMP', 'Camp'),
        ('SOCIAL', 'Social Service'),
        ('DUTY', 'Special Duty'),
        ('EXAM', 'Exam'),
        ('OTHER', 'Other'),
    ]

    ORGANIZED_BY_CHOICES = [
        ('UNIT', 'Unit'),
        ('GROUP_HQ', 'Group HQ'),
        ('DIRECTORATE', 'Directorate'),
    ]

    activity_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    organized_by = models.CharField(max_length=20, choices=ORGANIZED_BY_CHOICES, blank=True, null=True)
    location = models.CharField(max_length=255)
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Allow blank=True because we will fill it automatically in the save() method
    total_hours = models.DecimalField(
        max_digits=8,  # CHANGED FROM 5 TO 8
        decimal_places=2, 
        help_text="Total hours / periods",
        blank=True,
        null=True
    )
    
    parade_count = models.PositiveIntegerField(default=0)
    
    participants = models.ManyToManyField(User, through='Attendance', related_name='activities')

    def save(self, *args, **kwargs):
        # Calculate difference
        if self.start_date and self.end_date:
            diff = self.end_date - self.start_date
            # Convert total seconds to hours
            hours = diff.total_seconds() / 3600
            self.total_hours = Decimal(hours).quantize(Decimal("0.01"))
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ... Attendance Model stays the same ...
class Attendance(models.Model):
    ATTENDANCE_STATUS = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS)
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'activity')

    def __str__(self):
        return f"{self.user} - {self.activity} - {self.status}"
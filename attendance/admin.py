from django.contrib import admin

from attendance.models import Activity, Attendance

# Register your models here.

admin.site.register(Attendance)
admin.site.register(Activity)
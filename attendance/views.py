import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import User
from attendance.forms import ActivityForm
from attendance.models import Attendance
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q

def upload_attendance(request):
    return render(request, "dashboard/upload_attendance.html")

@login_required
def create_attendance(request):
    cadets = User.objects.all().order_by('username').filter(role="CADET")

    if request.method == 'POST':
        form = ActivityForm(request.POST)
        
        if form.is_valid():
            new_activity = form.save()
            marked_count = 0
            for cadet in cadets:
                status_key = f"status_{cadet.id}"
                status_value = request.POST.get(status_key)

                if status_value:
                    Attendance.objects.create(
                        user=cadet,
                        activity=new_activity,
                        status=status_value
                    )
                    marked_count += 1
            
            messages.success(request, f"Created '{new_activity.name}' and marked attendance for {marked_count} cadets.")
            return redirect('dashboard_upload_attendance')
        else:
            messages.error(request, "Error creating activity. Please check the fields.")
    else:
        form = ActivityForm()

    return render(request, 'dashboard/upload_attendance.html', {
        'form': form,
        'cadets': cadets
    })

@login_required
def view_attendance(request):
    user = request.user
    my_records = Attendance.objects.filter(user=user).select_related('activity').order_by('-activity__start_date')

    total_activities = my_records.count()
    present_count = my_records.filter(status='PRESENT').count()
    
    total_hours = my_records.filter(status='PRESENT').aggregate(
        total=Sum('activity__total_hours')
    )['total'] or 0

    if total_activities > 0:
        attendance_percentage = (present_count / total_activities) * 100
    else:
        attendance_percentage = 0

    context = {
        'my_records': my_records,
        'stats': {
            'total_activities': total_activities,
            'present_count': present_count,
            'absent_count': total_activities - present_count,
            'total_hours': total_hours,
            'percentage': round(attendance_percentage, 1)
        }
    }
    
    return render(request, 'dashboard/my_attendance.html', context)

def attendance_report(request):
    cadets = User.objects.annotate(
        total_events=Count('attendance'),
        present_count=Count('attendance', filter=Q(attendance__status='PRESENT')),
        absent_count=Count('attendance', filter=Q(attendance__status='ABSENT'))
    ).order_by('username').filter(role="CADET")

    for cadet in cadets:
        if cadet.total_events > 0:
            cadet.percentage = round((cadet.present_count / cadet.total_events) * 100, 1)
        else:
            cadet.percentage = 0

    return render(request, 'dashboard/attendance_report.html', {'cadets': cadets})

@login_required
def download_attendance_csv(request):
    cadets = User.objects.annotate(
        total_events=Count('attendance'),
        present_count=Count('attendance', filter=Q(attendance__status='PRESENT')),
        absent_count=Count('attendance', filter=Q(attendance__status='ABSENT'))
    ).filter(role="CADET").order_by('username')

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = 'attachment; filename="attendance_report.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Cadet Name',
        'Total Activities',
        'Present',
        'Absent',
        'Attendance %'
    ])

    for cadet in cadets:

        if cadet.total_events > 0:
            percentage = round((cadet.present_count / cadet.total_events) * 100, 1)
        else:
            percentage = 0

        writer.writerow([
            cadet.username.capitalize(),
            cadet.total_events,
            cadet.present_count,
            cadet.absent_count,
            percentage
        ])

    return response
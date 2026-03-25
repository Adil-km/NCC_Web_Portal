from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import User, UserTag
from attendance.models import Attendance
from .forms import AssignTagsForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from accounts.decorators import faculty_required
import logging
logger = logging.getLogger(__name__)

@faculty_required
def addrole(request):
    selected_user = None

    user_id = request.GET.get('user') or request.POST.get('user')

    if user_id:
        try:
            selected_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            selected_user = None

    if request.method == 'POST':
        form = AssignTagsForm(
            request.POST,
            selected_user=selected_user
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Tags updated successfully!")
            return redirect(f"{request.path}?user={selected_user.id}")

    else:
        form = AssignTagsForm(selected_user=selected_user)

    return render(request, 'dashboard/manage_role.html', {
        'form': form,
        'selected_user': selected_user
    })

def dashboard(request):
    return render(request, 'dashboard/home.html')

@login_required
def profile(request):
    user_tags = UserTag.objects.filter(users__user=request.user)
    return render(request, "dashboard/profile.html", {
        "user_tags": user_tags
    })

# Download or resource section
@login_required
def resources(request):
    return render(request, 'dashboard/resources.html')

@login_required
def upload_resources(request):
    return render(request, "dashboard/upload_resources.html")

@login_required
def profile_view(request):
    profile_user = request.user
    stats = Attendance.objects.filter(user=profile_user).aggregate(
        total_events=Count('id'),
        present_count=Count('id', filter=Q(status='PRESENT')),
        total_hours=Sum('activity__total_hours', filter=Q(status='PRESENT'))
    )
    total_events = stats['total_events'] or 0
    present_count = stats['present_count'] or 0
    total_hours = stats['total_hours'] or 0

    attendance_percentage = 0
    if total_events > 0:
        attendance_percentage = round((present_count / total_events) * 100, 1)

    recent_activity = Attendance.objects.filter(user=profile_user).filter(status="PRESENT")\
        .select_related('activity')\
        .order_by('-activity__start_date')[:5]

    context = {
        'profile_user': profile_user,
        'stats': {
            'total_events': total_events,
            'present_count': present_count,
            'attendance_percentage': attendance_percentage,
            'total_hours': total_hours,
        },
        'recent_activity': recent_activity
    }
    
    return render(request, 'dashboard/profile.html', context)

import json
import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.views.decorators.csrf import ensure_csrf_cookie
from accounts.models import User, UserTag
from accounts.utils import user_has_tag, user_tag_codes
from attendance.forms import ActivityForm
from attendance.models import Activity, Attendance
from gallery.forms import UploadImageForm
from gallery.models import Gallery
from events.forms import NewsEventForm
from events.models import NewsEvent
from .forms import AssignGroupForm, AssignTagsForm, CreateGroupWithPermissionsForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from accounts.decorators import (
    admin_required, 
    cadet_required, 
    faculty_required,
    higher_faculty_required,
    group_required,
    role_required
)
import logging
logger = logging.getLogger(__name__)


@faculty_required
def addtag(request):
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

    return render(request, 'dashboard/addtag.html', {
        'form': form,
        'selected_user': selected_user
    })

def dashboard(request):
    return render(request, 'dashboard/home.html')

@login_required(login_url='login')
def profile(request):
    user_tags = UserTag.objects.filter(users__user=request.user)
    return render(request, "dashboard/profile.html", {
        "user_tags": user_tags
    })

# @faculty_required
def faculty(request):
    return render(request, 'dashboard/faculty.html')

# @cadet_required
def cadet(request):
    return render(request, 'dashboard/cadet.html')

@higher_faculty_required
def assign_group(request):
    if request.method == "POST":
        form = AssignGroupForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            group = form.cleaned_data["group"]
            user.groups.add(group)
            return redirect("assign-group")
    else:
        form = AssignGroupForm()

    return render(request, "dashboard/faculty.html", {"form": form})


@higher_faculty_required
def create_group(request):
    if request.method == "POST":
        form = CreateGroupWithPermissionsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            perms = form.cleaned_data["permissions"]

            group = Group.objects.create(name=name)
            group.permissions.set(perms)
            group.save()

            return redirect("create-group")
    else:
        form = CreateGroupWithPermissionsForm()

    return render(request, "dashboard/create_group.html", {"form": form})

# Gallery Managing

def gallery(request):
    if not user_has_tag(request.user, "gallery_manager"):
        return HttpResponse("You are not allowed")

    images = Gallery.objects.all().order_by("-id")
    return render(request, "dashboard/manage_gallery.html",{'images': images})

def upload_gallery(request):
    if not user_has_tag(request.user, "gallery_manager"):
        return HttpResponse("You are not allowed")
    
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard_gallery')
    else:
        form = UploadImageForm()

    return render(
        request,
        'dashboard/upload_gallery.html',
        {'form': form}
    )

def edit_image(request, pk):
    if not user_has_tag(request.user, "gallery_manager"):
        return HttpResponse("You are not allowed")
    
    image_obj = get_object_or_404(Gallery, pk=pk)
    filename = image_obj.image.name.split('/')[1]
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES, instance=image_obj)
        if form.is_valid():
            form.save()
            logger.info(f"Image updated: {image_obj.image.name}")
            return redirect("dashboard_gallery")
    else:
        form = UploadImageForm(instance=image_obj)

    return render(
        request,
        "dashboard/upload_gallery.html",
        {
            "form": form,
            "edit": True,
            "image_obj": image_obj,
            "filename":filename
        }
    )

def delete_image(request, pk):
    if not user_has_tag(request.user, "gallery_manager"):
        return HttpResponse("You are not allowed")
    
    if request.method == "POST":
        image_obj = get_object_or_404(Gallery, pk=pk)
        logger.info(f"Image deleted: {image_obj.image.name}")
        image_obj.delete()
    return redirect("dashboard_gallery")

# Events

def events(request):
    if not user_has_tag(request.user, "news_editor"):
        return HttpResponse("You are not allowed")

    events = NewsEvent.objects.all().order_by("-date", "-created_at")

    return render(
        request,
        "dashboard/manage_events.html",
        {"events": events}
    )

def upload_event(request):
    if not user_has_tag(request.user, "gallery_manager"):
        return HttpResponse("You are not allowed")

    if request.method == "POST":
        form = NewsEventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("dashboard_events")
    else:
        form = NewsEventForm()

    return render(
        request,
        "dashboard/upload_events.html",
        {"form": form}
    )

def edit_event(request, pk):
    if not user_has_tag(request.user, "gallery_manager"):
        return HttpResponse("You are not allowed")

    news_event = get_object_or_404(NewsEvent, pk=pk)

    if request.method == "POST":
        form = NewsEventForm(
            request.POST,
            request.FILES,
            instance=news_event
        )
        if form.is_valid():
            form.save()
            logger.info(f"Event updated: {news_event.title}")
            return redirect("dashboard_events")
    else:
        form = NewsEventForm(instance=news_event)

    return render(
        request,
        "dashboard/upload_events.html",
        {
            "form": form,
            "edit": True,
            "news_event": news_event,
        }
    )

def delete_event(request, pk):
    if not user_has_tag(request.user, "gallery_manager"):
        return HttpResponse("You are not allowed")

    if request.method == "POST":
        news_event = get_object_or_404(NewsEvent, pk=pk)
        logger.info(f"Event deleted: {news_event.title}")
        news_event.delete()
        return redirect("dashboard_events")

    return HttpResponse("Invalid request method")

# Download or resource section

def resources(request):
    return render(request, 'dashboard/resources.html')


def upload_resources(request):
    return render(request, "dashboard/upload_resources.html")

# Notice

def notice(request):
    return render(request, 'dashboard/notice.html')

# Attendance

def upload_attendance(request):
    return render(request, "dashboard/upload_attendance.html")

def create_attendance(request):
    # Get all cadets (customize filter as needed, e.g., is_staff=False)
    cadets = User.objects.all().order_by('username')

    if request.method == 'POST':
        form = ActivityForm(request.POST)
        
        if form.is_valid():
            # 1. SAVE THE ACTIVITY FIRST
            new_activity = form.save()

            # 2. LOOP THROUGH CADETS AND SAVE ATTENDANCE
            marked_count = 0
            for cadet in cadets:
                # Look for 'status_1', 'status_2' in the POST data
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
            return redirect('dashboard_upload_attendance') # or redirect to dashboard
        else:
            messages.error(request, "Error creating activity. Please check the fields.")
    else:
        form = ActivityForm()

    return render(request, 'dashboard/take_attendance_fresh.html', {
        'form': form,
        'cadets': cadets
    })

@login_required
def view_attendance(request):
    user = request.user
    
    # 1. Get all attendance records for this user
    # 'select_related' optimizes the query by fetching Activity data in the same SQL call
    my_records = Attendance.objects.filter(user=user).select_related('activity').order_by('-activity__start_date')

    # 2. Calculate Statistics
    total_activities = my_records.count()
    present_count = my_records.filter(status='PRESENT').count()
    
    # Calculate Total Hours (sum of hours for activities where user was PRESENT)
    # We use 'activity__total_hours' to access the field in the related Activity model
    total_hours = my_records.filter(status='PRESENT').aggregate(
        total=Sum('activity__total_hours')
    )['total'] or 0

    # Calculate Percentage
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
    # Fetch all users and calculate counts in one efficient query
    cadets = User.objects.annotate(
        total_events=Count('attendance'),
        present_count=Count('attendance', filter=Q(attendance__status='PRESENT')),
        absent_count=Count('attendance', filter=Q(attendance__status='ABSENT'))
    ).order_by('username')

    # Calculate percentage in Python to avoid complex database math
    for cadet in cadets:
        if cadet.total_events > 0:
            cadet.percentage = round((cadet.present_count / cadet.total_events) * 100, 1)
        else:
            cadet.percentage = 0

    return render(request, 'dashboard/attendance_report.html', {'cadets': cadets})

@login_required
def profile_view(request):
    # STRICT: Always use the logged-in user
    profile_user = request.user

    # 1. Calculate Stats
    stats = Attendance.objects.filter(user=profile_user).aggregate(
        total_events=Count('id'),
        present_count=Count('id', filter=Q(status='PRESENT')),
        total_hours=Sum('activity__total_hours', filter=Q(status='PRESENT'))
    )

    # Handle None values (if user has 0 attendance)
    total_events = stats['total_events'] or 0
    present_count = stats['present_count'] or 0
    total_hours = stats['total_hours'] or 0

    attendance_percentage = 0
    if total_events > 0:
        attendance_percentage = round((present_count / total_events) * 100, 1)

    # 2. Get Recent History
    recent_activity = Attendance.objects.filter(user=profile_user)\
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
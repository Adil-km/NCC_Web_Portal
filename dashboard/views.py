from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from accounts.models import User, UserTag
from accounts.utils import user_has_tag
from attendance.models import Attendance
from gallery.forms import UploadImageForm
from gallery.models import Gallery
from events.forms import NewsEventForm
from events.models import NewsEvent
from homepage.forms import UploadHomePageForm, WebsiteSectionForm
from homepage.models import Homepage, WebsiteSection
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

@login_required
def gallery(request):
    if not user_has_tag(request.user, "gallery_manager"):
        return HttpResponse("You are not allowed")

    images = Gallery.objects.all().order_by("-id")
    return render(request, "dashboard/manage_gallery.html",{'images': images})

@login_required
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

@login_required
def edit_gallery(request, pk):
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

@login_required
def delete_gallery(request, pk):
    if not user_has_tag(request.user, "gallery_manager"):
        return HttpResponse("You are not allowed")
    
    if request.method == "POST":
        image_obj = get_object_or_404(Gallery, pk=pk)
        logger.info(f"Image deleted: {image_obj.image.name}")
        image_obj.delete()
    return redirect("dashboard_gallery")

# Events

@login_required
def events(request):
    if not user_has_tag(request.user, "news_editor"):
        return HttpResponse("You are not allowed")

    events = NewsEvent.objects.all().order_by("-date", "-created_at")

    return render(
        request,
        "dashboard/manage_events.html",
        {"events": events}
    )

@login_required
def upload_event(request):
    if not user_has_tag(request.user, "news_editor"):
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

@login_required
def edit_event(request, pk):
    if not user_has_tag(request.user, "news_editor"):
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

@login_required
def delete_event(request, pk):
    if not user_has_tag(request.user, "news_editor"):
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


#  homepage
def homepage(request):
    if not user_has_tag(request.user, "website_manager"):
        return HttpResponse("You are not allowed")

    about_obj = WebsiteSection.objects.filter(section='about').first()

    about_paragraphs = []

    if about_obj and about_obj.description:
        about_paragraphs = [
            item.strip()
            for item in about_obj.description.split("<br>")
            if item.strip()
        ]

    context = {
        'slider_images': Homepage.objects.filter(section='slider'),
        'about_images': Homepage.objects.filter(section='about'),

        # Keep full object (for title etc.)
        'about_section': about_obj,

        # Send split description separately
        'about_paragraphs': about_paragraphs,
    }

    return render(request, 'dashboard/homepage.html', context)

def upload_homepage(request):
    if not user_has_tag(request.user, "website_manager"):
        return HttpResponse("You are not allowed")
    
    if request.method == 'POST':
        form = UploadHomePageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = UploadHomePageForm()

    return render(
        request,
        'dashboard/upload_homepage.html',
        {'form': form}
    )

def delete_homepage_image(request, pk):
    if not user_has_tag(request.user, "website_manager"):
        return HttpResponse("You are not allowed")
    
    if request.method == "POST":
        image_obj = get_object_or_404(Homepage, pk=pk)
        logger.info(f"Image deleted: {image_obj.image.name}")
        image_obj.delete()
    return redirect("homepage")

def upload_desc(request):
    if not user_has_tag(request.user, "website_manager"):
        return HttpResponse("You are not allowed")

    if request.method == "POST":
        section_type = request.POST.get("section")

        # Get existing instance if exists
        instance = WebsiteSection.objects.filter(section=section_type).first()

        # Attach instance to form (important!)
        form = WebsiteSectionForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect("homepage")

    else:
        form = WebsiteSectionForm()

    return render(request, "dashboard/upload_desc.html", {
        "form": form
    })

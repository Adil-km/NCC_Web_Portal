from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group

from accounts.models import User, UserTag
from accounts.utils import user_has_tag
from gallery.forms import UploadImageForm
from gallery.models import Gallery
from .forms import AssignGroupForm, AssignTagsForm, CreateGroupWithPermissionsForm
from django.contrib.auth.decorators import login_required
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

@faculty_required
def faculty(request):
    return render(request, 'dashboard/faculty.html')

@cadet_required
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
    return render(request, "dashboard/edit_gallery.html",{'images': images})

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

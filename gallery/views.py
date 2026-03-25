from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.utils import user_has_tag
from .forms import UploadImageForm
from .models import Gallery
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from accounts.utils import user_has_tag
from gallery.forms import UploadImageForm
from gallery.models import Gallery
from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger(__name__)

def gallery(request):
    images = Gallery.objects.all().filter(visibility="public").order_by("-date")
    return render(request, "gallery/gallery.html",{'images': images})

def boys_gallery(request):
    images = Gallery.objects.all().filter(visibility="public").filter(category='boys')
    return render(request, "gallery/gallery.html",{'images': images})

def girls_gallery(request):
    images = Gallery.objects.all().filter(visibility="public").filter(category='girls')
    return render(request, "gallery/gallery.html",{'images': images})

def naval_gallery(request):
    images = Gallery.objects.all().filter(visibility="public").filter(category='naval')
    return render(request, "gallery/gallery.html",{'images': images})


# Gallery Dashboard
@login_required
def manage_gallery(request):
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
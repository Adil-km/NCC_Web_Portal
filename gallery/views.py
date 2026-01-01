from django.shortcuts import get_object_or_404, redirect, render
from .forms import UploadImageForm
from .models import Gallery
import logging
logger = logging.getLogger(__name__)
# Create your views here.

def gallery(request):
    images = Gallery.objects.all().order_by("-id")
    return render(request, "gallery/gallery.html",{'images': images})

def upload_gallery(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = UploadImageForm()

    return render(
        request,
        'gallery/upload.html',
        {'form': form}
    )

def edit_image(request, pk):
    image_obj = get_object_or_404(Gallery, pk=pk)

    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES, instance=image_obj)
        if form.is_valid():
            form.save()
            logger.info(f"Image updated: {image_obj.image.name}")
            return redirect("gallery")
    else:
        form = UploadImageForm(instance=image_obj)

    return render(
        request,
        "gallery/upload.html",
        {
            "form": form,
            "edit": True,
            "image_obj": image_obj
        }
    )

def delete_image(request, pk):
    if request.method == "POST":
        image_obj = get_object_or_404(Gallery, pk=pk)
        logger.info(f"Image deleted: {image_obj.image.name}")
        image_obj.delete()
    return redirect("gallery")

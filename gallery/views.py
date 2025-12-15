from django.shortcuts import redirect, render
from .forms import UploadImageForm
from .models import Gallery
# Create your views here.

def gallery(request):
    images = Gallery.objects.all()
    return render(request, "gallery/gallery.html",{'images': images})

def upload_gallery(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = UploadImageForm()

    images = Gallery.objects.all()

    return render(
        request,
        'gallery/upload.html',
        {'images': images, 'form': form}
    )
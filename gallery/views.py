from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.utils import user_has_tag
from .forms import UploadImageForm
from .models import Gallery
import logging
logger = logging.getLogger(__name__)
# Create your views here.

def gallery(request):
    images = Gallery.objects.all().order_by("-id")
    return render(request, "gallery/gallery.html",{'images': images})
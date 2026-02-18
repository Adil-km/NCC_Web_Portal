from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.utils import user_has_tag
from .forms import UploadImageForm
from .models import Gallery
import logging
logger = logging.getLogger(__name__)
# Create your views here.

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
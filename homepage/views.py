from django.shortcuts import render
from .models import Homepage, WebsiteSection
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from accounts.utils import user_has_tag
from homepage.forms import UploadHomePageForm, WebsiteSectionForm
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)

# Create your views here.

def home(request):
    slider = Homepage.objects.all().filter(section="slider")
    about = Homepage.objects.filter(section="about").first()
    about_obj = WebsiteSection.objects.filter(section='about').first()

    about_paragraphs = []
    if about_obj and about_obj.description:
        about_paragraphs = [
            item.strip()
            for item in about_obj.description.split("<br>")
            if item.strip()
        ]
    
    context = {
        'about' : about,
        'about_section': about_obj,
        'about_paragraphs': about_paragraphs,
        'slider': slider,

    }

    return render(request, "homepage/home.html", context)

def about(request):
    about_obj = WebsiteSection.objects.filter(section='about').first()
    about_paragraphs = []
    if about_obj and about_obj.description:
        about_paragraphs = [
            item.strip()
            for item in about_obj.description.split("<br>")
            if item.strip()
        ]
    
    context = {
        'about' : Homepage.objects.filter(section="about").first(),
        'about_section': about_obj,
        'about_paragraphs': about_paragraphs,
    }

    return render(request, "homepage/about.html", context)

def achievements(request):
    return render(request, "achievements.html")

def event(request):
    return render(request, "event.html")

def gallery(request):
    return render(request, "gallery.html")

def callToAction(request):
    return render(request, "callToAction.html")

def wings(request):
    return render(request, "homepage/wings.html")

def contact(request):
    return render(request, "homepage/contact.html")

def events(request):
    return render(request, "homepage/events.html")


#  Homepage dashboard
@login_required
def manage_homepage(request):
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
        'about_section': about_obj,
        'about_paragraphs': about_paragraphs,
    }

    return render(request, 'dashboard/homepage.html', context)

@login_required
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

@login_required
def delete_homepage_image(request, pk):
    if not user_has_tag(request.user, "website_manager"):
        return HttpResponse("You are not allowed")
    
    if request.method == "POST":
        image_obj = get_object_or_404(Homepage, pk=pk)
        logger.info(f"Image deleted: {image_obj.image.name}")
        image_obj.delete()
    return redirect("homepage")

@login_required
def upload_desc(request):
    if not user_has_tag(request.user, "website_manager"):
        return HttpResponse("You are not allowed")

    if request.method == "POST":
        section_type = request.POST.get("section")
        instance = WebsiteSection.objects.filter(section=section_type).first()
        form = WebsiteSectionForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect("homepage")
    else:
        form = WebsiteSectionForm()

    return render(request, "dashboard/upload_desc.html", {
        "form": form
    })
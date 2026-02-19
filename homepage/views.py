from unicodedata import category
from django.shortcuts import render
from .models import Homepage, WebsiteSection
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

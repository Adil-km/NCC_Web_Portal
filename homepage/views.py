from unicodedata import category
from django.shortcuts import render
from .models import Homepage
# Create your views here.

def home(request):
    slider = Homepage.objects.all().filter(section="slider")
    about = Homepage.objects.get(section="about")
    return render(request, "homepage/home.html", {"slider":slider, "about":about})

def about(request):
    about = Homepage.objects.get(section="about")
    return render(request, "homepage/about.html", {"about":about})

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

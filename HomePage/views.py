from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def achievements(request):
    return render(request, "achievements.html")

def event(request):
    return render(request, "event.html")

def gallery(request):
    return render(request, "gallery.html")

def callToAction(request):
    return render(request, "callToAction.html")

def contact(request):
    return render(request, "contact.html")



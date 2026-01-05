from django.shortcuts import render

from gallery.models import Gallery

# Create your views here.


def events(request):
    images = Gallery.objects.all().order_by("-id")
    return render(request, "events/events.html",{'images': images})

def event_detail(request):
    return render(request, 'events/event_detail.html')
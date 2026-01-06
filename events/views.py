from django.shortcuts import get_object_or_404, render

from gallery.models import Gallery

# Create your views here.


def events(request):
    images = Gallery.objects.all().order_by("-id")
    return render(request, "events/events.html",{'images': images})

def event_detail(request,pk):
    news = get_object_or_404(Gallery, pk=pk)
    return render(request, 'events/event_detail.html', {"news":news})
from unicodedata import category
from django.shortcuts import get_object_or_404, render

from events.models import NewsEvent

# Create your views here.


def events(request):
    events = NewsEvent.objects.all().filter(visibility="public").order_by("-date", "-created_at")
    return render(request, "events/events.html",{'events': events})

def news_events(request):
    events = NewsEvent.objects.all().filter(visibility="public").filter(category="news").order_by("-date", "-created_at")
    return render(request, "events/events.html",{'events': events})

def event_events(request):
    events = NewsEvent.objects.all().filter(visibility="public").filter(category="events").order_by("-date", "-created_at")
    return render(request, "events/events.html",{'events': events})

def achievement_events(request):
    events = NewsEvent.objects.all().filter(visibility="public").filter(category="achievement").order_by("-date", "-created_at")
    return render(request, "events/events.html",{'events': events})

def event_detail(request, pk):
    event = get_object_or_404(NewsEvent, pk=pk)

    content_list = [
        item.strip()
        for item in event.content.split("<br>")
        if item.strip()
    ]

    return render(request, 'events/event_detail.html', {
        "event": event,
        "content_list": content_list
    })

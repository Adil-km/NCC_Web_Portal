from django.shortcuts import get_object_or_404, render

from events.models import NewsEvent

# Create your views here.


def events(request):
    events = NewsEvent.objects.all().order_by("-date", "-created_at")
    return render(request, "events/events.html",{'events': events})

def event_detail(request,pk):
    event = get_object_or_404(NewsEvent, pk=pk)
    return render(request, 'events/event_detail.html', {"event":event})
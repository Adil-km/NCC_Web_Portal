from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from accounts.utils import user_has_tag
from events.forms import NewsEventForm
from events.models import NewsEvent
from django.contrib.auth.decorators import login_required
from events.models import NewsEvent

import logging
logger = logging.getLogger(__name__)

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


# Events dashboard
@login_required
def manage_events(request):
    if not user_has_tag(request.user, "news_editor"):
        return HttpResponse("You are not allowed")

    events = NewsEvent.objects.all().order_by("-date", "-created_at")

    return render(
        request,
        "dashboard/manage_events.html",
        {"events": events}
    )

@login_required
def upload_event(request):
    if not user_has_tag(request.user, "news_editor"):
        return HttpResponse("You are not allowed")

    if request.method == "POST":
        form = NewsEventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("dashboard_events")
    else:
        form = NewsEventForm()

    return render(
        request,
        "dashboard/upload_events.html",
        {"form": form}
    )

@login_required
def edit_event(request, pk):
    if not user_has_tag(request.user, "news_editor"):
        return HttpResponse("You are not allowed")

    news_event = get_object_or_404(NewsEvent, pk=pk)

    if request.method == "POST":
        form = NewsEventForm(
            request.POST,
            request.FILES,
            instance=news_event
        )
        if form.is_valid():
            form.save()
            logger.info(f"Event updated: {news_event.title}")
            return redirect("dashboard_events")
    else:
        form = NewsEventForm(instance=news_event)

    return render(
        request,
        "dashboard/upload_events.html",
        {
            "form": form,
            "edit": True,
            "news_event": news_event,
        }
    )

@login_required
def delete_event(request, pk):
    if not user_has_tag(request.user, "news_editor"):
        return HttpResponse("You are not allowed")

    if request.method == "POST":
        news_event = get_object_or_404(NewsEvent, pk=pk)
        logger.info(f"Event deleted: {news_event.title}")
        news_event.delete()
        return redirect("dashboard_events")

    return HttpResponse("Invalid request method")

from django.urls import path

from . import views

urlpatterns = [
    path('', views.events, name="events" ),
    path('news/', views.news_events, name="news_events" ),
    path('events/', views.event_events, name="event_events" ),
    path('achievement/', views.achievement_events, name="achievement_events" ),
    path('event_detail/<int:pk>/', views.event_detail, name="event_detail" ),
]

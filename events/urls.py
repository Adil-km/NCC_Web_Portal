from django.urls import path

from . import views

urlpatterns = [
    path('', views.events, name="events" ),
    path('event_detail/<int:pk>/', views.event_detail, name="event_detail" ),
]

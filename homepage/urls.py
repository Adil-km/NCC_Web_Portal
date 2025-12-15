
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home" ),
    path('about/', views.about, name="about" ),
    path('join/', views.callToAction, name="join" ),
    path('achievements/', views.achievements, name="achievements" ),
    path('contact/', views.contact, name="contact" ),
    path('event/', views.event, name="event" ),
]

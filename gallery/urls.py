from django.urls import path

from . import views

urlpatterns = [
    path('', views.gallery, name="gallery" ),
    path('boys/', views.boys_gallery, name="boys_gallery" ),
    path('girls/', views.girls_gallery, name="girls_gallery" ),
    path('naval/', views.naval_gallery, name="naval_gallery" ),
]

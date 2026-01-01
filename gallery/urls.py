from django.urls import path

from . import views

urlpatterns = [
    path('', views.gallery, name="gallery" ),
    path('upload/', views.upload_gallery, name="upload_gallery" ),
    path("edit/<int:pk>/", views.edit_image, name="edit_image"),
    path("delete/<int:pk>/", views.delete_image, name="delete_image"),
]

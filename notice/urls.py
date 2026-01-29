from django.urls import path

from . import views

urlpatterns = [
    path('', views.notice, name="dashboard_notice" ),
    path('upload/', views.upload_notice, name="dashboard_upload_notice" ),
]

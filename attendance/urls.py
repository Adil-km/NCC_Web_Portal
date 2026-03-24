from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view_attendance, name='dashboard_view_attendance'),
    path('upload/', views.create_attendance, name='dashboard_upload_attendance'),
    path('report/', views.attendance_report, name='attendance_report'),
    path('report/download', views.download_attendance_csv, name='download_attendance_csv'),
]
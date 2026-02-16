
from django.urls import include, path

from . import views

urlpatterns = [
    # path('', views.dashboard, name="dashboard" ),
    path('assign-role/', views.assign_group, name="assign-role" ),
    path('create-group/', views.create_group, name="create-group" ),
    path('cadet/', views.cadet, name="cadet" ),
    path('faculty/', views.faculty, name="faculty" ),
    # path('profile/', views.profile, name="profile" ),
    path('addtag/', views.addtag, name="addtag" ),
    
    # Gallery Managing
    path('gallery/', views.gallery, name="dashboard_gallery" ),
    path('gallery/upload/', views.upload_gallery, name="upload_gallery" ),
    path("gallery/edit/<int:pk>/", views.edit_image, name="edit_image"),
    path("gallery/delete/<int:pk>/", views.delete_image, name="delete_image"),

    # Homepage
    path('homepage/', views.homepage, name="homepage" ),
    path('homepage/upload/', views.upload_homepage, name="upload_homepage" ),
    
    # News & Events dashboard
    path('events/', views.events, name='dashboard_events'),
    path('events/upload/', views.upload_event, name='dashboard_upload_event'),
    path('events/edit/<int:pk>/', views.edit_event, name='dashboard_edit_event'),
    path('events/delete/<int:pk>/', views.delete_event, name='dashboard_delete_event'),

    path('resources/', views.resources, name='dashboard_resources'),
    path('resources/upload/', views.upload_resources, name='dashboard_upload_resources'),
    
    path('notice/',include("notice.urls") ),

    # path('attendance/upload/', views.upload_attendance, name='dashboard_upload_attendance'),
    path('attendance/upload/', views.create_attendance, name='dashboard_upload_attendance'),
    path('attendance/view/', views.view_attendance, name='dashboard_view_attendance'),
    path('attendance/report/', views.attendance_report, name='attendance_report'),
    
    path('', views.profile_view, name="profile" ),

]

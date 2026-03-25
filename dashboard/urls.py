
from django.urls import include, path

from . import views
from events.views import manage_events, edit_event, upload_event, delete_event
from gallery.views import manage_gallery, upload_gallery, edit_gallery, delete_gallery

urlpatterns = [
    path('', views.profile_view, name="profile" ),

    path('assign-role/', views.assign_group, name="assign-role" ),
    path('create-group/', views.create_group, name="create-group" ),
    path('cadet/', views.cadet, name="cadet" ),
    path('faculty/', views.faculty, name="faculty" ),
    path('addtag/', views.addtag, name="addtag" ),
    
    # Gallery Dashboard
    path('gallery/', manage_gallery, name="dashboard_gallery" ),
    path('gallery/upload/', upload_gallery, name="upload_gallery" ),
    path("gallery/edit/<int:pk>/", edit_gallery, name="edit_gallery"),
    path("gallery/delete/<int:pk>/", delete_gallery, name="delete_gallery"),

    # Homepage
    path('homepage/', views.homepage, name="homepage" ),
    path('homepage/upload/', views.upload_homepage, name="upload_homepage" ),
    path('homepage/upload/desc', views.upload_desc, name="upload_desc" ),
    path("homepage/delete/<int:pk>/", views.delete_homepage_image, name="delete_homepage_image"),
    
    # News & Events dashboard
    path('events/', manage_events, name='dashboard_events'),
    path('events/upload/', upload_event, name='dashboard_upload_event'),
    path('events/edit/<int:pk>/', edit_event, name='dashboard_edit_event'),
    path('events/delete/<int:pk>/', delete_event, name='dashboard_delete_event'),

    path('resources/', views.resources, name='dashboard_resources'),
    path('resources/upload/', views.upload_resources, name='dashboard_upload_resources'),
    
    path('notice/',include("notice.urls") ),
    path("attendance/",include("attendance.urls")),

]

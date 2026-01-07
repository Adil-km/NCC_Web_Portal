
from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard" ),
    path('assign-role/', views.assign_group, name="assign-role" ),
    path('create-group/', views.create_group, name="create-group" ),
    path('cadet/', views.cadet, name="cadet" ),
    path('faculty/', views.faculty, name="faculty" ),
    path('profile/', views.profile, name="profile" ),
    path('addtag/', views.addtag, name="addtag" ),
    
    # Gallery Managing
    path('gallery/', views.gallery, name="dashboard_gallery" ),
    path('gallery/upload/', views.upload_gallery, name="upload_gallery" ),
    path("gallery/edit/<int:pk>/", views.edit_image, name="edit_image"),
    path("gallery/delete/<int:pk>/", views.delete_image, name="delete_image"),

    # News & Events dashboard
    path('events/', views.events, name='dashboard_events'),
    path('events/upload/', views.upload_event, name='dashboard_upload_event'),
    path('events/edit/<int:pk>/', views.edit_event, name='dashboard_edit_event'),
    path('events/delete/<int:pk>/', views.delete_event, name='dashboard_delete_event'),

]

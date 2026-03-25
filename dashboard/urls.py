
from django.urls import include, path

from . import views
from events.views import manage_events, edit_event, upload_event, delete_event, internal_news
from gallery.views import manage_gallery, upload_gallery, edit_gallery, delete_gallery
from homepage.views import manage_homepage, upload_homepage, delete_homepage_image, upload_desc

urlpatterns = [
    path('', views.profile_view, name="profile" ),
    path('addrole/', views.addrole, name="addrole" ),
    
    # Gallery Dashboard
    path('gallery/', manage_gallery, name="dashboard_gallery" ),
    path('gallery/upload/', upload_gallery, name="upload_gallery" ),
    path("gallery/edit/<int:pk>/", edit_gallery, name="edit_gallery"),
    path("gallery/delete/<int:pk>/", delete_gallery, name="delete_gallery"),

    # News & Events Dashboard
    path('internal/', internal_news, name='dashboard_internal_news'),
    path('events/', manage_events, name='dashboard_events'),
    path('events/upload/', upload_event, name='dashboard_upload_event'),
    path('events/edit/<int:pk>/', edit_event, name='dashboard_edit_event'),
    path('events/delete/<int:pk>/', delete_event, name='dashboard_delete_event'),

    # Homepage Dashboard
    path('homepage/', manage_homepage, name="homepage" ),
    path('homepage/upload/', upload_homepage, name="upload_homepage" ),
    path('homepage/upload/desc', upload_desc, name="upload_desc" ),
    path("homepage/delete/<int:pk>/", delete_homepage_image, name="delete_homepage_image"),

    path('notice/',include("notice.urls") ),
    path("attendance/",include("attendance.urls")),

]


from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("homepage.urls")),
    path('account/', include("accounts.urls")),
    path('dashboard/', include("dashboard.urls")),
    path('gallery/', include("gallery.urls")),
    path('events/', include("events.urls")),
    # path('attendance/', include("attendance.urls")),
    # path('notice/', include("notice.urls")),
]
urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
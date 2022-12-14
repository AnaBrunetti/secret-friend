from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),

    # Apps
    path('', include('accounts.urls')),
    path('', include('chat.urls')),
    path('', include('website.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

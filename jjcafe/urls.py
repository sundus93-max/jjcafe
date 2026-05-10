from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
 
    path('admin/',         admin.site.urls),
    path('accounts/',      include('allauth.urls')),
    path('', include('cafe.urls')),
    # frontend routes
    path('', include('cafe.urls')),
    # API routes
    path('api/', include('cafe.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

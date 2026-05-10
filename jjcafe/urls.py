from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cafe import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth
    path('accounts/', include('allauth.urls')),

    # website (welcome + menu + order portal)
    path('', include('cafe.urls')),

    # API
    path('api/branding/', views.api_branding),
    path('api/menu/', views.api_menu),
    path('api/contact/', views.api_contact),
    path('api/story/', views.api_story),
    path('api/login/', views.api_login),
    path('api/promotions/', views.api_promotions),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
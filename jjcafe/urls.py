from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cafe import views

urlpatterns = [
    path('admin/',         admin.site.urls),
    path('accounts/',      include('allauth.urls')),
    path('',               include('cafe.urls')),

    # ── ANDROID API ──────────────────────────────────────────
    path('api/branding/',    views.api_branding,    name='api_branding'),
    path('api/menu/',        views.api_menu,        name='api_menu'),
    path('api/contact/',     views.api_contact,     name='api_contact'),
    path('api/story/',       views.api_story,       name='api_story'),
    path('api/login/',       views.api_login,       name='api_login'),
    path('api/promotions/',  views.api_promotions,  name='api_promotions'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

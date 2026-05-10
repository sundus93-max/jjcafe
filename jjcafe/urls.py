from django.contrib import admin
from django.urls import path, include
from cafe import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cafe.urls")),

    # APIs
    path("api/branding/", views.api_branding),
    path("api/menu/", views.api_menu),
]
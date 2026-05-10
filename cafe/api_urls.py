from django.urls import path
from . import views

urlpatterns = [
    path('branding/', views.api_branding),
    path('menu/', views.api_menu),
    path('contact/', views.api_contact),
    path('story/', views.api_story),
    path('login/', views.api_login),
    path('promotions/', views.api_promotions),
]
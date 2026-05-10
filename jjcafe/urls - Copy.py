from django.urls import path
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('find-us/', views.find_us, name='find_us'),
    path('our-story/', views.our_story, name='our_story'),
    path('cart/', views.cart, name='cart'),
]
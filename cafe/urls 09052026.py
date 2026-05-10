from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('find-us/', views.find_us, name='find_us'),
    path('our-story/', views.our_story, name='our_story'),
    path('cart/', views.cart, name='cart'),
# ⭐ ADD THIS
    path('add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('login/', views.login_view, name='login'),
]
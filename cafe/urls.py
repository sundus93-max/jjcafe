from django.urls import path
from . import views

urlpatterns = [
    # ── Welcome / Website ──
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('find-us/', views.find_us, name='find_us'),
    path('our-story/', views.our_story, name='our_story'),

    # ── Cart system ──
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('add-to-cart/<int:item_id>/', views.add_to_cart),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart),

    # ── Auth ──
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),

    # ── ORDER PORTAL (ADMIN DASHBOARD) ──
    path('orders/', views.orders_portal, name='orders_portal'),
    path('orders/update/<int:order_id>/', views.order_update_status),
]
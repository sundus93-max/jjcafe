from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("menu/", views.menu),
    path("cart/", views.cart),

    path("add/<int:item_id>/", views.add_to_cart),
    path("remove/<int:item_id>/", views.remove_from_cart),

    path("checkout/", views.checkout),

    path("login/", views.login_view),
    path("profile/", views.profile),

    # ORDER PORTAL
    path("orders/", views.orders_portal),
    path("orders/update/<int:order_id>/", views.order_update_status),
]
from django.urls import path
from . import views

urlpatterns = [
    # ── Pages ─────────────────────────────────────────────────
    path('',                                    views.home,                name='home'),
    path('menu/',                               views.menu,                name='menu'),
    path('find-us/',                            views.find_us,             name='find_us'),
    path('our-story/',                          views.our_story,           name='our_story'),
    path('login/',                              views.login_view,          name='login'),
    path('profile/',                            views.profile,             name='profile'),

    # ── Cart & Checkout ───────────────────────────────────────
    path('cart/',                               views.cart,                name='cart'),
    path('checkout/',                           views.checkout,            name='checkout'),
    path('add-to-cart/<int:item_id>/',          views.add_to_cart,         name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/',     views.remove_from_cart,    name='remove_from_cart'),

    # ── Independent Logouts ───────────────────────────────────
    path('website-logout/',                     views.website_logout,      name='website_logout'),
    path('portal-logout/',                      views.portal_logout,       name='portal_logout'),

    # ── Notifications ─────────────────────────────────────────
    path('notifications/',                      views.notifications_api,   name='notifications_api'),

    # ── Order Portal ──────────────────────────────────────────
    path('orders/',                             views.orders_portal,       name='orders_portal'),
    path('orders/update-status/<int:order_id>/', views.order_update_status, name='order_update_status'),

    # ── Reports ───────────────────────────────────────────────
    path('reports/',                            views.finance_report,      name='finance_report'),
    path('reports/export-csv/',                 views.export_orders_csv,   name='export_orders_csv'),
]

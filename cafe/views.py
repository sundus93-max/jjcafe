import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Sum
from django.utils import timezone

from .models import (
    SiteBranding, Category, Item,
    ContactInfo, StorySection,
    Order, OrderItem, CustomerProfile,
    PaymentMethod, Promotion
)

# ───────────────── HOME (WELCOME PORTAL)
def home(request):
    return render(request, 'home.html')


# ───────────────── MENU
def menu(request):
    categories = Category.objects.prefetch_related('items').all()
    uncategorised = Item.objects.filter(category__isnull=True)
    return render(request, 'menu.html', {
        'categories': categories,
        'uncategorised': uncategorised,
    })


# ───────────────── CART
def cart(request):
    cart_data = request.session.get('cart', {})
    items = []
    total = 0

    for item_id, qty in cart_data.items():
        try:
            item = Item.objects.get(id=int(item_id))
            subtotal = item.price * qty
            items.append({
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'qty': qty,
                'total': subtotal
            })
            total += subtotal
        except Item.DoesNotExist:
            continue

    return render(request, 'cart.html', {'items': items, 'total': total})


# ───────────────── ADD TO CART
@login_required(login_url='/login/')
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    qty = 1
    if request.method == "POST":
        qty = int(request.POST.get("quantity", 1))

    cart = request.session.get("cart", {})
    key = str(item_id)
    cart[key] = cart.get(key, 0) + qty

    request.session["cart"] = cart
    return redirect("cart")


# ───────────────── REMOVE
def remove_from_cart(request, item_id):
    cart = request.session.get("cart", {})
    cart.pop(str(item_id), None)
    request.session["cart"] = cart
    return redirect("cart")


# ───────────────── CHECKOUT (simple safe version)
@login_required(login_url='/login/')
def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("cart")

    total = 0
    items = []

    for item_id, qty in cart.items():
        item = Item.objects.get(id=item_id)
        subtotal = item.price * qty
        total += subtotal
        items.append((item, qty, subtotal))

    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            total=total,
            status="pending"
        )

        for item, qty, subtotal in items:
            OrderItem.objects.create(
                order=order,
                item=item,
                name=item.name,
                price=item.price,
                quantity=qty
            )

        request.session["cart"] = {}
        return render(request, "success.html", {"order": order})

    return render(request, "checkout.html", {"items": items, "total": total})


# ───────────────── LOGIN
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"],
            password=request.POST["password"]
        )
        if user:
            login(request, user)
            return redirect("/")
    return render(request, "login.html")


# ───────────────── PROFILE (FIXED - THIS WAS YOUR ERROR)
@login_required
def profile(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user)

    return render(request, "profile.html", {
        "profile": profile,
        "orders": orders
    })


# ───────────────── ORDER PORTAL (ADMIN STAFF)
@staff_member_required
def orders_portal(request):
    orders = Order.objects.all().order_by("-created_at")

    stats = {
        "total": orders.count(),
        "pending": orders.filter(status="pending").count(),
        "completed": orders.filter(status="completed").count(),
    }

    return render(request, "orders_portal.html", {
        "orders": orders,
        "stats": stats
    })


# ───────────────── UPDATE STATUS
@staff_member_required
def order_update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order.status = request.POST.get("status")
        order.save()

    return redirect("orders_portal")


# ───────────────── APIs (FIXED BRANDING)
def api_branding(request):
    b = SiteBranding.objects.first()

    if not b:
        return JsonResponse({
            "app_name": "JJCafe",
            "tagline": "Brew • Bite • Bliss"
        })

    return JsonResponse({
        "app_name": b.app_name,
        "tagline": b.tagline,
        "logo": request.build_absolute_uri(b.website_logo.url) if b.website_logo else None,
    })


def api_menu(request):
    categories = Category.objects.prefetch_related("items").all()

    data = []
    for c in categories:
        data.append({
            "name": c.name,
            "items": [
                {
                    "id": i.id,
                    "name": i.name,
                    "price": str(i.price),
                }
                for i in c.items.all()
            ]
        })

    return JsonResponse({"categories": data})
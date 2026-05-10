import json
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.utils import timezone
from .models import *

# ─────────────────────────────
# 🟢 WELCOME PORTAL
# ─────────────────────────────

def home(request):
    return render(request, 'home.html')

def menu(request):
    categories = Category.objects.prefetch_related('items').all()
    return render(request, 'menu.html', {'categories': categories})

def find_us(request):
    contact = ContactInfo.objects.first()
    return render(request, 'find_us.html', {'contact': contact})

def our_story(request):
    story = StorySection.objects.all()
    return render(request, 'our_story.html', {'story': story})


# ─────────────────────────────
# 🛒 CART SYSTEM (FIXED)
# ─────────────────────────────

def cart(request):
    cart_data = request.session.get('cart', {})
    items = []
    total = 0

    for item_id, qty in cart_data.items():
        try:
            item = Item.objects.get(id=item_id)
            subtotal = item.price * qty
            items.append({
                'item': item,
                'qty': qty,
                'subtotal': subtotal
            })
            total += subtotal
        except:
            continue

    return render(request, 'cart.html', {'items': items, 'total': total})


@login_required
def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})

        if qty <= 0:
            cart.pop(str(item_id), None)
        else:
            cart[str(item_id)] = qty

        request.session['cart'] = cart

    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart.pop(str(item_id), None)
    request.session['cart'] = cart
    return redirect('cart')


# ─────────────────────────────
# 💳 CHECKOUT (SIMPLE FIXED)
# ─────────────────────────────

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    total = 0
    items = []

    for item_id, qty in cart.items():
        item = Item.objects.get(id=item_id)
        subtotal = item.price * qty
        total += subtotal
        items.append((item, qty))

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            total=total,
            status='pending'
        )

        for item, qty in items:
            OrderItem.objects.create(
                order=order,
                item=item,
                name=item.name,
                price=item.price,
                quantity=qty
            )

        request.session['cart'] = {}
        return render(request, 'success.html', {'order': order})

    return render(request, 'checkout.html', {'items': items, 'total': total})


# ─────────────────────────────
# 🔐 LOGIN
# ─────────────────────────────

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')


# ─────────────────────────────
# 🟡 ORDER PORTAL (STAFF)
# ─────────────────────────────

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def orders_portal(request):
    orders = Order.objects.all().order_by('-created_at')

    stats = {
        'total': orders.count(),
        'pending': orders.filter(status='pending').count(),
        'completed': orders.filter(status='completed').count(),
        'revenue': orders.filter(status='completed').aggregate(Sum('total'))['total__sum'] or 0
    }

    return render(request, 'orders_portal.html', {
        'orders': orders,
        'stats': stats
    })


@staff_member_required
def order_update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.status = request.POST['status']
        order.save()
    return redirect('orders_portal')


# ─────────────────────────────
# 🌐 API (keep minimal)
# ─────────────────────────────

def api_menu(request):
    data = []
    for cat in Category.objects.all():
        data.append({
            'name': cat.name,
            'items': [
                {'name': i.name, 'price': str(i.price)}
                for i in cat.items.all()
            ]
        })
    return JsonResponse({'menu': data})


def api_branding(request):
    return JsonResponse({'app': 'JJCafe'})


def api_contact(request):
    c = ContactInfo.objects.first()
    return JsonResponse({'phone': c.phone if c else ''})


def api_story(request):
    return JsonResponse({'story': list(StorySection.objects.values())})


@csrf_exempt
def api_login(request):
    return JsonResponse({'status': 'ok'})


def api_promotions(request):
    return JsonResponse({'promos': []})
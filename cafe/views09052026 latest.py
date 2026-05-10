import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Category, Item, ContactInfo, StorySection


# ─── PAGES ─────────────────────────────────────────────────────────────────────

def home(request):
    return render(request, 'home.html')


def menu(request):
    """Groups items by category. Uncategorised items go in an 'Other' bucket."""
    categories  = Category.objects.prefetch_related('items').all()
    # Items that have no category
    uncategorised = Item.objects.filter(category__isnull=True)
    return render(request, 'menu.html', {
        'categories': categories,
        'uncategorised': uncategorised,
        'active': 'menu',
    })


def find_us(request):
    contact = ContactInfo.objects.first()
    return render(request, 'find_us.html', {'contact': contact, 'active': 'find_us'})


def our_story(request):
    story = StorySection.objects.all()
    return render(request, 'our_story.html', {'story': story, 'active': 'our_story'})


# ─── CART ──────────────────────────────────────────────────────────────────────

def cart(request):
    cart_data = request.session.get('cart', {})
    cart_items = []
    total = 0

    for item_id_str, quantity in cart_data.items():
        try:
            item     = Item.objects.get(id=int(item_id_str))
            subtotal = item.price * quantity
            cart_items.append({'item': item, 'quantity': quantity, 'subtotal': subtotal})
            total   += subtotal
        except Item.DoesNotExist:
            pass

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


def add_to_cart(request, item_id):
    get_object_or_404(Item, id=item_id)   # 404 if item doesn't exist

    cart = request.session.get('cart', {})
    key  = str(item_id)

    cart[key] = cart.get(key, 0) + 1

    # ✅ FIX: explicitly save and mark modified
    request.session['cart']    = cart
    request.session.modified   = True      # ← THIS was the cart bug

    return redirect('menu')


def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    key  = str(item_id)
    if key in cart:
        del cart[key]
    request.session['cart']  = cart
    request.session.modified = True
    return redirect('cart')


# ─── LOGIN ─────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user     = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


# ─── REST API (for Android App) ────────────────────────────────────────────────

def api_menu(request):
    """Returns all categories + their items as JSON."""
    data = []
    for cat in Category.objects.prefetch_related('items').all():
        items = []
        for item in cat.items.all():
            items.append({
                'id':          item.id,
                'name':        item.name,
                'price':       str(item.price),
                'description': item.description,
                'image':       request.build_absolute_uri(item.image.url) if item.image else None,
            })
        data.append({
            'id':    cat.id,
            'name':  cat.name,
            'image': request.build_absolute_uri(cat.image.url) if cat.image else None,
            'items': items,
        })

    # Uncategorised
    uncategorised = Item.objects.filter(category__isnull=True)
    if uncategorised.exists():
        data.append({
            'id': 0, 'name': 'Other', 'image': None,
            'items': [
                {
                    'id':          i.id,
                    'name':        i.name,
                    'price':       str(i.price),
                    'description': i.description,
                    'image':       request.build_absolute_uri(i.image.url) if i.image else None,
                }
                for i in uncategorised
            ]
        })

    return JsonResponse({'categories': data})


@csrf_exempt
@require_POST
def api_login(request):
    """Simple JSON login for Android. Returns {'success': true, 'username': '...'}"""
    try:
        body     = json.loads(request.body)
        username = body.get('username', '')
        password = body.get('password', '')
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    user = authenticate(request, username=username, password=password)
    if user:
        return JsonResponse({'success': True, 'username': user.username, 'email': user.email})
    return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)

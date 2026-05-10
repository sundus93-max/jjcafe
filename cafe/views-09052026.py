from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login

from .models import Item, ContactInfo, StorySection


# ─── PAGES ─────────────────────────────────────────

def home(request):
    return render(request, 'home.html')


def menu(request):
    items = Item.objects.all()
    return render(request, 'menu.html', {'items': items})


def find_us(request):
    contact = ContactInfo.objects.first()
    return render(request, 'find_us.html', {'contact': contact})


def our_story(request):
    story = StorySection.objects.all()
    return render(request, 'our_story.html', {'story': story})


def cart(request):
    cart = request.session.get('cart', {})
    items = Item.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for item in items:
        quantity = cart[str(item.id)]
        subtotal = item.price * quantity

        cart_items.append({
            'item': item,
            'quantity': quantity,
            'subtotal': subtotal
        })

        total += subtotal

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# ─── CART FUNCTION ────────────────────────────────

def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    cart = request.session.get('cart', {})

    item_id_str = str(item_id)

    if item_id_str in cart:
        cart[item_id_str] += 1
    else:
        cart[item_id_str] = 1

    request.session['cart'] = cart

    return redirect('menu')


# ─── LOGIN ─────────────────────────────────────────

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'login.html')
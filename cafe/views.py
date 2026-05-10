import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import models as db_models
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import SiteBranding, Category, Item, ContactInfo, StorySection
from .models import PaymentMethod
from django.shortcuts import render

# ─── PAGES ─────────────────────────────────────────────────────────────

def home(request):
    return render(request, 'home.html')


def menu(request):
    categories    = Category.objects.prefetch_related('items').all()
    uncategorised = Item.objects.filter(category__isnull=True)
    return render(request, 'menu.html', {
        'categories':    categories,
        'uncategorised': uncategorised,
        'active':        'menu',
    })


def find_us(request):
    contact = ContactInfo.objects.first()
    return render(request, 'find_us.html', {'contact': contact, 'active': 'find_us'})


def our_story(request):
    story = StorySection.objects.all()
    return render(request, 'our_story.html', {'story': story, 'active': 'our_story'})


# ─── CART ──────────────────────────────────────────────────────────────

def cart(request):
    cart_data = request.session.get('cart', {})
    items     = []
    total     = 0

    for item_id, qty in cart_data.items():
        try:
            item     = Item.objects.get(id=int(item_id))
            subtotal = item.price * qty
            items.append({
                'id':    item.id,
                'name':  item.name,
                'price': item.price,
                'qty':   qty,
                'total': subtotal,
                'image': item.image.url if item.image else None,
            })
            total += subtotal
        except Item.DoesNotExist:
            continue

    return render(request, 'cart.html', {'items': items, 'total': total})


@login_required(login_url='/login/')
def add_to_cart(request, item_id):
    """Add item to cart — requires login. Accepts quantity via POST."""
    item = get_object_or_404(Item, id=item_id)
    qty  = 1
    if request.method == 'POST':
        try:
            qty = max(1, int(request.POST.get('quantity', 1)))
        except (ValueError, TypeError):
            qty = 1

    cart    = request.session.get('cart', {})
    key     = str(item_id)
    cart[key] = cart.get(key, 0) + qty
    request.session['cart']  = cart
    request.session.modified = True
    return redirect('cart')


@login_required(login_url='/login/')
def update_cart(request, item_id):
    """Update quantity of an item in the cart."""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        key  = str(item_id)
        try:
            qty = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            qty = 1

        if qty <= 0:
            cart.pop(key, None)
        else:
            cart[key] = qty

        request.session['cart']  = cart
        request.session.modified = True
    return redirect('cart')


@login_required(login_url='/login/')
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart.pop(str(item_id), None)
    request.session['cart']  = cart
    request.session.modified = True
    return redirect('cart')


# ─── CHECKOUT / PAYTM ──────────────────────────────────────────────────

@login_required(login_url='/login/')
def checkout(request):
    """Initiate Paytm payment."""
    cart_data = request.session.get('cart', {})
    if not cart_data:
        return redirect('cart')

    # Calculate total
    total = 0
    for item_id, qty in cart_data.items():
        try:
            item   = Item.objects.get(id=int(item_id))
            total += item.price * qty
        except Item.DoesNotExist:
            pass

    import uuid
    order_id = f"JJCAFE_{request.user.id}_{uuid.uuid4().hex[:8].upper()}"

    # ── Paytm credentials from settings ──────────────────────────
    PAYTM_MID      = getattr(settings, 'PAYTM_MID',      'YOUR_MERCHANT_ID')
    PAYTM_KEY      = getattr(settings, 'PAYTM_MERCHANT_KEY', 'YOUR_MERCHANT_KEY')
    PAYTM_WEBSITE  = getattr(settings, 'PAYTM_WEBSITE',  'WEBSTAGING')
    PAYTM_CHANNEL  = getattr(settings, 'PAYTM_CHANNEL_ID', 'WEB')
    PAYTM_INDUSTRY = getattr(settings, 'PAYTM_INDUSTRY_TYPE', 'Retail')
    PAYTM_CALLBACK = request.build_absolute_uri('/paytm/callback/')
    IS_STAGING     = getattr(settings, 'PAYTM_STAGING', True)

    PAYTM_URL = (
        "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction"
        if IS_STAGING else
        "https://securegw.paytm.in/theia/api/v1/initiateTransaction"
    )

    paytm_params = {
        "body": {
            "requestType":   "Payment",
            "mid":            PAYTM_MID,
            "websiteName":    PAYTM_WEBSITE,
            "orderId":        order_id,
            "callbackUrl":    PAYTM_CALLBACK,
            "txnAmount":     {"value": str(round(total, 2)), "currency": "INR"},
            "userInfo":      {"custId": str(request.user.id), "email": request.user.email},
        }
    }

    try:
        import paytmchecksum
        checksum = paytmchecksum.generateSignature(
            json.dumps(paytm_params["body"]), PAYTM_KEY
        )
        paytm_params["head"] = {"signature": checksum}

        import urllib.request
        post_data = json.dumps(paytm_params).encode('utf-8')
        req = urllib.request.Request(
            f"{PAYTM_URL}?mid={PAYTM_MID}&orderId={order_id}",
            data=post_data,
            headers={'Content-Type': 'application/json', 'Content-Length': len(post_data)},
        )
        response    = urllib.request.urlopen(req, timeout=10)
        response_data = json.loads(response.read().decode('utf-8'))
        txn_token   = response_data['body']['txnToken']

        PAYTM_PAY_URL = (
            "https://securegw-stage.paytm.in/theia/api/v1/showPaymentPage"
            if IS_STAGING else
            "https://securegw.paytm.in/theia/api/v1/showPaymentPage"
        )

        # Store order id in session
        request.session['paytm_order_id'] = order_id

        return render(request, 'checkout.html', {
            'mid':       PAYTM_MID,
            'order_id':  order_id,
            'txn_token': txn_token,
            'total':     total,
            'paytm_url': PAYTM_PAY_URL,
        })

    except Exception as e:
        return render(request, 'checkout.html', {
            'error': f"Payment gateway error: {str(e)}. Please configure Paytm credentials in settings.py",
            'total': total,
        })


@csrf_exempt
def paytm_callback(request):
    """Handle Paytm payment response."""
    if request.method == 'POST':
        paytm_response = dict(request.POST)
        paytm_response = {k: v[0] if isinstance(v, list) else v for k, v in paytm_response.items()}

        received_checksum = paytm_response.pop('CHECKSUMHASH', None)
        PAYTM_KEY = getattr(settings, 'PAYTM_MERCHANT_KEY', '')

        try:
            import paytmchecksum
            is_valid = paytmchecksum.verifySignature(paytm_response, PAYTM_KEY, received_checksum)
        except Exception:
            is_valid = False

        if is_valid and paytm_response.get('STATUS') == 'TXN_SUCCESS':
            # Clear the cart on success
            request.session['cart'] = {}
            request.session.modified = True
            return render(request, 'success.html', {
                'order_id':  paytm_response.get('ORDERID'),
                'txn_id':    paytm_response.get('TXNID'),
                'amount':    paytm_response.get('TXNAMOUNT'),
                'status':    'SUCCESS',
            })
        else:
            return render(request, 'success.html', {
                'order_id': paytm_response.get('ORDERID'),
                'status':   'FAILED',
                'message':  paytm_response.get('RESPMSG', 'Payment failed'),
            })

    return redirect('cart')


# Auto-create defaults if table is empty
if not PaymentMethod.objects.exists():
    defaults = [
        ('Credit / Debit Card', 'card',             '💳', 1, True),
        ('Cash on Pickup',      'cash_on_pickup',   '💵', 2, True),
        ('Cash on Delivery',    'cash_on_delivery', '🏠', 3, True),
        ('Apple Pay',           'apple_pay',        '🍎', 4, False),
        ('Google Pay',          'google_pay',       '📱', 5, False),
    ]
    for name, mtype, icon, order, enabled in defaults:
        PaymentMethod.objects.get_or_create(
            method_type=mtype,
            defaults={'name': name, 'icon': icon, 'order': order, 'is_enabled': enabled}
        )

payment_methods = PaymentMethod.objects.filter(is_enabled=True)

# ─── LOGIN ─────────────────────────────────────────────────────────────

def login_view(request):
    next_url = request.GET.get('next', '/')
    if request.method == "POST":
        next_url  = request.POST.get('next', '/')
        username  = request.POST.get('username', '').strip()
        password  = request.POST.get('password', '')
        user      = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(next_url or '/')
        return render(request, 'login.html', {'error': 'Invalid username or password', 'next': next_url})
    return render(request, 'login.html', {'next': next_url})


# ══════════════════════════════════════════════════════════════════════
#  ANDROID API ENDPOINTS
# ══════════════════════════════════════════════════════════════════════

def api_branding(request):
    b = SiteBranding.objects.first()
    if not b:
        return JsonResponse({'app_name':'JJCafe','tagline':'Brew • Bite • Bliss','logo':None,'background':None,'primary_color':'#c8883a','secondary_color':'#2b1a0e'})
    return JsonResponse({'app_name':b.app_name,'tagline':b.tagline,'logo':request.build_absolute_uri(b.logo.url) if b.logo else None,'background':request.build_absolute_uri(b.background.url) if b.background else None,'primary_color':b.primary_color,'secondary_color':b.secondary_color})


def api_menu(request):
    data       = []
    categories = Category.objects.prefetch_related('items').all()
    for cat in categories:
        items = [{'id':i.id,'name':i.name,'price':str(i.price),'description':i.description,'image':request.build_absolute_uri(i.image.url) if i.image else None} for i in cat.items.all()]
        data.append({'id':cat.id,'name':cat.name,'image':request.build_absolute_uri(cat.image.url) if cat.image else None,'items':items})
    uncategorised = Item.objects.filter(category__isnull=True)
    if uncategorised.exists():
        data.append({'id':0,'name':'Other','image':None,'items':[{'id':i.id,'name':i.name,'price':str(i.price),'description':i.description,'image':request.build_absolute_uri(i.image.url) if i.image else None} for i in uncategorised]})
    return JsonResponse({'categories': data})


def api_contact(request):
    c = ContactInfo.objects.first()
    if not c:
        return JsonResponse({'error': 'No contact info'}, status=404)
    return JsonResponse({'address':c.address,'phone':c.phone,'email':c.email,'opening_hours':c.opening_hours,'google_maps_url':c.google_maps_url})


def api_story(request):
    sections = StorySection.objects.all()
    return JsonResponse({'story':[{'order':s.order,'heading':s.heading,'body':s.body,'image_url':s.image_url} for s in sections]})


@csrf_exempt
@require_POST
def api_login(request):
    try:
        body     = json.loads(request.body)
        username = body.get('username', '')
        password = body.get('password', '')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    user = authenticate(request, username=username, password=password)
    if user:
        return JsonResponse({'success': True, 'username': user.username, 'email': user.email})
    return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)


# ─── CHECKOUT + PAYMENT ────────────────────────────────────────────────────

def checkout(request):
    cart_data = request.session.get('cart', {})
    if not cart_data:
        return redirect('cart')

    items = []
    total = 0
    for item_id, qty in cart_data.items():
        try:
            item     = Item.objects.get(id=int(item_id))
            subtotal = item.price * qty
            items.append({'name': item.name, 'qty': qty, 'total': subtotal, 'id': item.id, 'price': item.price, 'obj': item})
            total   += subtotal
        except Item.DoesNotExist:
            continue

    if request.method == 'POST':
        from .models import Order, OrderItem
        name  = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        # Save order to DB
        order = Order.objects.create(
            user   = request.user if request.user.is_authenticated else None,
            name   = name,
            email  = email,
            phone  = phone,
            total  = total,
            status = 'pending',
        )
        for it in items:
            OrderItem.objects.create(
                order    = order,
                item     = it['obj'],
                name     = it['name'],
                price    = it['price'],
                quantity = it['qty'],
            )

        # ── PAYMENT GATEWAY REDIRECT ──────────────────────────────
        # Option A: PayTabs (popular in UAE)
        # Replace with your PayTabs credentials from https://merchant.paytabs.com
        PAYTABS_PROFILE_ID  = 'YOUR_PROFILE_ID'
        PAYTABS_SERVER_KEY  = 'YOUR_SERVER_KEY'

        import urllib.request, urllib.parse
        payload = {
            'profile_id':        PAYTABS_PROFILE_ID,
            'tran_type':         'sale',
            'tran_class':        'ecom',
            'cart_id':           str(order.id),
            'cart_amount':       str(total),
            'cart_currency':     'AED',
            'cart_description':  f'JJCafe Order #{order.id}',
            'customer_details': {
                'name':  name,
                'email': email,
                'phone': phone,
            },
            'callback':          'http://YOUR_DOMAIN/payment/callback/',
            'return':            'http://YOUR_DOMAIN/success/',
        }

        # ── FOR NOW: skip gateway and show success page ───────────
        # When you have PayTabs credentials, uncomment the redirect block above
        request.session['cart'] = {}
        request.session.modified = True
        return render(request, 'success.html', {'name': name, 'order_id': order.id})

    from .models import PaymentMethod
    payment_methods = PaymentMethod.objects.filter(is_enabled=True)
    return render(request, 'checkout.html', {'items': items, 'total': total, 'payment_methods': payment_methods})


# ─── API: PROMOTIONS ───────────────────────────────────────────────────────

def api_promotions(request):
    from .models import Promotion
    from datetime import date
    today = date.today()
    promos = Promotion.objects.filter(is_active=True).filter(
        Q(start_date__isnull=True) | Q(start_date__lte=today)
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=today)
    )
    data = []
    for p in promos:
        data.append({
            'id':         p.id,
            'title':      p.title,
            'type':       p.promo_type,
            'text':       p.text,
            'image':      request.build_absolute_uri(p.image.url) if p.image else None,
            'video_url':  p.video_url,
        })
    return JsonResponse({'promotions': data})


# ─── ORDER MANAGEMENT PORTAL ───────────────────────────────────────────────

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.utils import timezone
import json as _json

@staff_member_required(login_url='/login/')
def orders_portal(request):
    from .models import Order, OrderItem
    orders = Order.objects.prefetch_related('order_items').all()

    today = timezone.now().date()
    stats = {
        'total':     orders.count(),
        'pending':   orders.filter(status='pending').count(),
        'preparing': orders.filter(status='preparing').count(),
        'completed': orders.filter(status='completed').count(),
        'revenue':   orders.filter(created_at__date=today, status__in=['paid','completed']).aggregate(s=Sum('total'))['s'] or 0,
    }

    orders_list = []
    for o in orders:
        orders_list.append({
            'id':             o.id,
            'name':           o.name,
            'email':          o.email,
            'phone':          o.phone,
            'total':          str(o.total),
            'status':         o.status,
            'status_display': o.get_status_display(),
            'payment_method': o.payment_method,
            'notes':          o.notes,
            'created_at':     o.created_at.strftime('%d %b %Y, %H:%M'),
            'items': [
                {
                    'name':     oi.name,
                    'quantity': oi.quantity,
                    'price':    str(oi.price),
                    'subtotal': str(oi.subtotal),
                }
                for oi in o.order_items.all()
            ]
        })

    return render(request, 'orders_portal.html', {
        'orders':      orders,
        'orders_json': _json.dumps(orders_list),
        'stats':       stats,
    })


@staff_member_required(login_url='/login/')
def order_update_status(request, order_id):
    from .models import Order
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.status = request.POST.get('status', order.status)
        order.save()
    return redirect('orders_portal')


# ─── USER PROFILE ──────────────────────────────────────────────────────────

from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def profile(request):
    from .models import CustomerProfile, Order
    profile_obj, _ = CustomerProfile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    success = False

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name  = request.POST.get('last_name', '')
        request.user.email      = request.POST.get('email', request.user.email)
        request.user.save()
        profile_obj.phone   = request.POST.get('phone', '')
        profile_obj.address = request.POST.get('address', '')
        profile_obj.save()
        success = True

    return render(request, 'profile.html', {
        'profile': profile_obj,
        'orders':  orders,
        'success': success,
    })

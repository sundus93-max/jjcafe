from django.shortcuts import render, redirect
from .models import Item, Order, OrderItem

#HOME
	def home(request):
    return render(request, 'home.html')

# MENU

def menu(request):
    items = Item.objects.all()
    return render(request, 'menu.html', {'items': items})

#FIND_US

def find_us(request):
    contact = ContactInfo.objects.first()
    return render(request, 'find_us.html', {'contact': contact})

#OUR_STORY

def our_story(request):
    story = StorySection.objects.all()
    return render(request, 'our_story.html', {'story': story})


# ADD TO CART

def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        cart[str(item_id)] += 1
    else:
        cart[str(item_id)] = 1

    request.session['cart'] = cart
    return redirect('menu')


# CART

def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for item_id, qty in cart.items():
        item = Item.objects.get(id=item_id)
        item.qty = qty
        item.total = item.price * qty
        total += item.total
        items.append(item)

    return render(request, 'cart.html', {'items': items, 'total': total})


# CHECKOUT

def checkout(request):
    cart = request.session.get('cart', {})

    if request.method == "POST":
        payment = request.POST['payment']

        order = Order.objects.create(payment_method=payment)

        total = 0

        for item_id, qty in cart.items():
            item = Item.objects.get(id=item_id)
            OrderItem.objects.create(order=order, item=item, quantity=qty)
            total += item.price * qty

        order.total_amount = total
        order.status = "paid" if payment == "gpay" else "pending"
        order.save()

        request.session['cart'] = {}
        return render(request, 'success.html', {'order': order})

    return render(request, 'checkout.html')
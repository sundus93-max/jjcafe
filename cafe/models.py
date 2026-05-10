from django.db import models
from django.contrib.auth.models import User


# ── SITE BRANDING ──────────────────────────────────────────────────────────────
class SiteBranding(models.Model):
    app_name        = models.CharField(max_length=100, default='JJCafe')
    tagline         = models.CharField(max_length=200, blank=True, default='Brew • Bite • Bliss')
    primary_color   = models.CharField(max_length=7, default='#c8883a', help_text='Hex e.g. #c8883a')
    secondary_color = models.CharField(max_length=7, default='#2b1a0e', help_text='Hex e.g. #2b1a0e')

    # ── WEBSITE branding
    website_logo       = models.ImageField(upload_to='branding/', null=True, blank=True, verbose_name='Website Logo')
    website_background = models.ImageField(upload_to='branding/', null=True, blank=True, verbose_name='Website Background')

    # ── ADMIN PORTAL branding
    admin_logo       = models.ImageField(upload_to='branding/admin/', null=True, blank=True, verbose_name='Admin Portal Logo')
    admin_background = models.ImageField(upload_to='branding/admin/', null=True, blank=True, verbose_name='Admin Portal Background')

    class Meta:
        verbose_name        = 'Site Branding'
        verbose_name_plural = 'Site Branding'

    def __str__(self):
        return 'Branding Settings'


# ── PAYMENT METHOD ─────────────────────────────────────────────────────────────
class PaymentMethod(models.Model):
    TYPE_CHOICES = [
        ('card',             'Credit / Debit Card'),
        ('cash_on_pickup',   'Cash on Pickup'),
        ('cash_on_delivery', 'Cash on Delivery'),
        ('apple_pay',        'Apple Pay'),
        ('google_pay',       'Google Pay'),
    ]
    name       = models.CharField(max_length=100)
    method_type = models.CharField(max_length=30, choices=TYPE_CHOICES, unique=True)
    is_enabled = models.BooleanField(default=True)
    icon       = models.CharField(max_length=10, default='💳', help_text='Emoji icon e.g. 💳 🍎 📱')
    order      = models.PositiveSmallIntegerField(default=0, help_text='Display order')

    class Meta:
        verbose_name        = 'Payment Method'
        verbose_name_plural = 'Payment Methods'
        ordering            = ['order', 'name']

    def __str__(self):
        status = '✅' if self.is_enabled else '⏸'
        return f'{status} {self.name}'


# ── CATEGORY ───────────────────────────────────────────────────────────────────
class Category(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image       = models.ImageField(upload_to='categories/', null=True, blank=True)
    order       = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering            = ['order', 'name']
        verbose_name        = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# ── MENU ITEM ──────────────────────────────────────────────────────────────────
class Item(models.Model):
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    name        = models.CharField(max_length=100)
    price       = models.DecimalField(max_digits=6, decimal_places=2)
    image       = models.ImageField(upload_to='items/', null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name        = 'Menu Item'
        verbose_name_plural = 'Menu Items'
        ordering            = ['name']

    def __str__(self):
        return f'{self.category} → {self.name}' if self.category else self.name


# ── FIND US ────────────────────────────────────────────────────────────────────
class ContactInfo(models.Model):
    address         = models.TextField(help_text='Full street address')
    phone           = models.CharField(max_length=30, blank=True)
    email           = models.EmailField(blank=True)
    opening_hours   = models.TextField(blank=True)
    google_maps_url = models.URLField(max_length=500, blank=True)

    class Meta:
        verbose_name        = 'Find Us'
        verbose_name_plural = 'Find Us'

    def __str__(self):
        return 'Contact & Location'


# ── OUR STORY ──────────────────────────────────────────────────────────────────
class StorySection(models.Model):
    order     = models.PositiveSmallIntegerField(default=1)
    heading   = models.CharField(max_length=200, blank=True)
    body      = models.TextField()
    image_url = models.URLField(blank=True)

    class Meta:
        ordering            = ['order']
        verbose_name        = 'Our Story Section'
        verbose_name_plural = 'Our Story'

    def __str__(self):
        return f'Section {self.order}: {self.heading or self.body[:40]}'


# ── CUSTOMER PROFILE ───────────────────────────────────────────────────────────
class CustomerProfile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone        = models.CharField(max_length=20, blank=True)
    address      = models.TextField(blank=True)
    joined_at    = models.DateTimeField(auto_now_add=True)
    total_orders = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name        = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.user.email or self.user.username


# ── ORDER ──────────────────────────────────────────────────────────────────────
class Order(models.Model):
    STATUS = [
        ('pending',   'Pending'),
        ('paid',      'Paid'),
        ('preparing', 'Preparing'),
        ('ready',     'Ready for Pickup'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user           = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name           = models.CharField(max_length=120, blank=True)
    email          = models.EmailField(blank=True)
    phone          = models.CharField(max_length=20, blank=True)
    total          = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status         = models.CharField(max_length=20, choices=STATUS, default='pending')
    payment_method = models.CharField(max_length=30, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    payment_ref    = models.CharField(max_length=200, blank=True)
    notes          = models.TextField(blank=True, help_text='Special instructions')

    class Meta:
        verbose_name        = 'Order'
        verbose_name_plural = 'Orders'
        ordering            = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} — {self.name or "Guest"} — AED {self.total}'

    def get_status_color(self):
        colors = {
            'pending': '#e67e22', 'paid': '#27ae60',
            'preparing': '#2980b9', 'ready': '#8e44ad',
            'completed': '#95a5a6', 'cancelled': '#e74c3c',
        }
        return colors.get(self.status, '#999')


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item     = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
    name     = models.CharField(max_length=100)
    price    = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity}× {self.name}'

    @property
    def subtotal(self):
        return self.price * self.quantity


# ── PROMOTION ──────────────────────────────────────────────────────────────────
class Promotion(models.Model):
    TYPE_CHOICES = [
        ('text',  'Text Banner'),
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    SHOW_ON_CHOICES = [
        ('both',    'Website & App'),
        ('website', 'Website Only'),
        ('app',     'App Only'),
    ]
    title      = models.CharField(max_length=200)
    promo_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='text')
    show_on    = models.CharField(max_length=10, choices=SHOW_ON_CHOICES, default='both')
    text       = models.TextField(blank=True)
    image      = models.ImageField(upload_to='promotions/', null=True, blank=True)
    video_url  = models.URLField(blank=True)
    is_active  = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
    end_date   = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Promotion'
        verbose_name_plural = 'Promotions'
        ordering            = ['-created_at']

    def __str__(self):
        return f'{"✅" if self.is_active else "⏸"} {self.title}'


# ── ORDER NOTIFICATION ────────────────────────────────────────────────────────
class OrderNotification(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    order      = models.ForeignKey('Order', on_delete=models.CASCADE)
    message    = models.CharField(max_length=255)
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Notification for {self.user.email}: {self.message}'

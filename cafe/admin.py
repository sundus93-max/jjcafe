from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from .models import (
    SiteBranding, Category, Item, ContactInfo, StorySection,
    CustomerProfile, Order, OrderItem, Promotion, PaymentMethod
)

# ── Import proxy models defined in cafe/models.py ────────────────────────────
from .models import StaffUserProxy, CustomerUserProxy

# ── Remove default Users and Groups from admin ────────────────────────────────
admin.site.unregister(User)
admin.site.unregister(Group)


# ══════════════════════════════════════════════════════════════
#  CUSTOM ADMIN SITE HEADER
# ══════════════════════════════════════════════════════════════
admin.site.site_header  = "☕ JJCafe Admin Portal"
admin.site.site_title   = "JJCafe Admin"
admin.site.index_title  = "Welcome to JJCafe Management"


# ══════════════════════════════════════════════════════════════
#  1. SITE BRANDING  (logo + background)
# ══════════════════════════════════════════════════════════════
@admin.register(SiteBranding)
class SiteBrandingAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🏷️ App Identity', {
            'fields': ('app_name', 'tagline'),
        }),
        ('🌐 Website Images', {
            'fields': ('website_logo', 'website_logo_preview', 'website_background', 'website_bg_preview'),
            'description': 'These images show on the public website.',
        }),
        ('⚙️ Admin Portal Images', {
            'fields': ('admin_logo', 'admin_logo_preview', 'admin_background', 'admin_bg_preview'),
            'description': 'These images show inside this admin portal only. Leave blank to use website images.',
        }),
        ('🎨 Colors', {
            'fields': ('primary_color', 'secondary_color'),
            'description': 'Use hex codes e.g. #c8883a',
        }),
    )
    readonly_fields = ('website_logo_preview', 'website_bg_preview', 'admin_logo_preview', 'admin_bg_preview')

    def website_logo_preview(self, obj):
        if obj.website_logo:
            return format_html('<img src="{}" style="width:80px;height:80px;object-fit:cover;border-radius:50%;border:3px solid #c8883a;margin-top:6px">', obj.website_logo.url)
        return format_html('<span style="color:#999">Not set</span>')
    website_logo_preview.short_description = "Preview"

    def website_bg_preview(self, obj):
        if obj.website_background:
            return format_html('<img src="{}" style="width:280px;height:100px;object-fit:cover;border-radius:10px;margin-top:6px">', obj.website_background.url)
        return format_html('<span style="color:#999">Not set</span>')
    website_bg_preview.short_description = "Preview"

    def admin_logo_preview(self, obj):
        if obj.admin_logo:
            return format_html('<img src="{}" style="width:80px;height:80px;object-fit:cover;border-radius:50%;border:3px solid #2980b9;margin-top:6px">', obj.admin_logo.url)
        return format_html('<span style="color:#999">Not set — will use website logo</span>')
    admin_logo_preview.short_description = "Preview"

    def admin_bg_preview(self, obj):
        if obj.admin_background:
            return format_html('<img src="{}" style="width:280px;height:100px;object-fit:cover;border-radius:10px;margin-top:6px">', obj.admin_background.url)
        return format_html('<span style="color:#999">Not set — will use website background</span>')
    admin_bg_preview.short_description = "Preview"

    def has_add_permission(self, request):
        return not SiteBranding.objects.exists()


# ══════════════════════════════════════════════════════════════
#  2. STAFF USERS  (separate from customers)
# ══════════════════════════════════════════════════════════════
@admin.register(StaffUserProxy)
class StaffUserAdmin(BaseUserAdmin):
    list_display  = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter   = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=True)

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        super().save_model(request, obj, form, change)


class CustomerProfileInline(admin.StackedInline):
    model  = CustomerProfile
    extra  = 0
    fields = ('phone', 'address', 'total_orders')

@admin.register(CustomerUserProxy)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display  = ('customer_name', 'email_addr', 'phone_num', 'total_orders_num', 'date_joined')
    search_fields = ('username', 'email', 'customer_profile__phone')
    inlines       = [CustomerProfileInline]
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        ('Account Info', {'fields': ('username', 'email', 'first_name', 'last_name', 'is_active')}),
        ('Dates',        {'fields': ('date_joined', 'last_login')}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=False, is_superuser=False)

    def customer_name(self, obj):
        name = obj.get_full_name()
        return name if name else obj.username
    customer_name.short_description = "Name"

    def email_addr(self, obj):
        return obj.email
    email_addr.short_description = "Email"

    def phone_num(self, obj):
        try:
            profile = CustomerProfile.objects.filter(user=obj).first()
            return profile.phone if profile and profile.phone else '—'
        except Exception:
            return '—'
    phone_num.short_description = "Phone"

    def total_orders_num(self, obj):
        try:
            count = Order.objects.filter(user=obj).count()
            return format_html('<b style="color:#c8883a">{}</b>', count)
        except Exception:
            return '—'
    total_orders_num.short_description = "Orders"


# ══════════════════════════════════════════════════════════════
#  3. CATEGORY + MENU ITEMS
# ══════════════════════════════════════════════════════════════
class ItemInline(admin.TabularInline):
    model           = Item
    extra           = 1
    fields          = ('name', 'price', 'description', 'image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:55px;height:55px;object-fit:cover;border-radius:8px">',
                obj.image.url
            )
        return '—'
    image_preview.short_description = "Preview"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display       = ('order', 'cat_img', 'name', 'item_count')
    list_editable      = ('order',)
    list_display_links = ('name',)
    inlines            = [ItemInline]

    def cat_img(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:44px;height:44px;object-fit:cover;border-radius:50%">', obj.image.url)
        return '—'
    cat_img.short_description = "Photo"

    def item_count(self, obj):
        return format_html('<b style="color:#c8883a">{}</b> items', obj.items.count())
    item_count.short_description = "Items"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display  = ('item_img', 'name', 'category', 'price')
    list_filter   = ('category',)
    search_fields = ('name',)

    def item_img(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:48px;height:48px;object-fit:cover;border-radius:8px">', obj.image.url)
        return '—'
    item_img.short_description = "Photo"


# ══════════════════════════════════════════════════════════════
#  4. ORDERS
# ══════════════════════════════════════════════════════════════
class OrderItemInline(admin.TabularInline):
    model         = OrderItem
    extra         = 0
    readonly_fields = ('name', 'price', 'quantity', 'subtotal')
    fields        = ('name', 'price', 'quantity', 'subtotal')

    def subtotal(self, obj):
        return f"AED {obj.subtotal}"
    subtotal.short_description = "Subtotal"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display       = ('id', 'status_badge', 'customer_info', 'total_display', 'payment_ref', 'created_at')
    list_filter        = ('status', 'created_at')
    search_fields      = ('name', 'email', 'phone', 'payment_ref')
    readonly_fields    = ('created_at', 'total')
    list_display_links = ('id', 'customer_info')
    inlines            = [OrderItemInline]

    fieldsets = (
        ('Customer',    {'fields': ('user', 'name', 'email', 'phone')}),
        ('Order',       {'fields': ('status', 'total', 'payment_ref', 'created_at')}),
    )

    def status_badge(self, obj):
        colors = {
            'pending':   '#e67e22', 'paid':      '#27ae60',
            'preparing': '#2980b9', 'ready':     '#8e44ad',
            'completed': '#95a5a6', 'cancelled': '#e74c3c',
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:bold">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"

    def customer_info(self, obj):
        return obj.name or (obj.user.email if obj.user else 'Guest')
    customer_info.short_description = "Customer"

    def total_display(self, obj):
        return format_html('<b style="color:#c8883a">AED {}</b>', obj.total)
    total_display.short_description = "Total"

    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data and obj.user:
            from .models import OrderNotification
            status_msgs = {
                'paid':      '✅ Your order #{} has been paid and confirmed!',
                'preparing': '👨‍🍳 Your order #{} is now being prepared.',
                'ready':     '🎉 Your order #{} is ready for pickup!',
                'completed': '✅ Your order #{} has been completed. Thank you!',
                'cancelled': '❌ Your order #{} has been cancelled.',
            }
            msg_template = status_msgs.get(obj.status)
            if msg_template:
                OrderNotification.objects.create(
                    user=obj.user,
                    order=obj,
                    message=msg_template.format(obj.id)
                )
        super().save_model(request, obj, form, change)


# ══════════════════════════════════════════════════════════════
#  5. PROMOTIONS
# ══════════════════════════════════════════════════════════════
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display       = ('promo_preview', 'title', 'type_badge', 'is_active', 'date_range', 'created_at')
    list_filter        = ('is_active', 'promo_type')
    search_fields      = ('title', 'text')
    list_display_links = ('title',)
    list_editable      = ('is_active',)

    fieldsets = (
        ('📢 Promotion Details', {
            'fields': ('title', 'promo_type', 'is_active'),
        }),
        ('📝 Content  (fill only what matches your type above)', {
            'fields': ('text', 'image', 'img_preview', 'video_url'),
            'description': (
                'Text Banner → fill <b>Text</b> only | '
                'Image → upload <b>Image</b> only | '
                'Video → paste <b>Video URL</b> only'
            ),
        }),
        ('📅 Schedule  (optional)', {
            'fields': ('start_date', 'end_date'),
            'description': 'Leave blank to always show.',
        }),
    )
    readonly_fields = ('img_preview', 'created_at')

    def img_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:300px;max-height:160px;object-fit:cover;border-radius:10px;margin-top:6px">',
                obj.image.url
            )
        return '—'
    img_preview.short_description = "Image Preview"

    def promo_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:48px;height:48px;object-fit:cover;border-radius:8px">', obj.image.url)
        if obj.promo_type == 'video':
            return format_html('<span style="font-size:20px">🎬</span>')
        return format_html('<span style="font-size:20px">📝</span>')
    promo_preview.short_description = ""

    def type_badge(self, obj):
        colors = {'text': '#3498db', 'image': '#9b59b6', 'video': '#e74c3c'}
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:bold">{}</span>',
            colors.get(obj.promo_type, '#999'), obj.get_promo_type_display()
        )
    type_badge.short_description = "Type"

    def active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color:#27ae60;font-weight:bold">✅ Active</span>')
        return format_html('<span style="color:#999">⏸ Inactive</span>')
    active_badge.short_description = "Status"

    def date_range(self, obj):
        if obj.start_date and obj.end_date:
            return f"{obj.start_date} → {obj.end_date}"
        return '—'
    date_range.short_description = "Schedule"


# ══════════════════════════════════════════════════════════════
#  6. FIND US + OUR STORY
# ══════════════════════════════════════════════════════════════
@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Address & Hours', {'fields': ('address', 'opening_hours')}),
        ('Contact',         {'fields': ('phone', 'email')}),
        ('Google Maps',     {'fields': ('google_maps_url',)}),
    )
    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()


@admin.register(StorySection)
class StorySectionAdmin(admin.ModelAdmin):
    list_display       = ('order', 'heading', 'short_body')
    list_display_links = ('order', 'heading')
    ordering           = ('order',)

    def short_body(self, obj):
        return obj.body[:80] + ('…' if len(obj.body) > 80 else '')
    short_body.short_description = "Body"


# ══════════════════════════════════════════════════════════════
#  7. PAYMENT METHODS
# ══════════════════════════════════════════════════════════════
@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display       = ('icon', 'name', 'method_type', 'is_enabled', 'order')
    list_editable      = ('is_enabled', 'order')
    list_display_links = ('name',)
    ordering           = ('order',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not qs.exists():
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
        return super().get_queryset(request)


# ══════════════════════════════════════════════════════════════
#  ROLE MANAGEMENT
# ══════════════════════════════════════════════════════════════
from django.contrib.auth.admin import GroupAdmin
admin.site.register(Group, GroupAdmin)


# ══════════════════════════════════════════════════════════════
#  ORDER NOTIFICATIONS
# ══════════════════════════════════════════════════════════════
from .models import OrderNotification

@admin.register(OrderNotification)
class OrderNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter  = ('is_read',)
    ordering     = ('-created_at',)

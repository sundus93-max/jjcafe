from django.contrib import admin
from .models import Item, ContactInfo, StorySection


# ── MENU ITEMS ────────────────────────────────────────────────────────────────

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display  = ('name', 'price')
    search_fields = ('name',)
    ordering      = ('name',)



# ── FIND US ───────────────────────────────────────────────────────────────────

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """Prevent adding more than one ContactInfo row."""
    fieldsets = (
        ('Address & Hours', {
            'fields': ('address', 'opening_hours')
        }),
        ('Contact', {
            'fields': ('phone', 'email')
        }),
        ('Google Maps', {
            'fields': ('google_maps_url',),
            'description': (
                'Go to Google Maps → click Share → Embed a map → '
                'copy the URL inside src="…" and paste it here.'
            )
        }),
    )

    def has_add_permission(self, request):
        # Only allow one row
        return not ContactInfo.objects.exists()


# ── OUR STORY ─────────────────────────────────────────────────────────────────

@admin.register(StorySection)
class StorySectionAdmin(admin.ModelAdmin):
    list_display  = ('order', 'heading','short_body')
    list_editable = ('order',)
    list_display_links = ('heading',)
    ordering = ('order',)

    def short_body(self, obj):
        return obj.body[:80] + ('…' if len(obj.body) > 80 else '')
    short_body.short_description = 'Body'

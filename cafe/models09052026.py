from django.db import models

# ── MENU ──────────────────────────────────────────────────────────────────────
class Item(models.Model):
    name        = models.CharField(max_length=100)
    price       = models.DecimalField(max_digits=6, decimal_places=2)
    image       = models.ImageField(upload_to='items/', null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return self.name

# ── FIND US ───────────────────────────────────────────────────────────────────
class ContactInfo(models.Model):
    address         = models.TextField(help_text="Full street address")
    phone           = models.CharField(max_length=30, blank=True)
    email           = models.EmailField(blank=True)
    opening_hours   = models.TextField(blank=True, help_text="e.g. Mon–Fri 8am–6pm")
    google_maps_url = models.URLField(max_length=500, blank=True)

    class Meta:
        verbose_name = "Find Us"
        verbose_name_plural = "Find Us"

    def __str__(self):
        return "Contact & Location"

# ── OUR STORY ─────────────────────────────────────────────────────────────────
class StorySection(models.Model):
    order       = models.PositiveSmallIntegerField(default=1)
    heading     = models.CharField(max_length=200, blank=True)
    body        = models.TextField()
    image_url   = models.URLField(blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Our Story Section"
        verbose_name_plural = "Our Story"

    def __str__(self):
        return f"Section {self.order}: {self.heading or self.body[:40]}"

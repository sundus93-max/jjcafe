from django.db.models import Q
from datetime import date


def branding(request):
    from .models import SiteBranding, Promotion

    b        = SiteBranding.objects.first()
    is_admin = request.path.startswith('/admin/')

    if b:
        if is_admin:
            logo_url = b.admin_logo.url       if b.admin_logo       else (b.website_logo.url if b.website_logo else None)
            bg_url   = b.admin_background.url if b.admin_background else (b.website_background.url if b.website_background else None)
        else:
            logo_url = b.website_logo.url       if b.website_logo       else None
            bg_url   = b.website_background.url if b.website_background else None

        branding_data = {
            'app_name':       b.app_name,
            'tagline':        b.tagline,
            'logo_url':       logo_url,
            'background_url': bg_url,
            'primary_color':  b.primary_color,
            'secondary_color':b.secondary_color,
        }
    else:
        branding_data = {
            'app_name': 'JJCafe', 'tagline': 'Brew • Bite • Bliss',
            'logo_url': None, 'background_url': None,
            'primary_color': '#c8883a', 'secondary_color': '#2b1a0e',
        }

    # Active promotions for website pages
    today  = date.today()
    promos = []
    if not is_admin:
        promos = list(Promotion.objects.filter(
            is_active=True,
            show_on__in=['both', 'website'],
        ).filter(
            Q(start_date__isnull=True) | Q(start_date__lte=today)
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=today)
        ))

    return {'branding': branding_data, 'site_promotions': promos}

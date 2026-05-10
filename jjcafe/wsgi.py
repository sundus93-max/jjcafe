import os
from django.core.wsgi import get_wsgi_application

# Reads DJANGO_SETTINGS_MODULE env var
# On Render: set to 'jjcafe.settings.production'
# Locally:   set to 'jjcafe.settings.local'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jjcafe.settings.local')

application = get_wsgi_application()

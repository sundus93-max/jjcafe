from .base import *

# =====================================================
# LOCAL DEVELOPMENT SETTINGS
# =====================================================

DEBUG = True

ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1']

# Local MySQL database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jjcafe_db',
        'USER': 'root',
        'PASSWORD': '',         # ← Change to your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
        }
    }
}

# Local media serving
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Disable secure cookies locally
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE    = False

from .base import *
import dj_database_url

# =====================================================
# PRODUCTION SETTINGS (Render)
# =====================================================

DEBUG = False

ALLOWED_HOSTS = [
    '*.onrender.com',
    'localhost',
    '127.0.0.1',
    'jjcafe.onrender.com',
]

# ✅ HTTPS secure cookies for production
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False  # Render handles SSL termination

# ✅ Required for Render reverse proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# ✅ Trust only your production domain
CSRF_TRUSTED_ORIGINS = [
    'https://jjcafe.onrender.com',
]

# ✅ Database — reads from DATABASE_URL environment variable
DATABASES = {
    "default": dj_database_url.config(
        env='DATABASE_URL',
        conn_max_age=600,
        ssl_require=False,
    )
}

# =====================================================
# CLOUDINARY — serves all uploaded media in production
# =====================================================

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

MEDIA_URL = '/media/'

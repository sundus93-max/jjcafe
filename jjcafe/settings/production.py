from .base import *
import dj_database_url
 
DEBUG = False
 
ALLOWED_HOSTS = [
    '*.onrender.com',
    'localhost',
    '127.0.0.1',
    'jjcafe.onrender.com',
]
 
SESSION_COOKIE_SECURE   = True
CSRF_COOKIE_SECURE      = True
SECURE_SSL_REDIRECT     = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST    = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE    = "Lax"
 
CSRF_TRUSTED_ORIGINS = [
    'https://jjcafe.onrender.com',
]
 
# Supabase PostgreSQL via connection pooler (port 6543)
DATABASES = {
    "default": dj_database_url.parse(
        'postgresql://postgres.ghpcsykhbfjzfxqsehqd:JJJCafeLPT2026aws-1-ap-south-1.pooler.supabase.com:5432/postgres',
        conn_max_age=600,
    )
}
 
 
# Cloudinary for media uploads
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'
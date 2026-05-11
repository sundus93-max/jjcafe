import os
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

# ✅ FIXED DATABASE SECTION
DATABASE_URL = os.environ.get("DATABASE_URL")

if isinstance(DATABASE_URL, bytes):
    DATABASE_URL = DATABASE_URL.decode()

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=True,
    )
}
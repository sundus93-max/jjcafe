from .base import *
import dj_database_url
import os

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

#USE_LIVE_DB = os.environ.get('USE_LIVE_DB', 'false').lower() == 'true'
USE_LIVE_DB = False

if USE_LIVE_DB:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'jjcafe_db',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'sql_mode': 'STRICT_TRANS_TABLES',
                'charset': 'utf8mb4',
            }
        }
    }

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
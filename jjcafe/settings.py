"""
Django settings for jjcafe project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-=e4jd6k2bpjo@fyyw3uw&g^^4l@6&_1^67gkd%y^2^rsp*7fg%'

DEBUG = True

ALLOWED_HOSTS = ["*"]

# ─────────────────────────────────────────
# APPS
# ─────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',          # ← CORS for Android app
    'cafe',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1

# ─────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',     # ← must be FIRST
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# ─────────────────────────────────────────
# CORS — Allow Android app to call API
# ─────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = True       # During development — restrict in production

ROOT_URLCONF = 'jjcafe.urls'

# ─────────────────────────────────────────
# TEMPLATES
# ─────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'cafe' / 'Templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cafe.context_processors.branding',
            ],
        },
    },
]

WSGI_APPLICATION = 'jjcafe.wsgi.application'

# ─────────────────────────────────────────
# DATABASE (MySQL / MariaDB)
# ─────────────────────────────────────────
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
        }
    }
}

# ─────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─────────────────────────────────────────
# ALLAUTH SETTINGS
# ─────────────────────────────────────────
ACCOUNT_LOGIN_METHODS       = {"email"}
ACCOUNT_SIGNUP_FIELDS       = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION  = "none"
LOGIN_URL                   = '/login/'     # ← Fixed (was Login_URL)
LOGIN_REDIRECT_URL          = '/'
LOGOUT_REDIRECT_URL         = '/'

# ─────────────────────────────────────────
# INTERNATIONALIZATION
# ─────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True

# ─────────────────────────────────────────
# STATIC & MEDIA
# ─────────────────────────────────────────
STATIC_URL       = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

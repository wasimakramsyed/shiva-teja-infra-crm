from pathlib import Path
from decouple import config

# --------------------------------------------------
# Base Directory
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# Security
# --------------------------------------------------

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="127.0.0.1,localhost"
).split(",")
CSRF_TRUSTED_ORIGINS = [
    "https://shivateja-prod-v2.eba-km3ptqbm.ap-south-2.elasticbeanstalk.com",
    "https://shivateja-infra.in",
    "https://www.shivateja-infra.in",
]

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# ======================================================
# Email Configuration
# ======================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_USE_SSL = False

EMAIL_HOST_USER = config(
    "EMAIL_HOST_USER",
    default=""
)

EMAIL_HOST_PASSWORD = config(
    "EMAIL_HOST_PASSWORD",
    default=""
)

DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL",
    default=""
)

 
SERVER_EMAIL = DEFAULT_FROM_EMAIL
# --------------------------------------------------
# Installed Apps
# --------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'settings_config',
    'employees',
    'teams',
    'projects',
    'leads',
    'customers',
    'bookings',
    'payments',
    'commissions',
    'registrations',
    'reports',
    'dashboard',
    'notifications',
    'common',
    'activities',
]

# --------------------------------------------------
# Middleware
# --------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise should come immediately after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# --------------------------------------------------
# Templates
# --------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# --------------------------------------------------
# PostgreSQL Database
# --------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", default="5432"),
        "CONN_MAX_AGE": 600,
        "OPTIONS": {
            "connect_timeout": 10,
        },
    }
}

# --------------------------------------------------
# Password Validation
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# --------------------------------------------------
# Internationalization
# --------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# --------------------------------------------------
# Static Files
# --------------------------------------------------

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)
# --------------------------------------------------
# Media Files
# --------------------------------------------------

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------------
# Authentication
# --------------------------------------------------

AUTH_USER_MODEL = "accounts.User"

# --------------------------------------------------
# Default Primary Key
# --------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======================================================
# MSG91 SMS Configuration
# ======================================================

MSG91_AUTH_KEY = config(
    "MSG91_AUTH_KEY",
    default=""
)

MSG91_TEMPLATE_ID = config(
    "MSG91_TEMPLATE_ID",
    default=""
)

MSG91_SENDER_ID = config(
    "MSG91_SENDER_ID",
    default=""
)

# ======================================================
# Production Settings
# ======================================================

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_COOKIE_SECURE = not DEBUG

SESSION_COOKIE_SECURE = not DEBUG

SECURE_SSL_REDIRECT = not DEBUG

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

SECURE_REFERRER_POLICY = "same-origin"

CSRF_COOKIE_HTTPONLY = True

SESSION_COOKIE_HTTPONLY = True

CONN_MAX_AGE = 600

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/login/"
# ======================================================
# Logging Configuration
# ======================================================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "standard": {
            "format": "[{asctime}] {levelname} {name}: {message}",
            "style": "{",
        },
    },

    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "django.log",
            "formatter": "standard",
        },
    },

    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
        "": {
            "handlers": ["file"],
            "level": "INFO",
        },
    },
}

SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

EMAIL_TIMEOUT = 30
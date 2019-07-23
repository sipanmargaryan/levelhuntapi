import os
from datetime import timedelta

from .base import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV.str('SECRET_KEY', 'Keep it secret!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV.bool('DEBUG', True)
ENABLE_DEBUG_TOOLBAR = DEBUG and ENV.bool('ENABLE_DEBUG_TOOLBAR', False)

ALLOWED_HOSTS = ENV.list('ALLOWED_HOSTS', default=['*'])
INTERNAL_IPS = ENV.list('INTERNAL_IPS', default=('127.0.0.1',))

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

EXTERNAL_APPS = [
    'django_celery_results',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'django_extensions',
    'rest_framework_swagger',
]

PROJECT_APPS = [
    'core.email',
    'core.utils',
    'core.tests',
    'core.views',
    'users',
    'skills',
    'questions',
    'universities',
    'admins',
]

INSTALLED_APPS.extend(EXTERNAL_APPS + PROJECT_APPS)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Django Debug Toolbar settings
# https://django-debug-toolbar.readthedocs.io/en/stable/configuration.html

if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

    DEBUG_TOOLBAR_CONFIG = {
        'RESULTS_CACHE_SIZE': 50,
        'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
    }

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.sql.SQLPanel',
    ]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database

DATABASES = {
    'default': ENV.db_url('DATABASE_URL', default='sqlite://:memory:'),
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Redis settings

REDIS_URL = 'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_PATH}'.format(
    REDIS_HOST=ENV.str('REDIS_HOST', '127.0.0.1'),
    REDIS_PORT='6379',
    REDIS_PATH='0',
)

# Cache settings

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Celery settings

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_TASK_ALWAYS_EAGER = ENV.bool('CELERY_TASK_ALWAYS_EAGER', False)

CELERY_ROUTES = {
    'core.email.tasks.send_async_email': {'queue': 'email'},
}

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 15,
}

# JWT settings

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}

# Email settings

DEFAULT_FROM_EMAIL = 'no-reply@levelhunt.com'
EMAIL_BASE_TEMPLATE = 'email/base.html'
EMAIL_HOST = ENV.str('EMAIL_HOST', 'localhost')
EMAIL_PORT = ENV.int('EMAIL_PORT', 25)
EMAIL_BACKEND = ENV.str('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

# SENTRY Integration

SENTRY_DSN = ENV.str('SENTRY_DSN', '')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
    )

AUTH_USER_MODEL = 'users.User'
ADMIN_URLS_PATH = ENV.str('ADMIN_URLS_PATH', 'admin/')
LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'
SITE_NAME = 'LevelHunt'
CLIENT_DOMAIN = ENV.str('CLIENT_DOMAIN', 'localhost:3000')
URL_SCHEME = ENV.str('URL_SCHEME', 'http')

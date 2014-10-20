# OUTSIDE OF SCHOOL PROJECT YOU SHOULD NOT COMMIT THIS.

import os

from .common import *

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = ['static']
STATIC_ROOT = os.getenv('STATIC_ROOT', "sitestatic")
MEDIA_ROOT = os.getenv('MEDIA_ROOT', "")

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

# Database
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import dj_database_url
DATABASES = {}
DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Test Email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# Security
SECRET_KEY = os.getenv('SECRET_KEY', 'mopi)(=3l5y-)n*o2$io0=i(_=5vo=u4@5l%3kliqtkd_k(12=')
DEBUG = False
TEMPLATE_DEBUG = False

# OUTSIDE OF SCHOOL PROJECT YOU SHOULD NOT COMMIT THIS.

import os

from .common import *

# Database
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import dj_database_url
DATABASES = {}
DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

# Security
SECRET_KEY = 'u=^)5nuz)f)*svbu22kxg^(g+w2q*zk!x##o^hk7((_+87dsoc'
DEBUG = True
TEMPLATE_DEBUG = False


ALLOWED_HOSTS = ['.abarticulus.me']

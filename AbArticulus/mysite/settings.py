# OUTSIDE OF SCHOOL PROJECT YOU SHOULD NOT COMMIT THIS.

import os

from .common import *

# Database
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import dj_database_url
DATABASES = {}
DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

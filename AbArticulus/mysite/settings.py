# OUTSIDE OF SCHOOL PROJECT YOU SHOULD NOT COMMIT THIS.

import os

from .common import *

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = ['static']
STATIC_ROOT = "sitestatic"

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
EMAIL_HOST_USER = 'orlykahnmakeupartist@gmail.com'
EMAIL_HOST_PASSWORD = 'testpassword'
DEFAULT_FROM_EMAIL = 'orlykahnmakeupartist@gmail.com'

# Security
SECRET_KEY = 'u=^)5nuz)f)*svbu22kxg^(g+w2q*zk!x##o^hk7((_+87dsoc'
DEBUG = True
TEMPLATE_DEBUG = False


AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.yahoo.YahooBackend',
    'social_auth.backends.browserid.BrowserIDBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.contrib.disqus.DisqusBackend',
    'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    'social_auth.backends.contrib.orkut.OrkutBackend',
    'social_auth.backends.contrib.foursquare.FoursquareBackend',
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.contrib.vk.VKOAuth2Backend',
    'social_auth.backends.contrib.live.LiveBackend',
    'social_auth.backends.contrib.skyrock.SkyrockBackend',
    'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
    'social_auth.backends.contrib.readability.ReadabilityBackend',
    'social_auth.backends.contrib.fedora.FedoraBackend',
    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)



TWITTER_CONSUMER_KEY         = ''
TWITTER_CONSUMER_SECRET      = ''
FACEBOOK_APP_ID              = ''
FACEBOOK_API_SECRET          = ''
LINKEDIN_CONSUMER_KEY        = ''
LINKEDIN_CONSUMER_SECRET     = ''
ORKUT_CONSUMER_KEY           = ''
ORKUT_CONSUMER_SECRET        = ''
GOOGLE_CONSUMER_KEY          = ''
GOOGLE_CONSUMER_SECRET       = ''
GOOGLE_OAUTH2_CLIENT_ID      = '1071906404324-fkpki7vpattft1qalksm93j0pj3pmovo.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET  = '7Qkbly5ZunEL7OSgEUCPAUBt'
FOURSQUARE_CONSUMER_KEY      = ''
FOURSQUARE_CONSUMER_SECRET   = ''
VK_APP_ID                    = ''
VK_API_SECRET                = ''
LIVE_CLIENT_ID               = ''
LIVE_CLIENT_SECRET           = ''
SKYROCK_CONSUMER_KEY         = ''
SKYROCK_CONSUMER_SECRET      = ''
YAHOO_CONSUMER_KEY           = ''
YAHOO_CONSUMER_SECRET        = ''
READABILITY_CONSUMER_SECRET  = ''
READABILITY_CONSUMER_SECRET  = ''



LOGIN_URL          = '/login-form/'
LOGIN_REDIRECT_URL = '/logged-in/'
LOGIN_ERROR_URL    = '/login-error/'
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
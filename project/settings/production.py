# NOTE: os, BASE_DIR, DATABASES are defined in .base.py
import os
from .base import *

ENVIRONMENT = 'production'

SOCIAL_AUTH_GITHUB_KEY = os.environ['GITHUB_KEY']
SOCIAL_AUTH_GITHUB_SECRET = os.environ['GITHUB_SECRET']

DEBUG = False
ALLOWED_HOSTS = ['*']

# Only when running in Heroku
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'https://afternoon-headland-18234.herokuapp.com/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '..', 'apps', 'core', 'static'),
]

if "DYNO" in os.environ:
    import dj_database_url

    # Override the sqlite
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

    # Append whitenoise middleware
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

    # This is the hostname for your site
    ALLOWED_HOSTS = ['afternoon-headland-18234.herokuapp.com']

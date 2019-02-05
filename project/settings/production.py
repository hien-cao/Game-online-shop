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

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '..', 'apps', 'apis', 'dev_api', 'static'),
    os.path.join(BASE_DIR, '..', 'apps', 'core', 'static'),
    os.path.join(BASE_DIR, '..', 'apps', 'game', 'static'),
    os.path.join(BASE_DIR, '..', 'apps', 'review', 'static'),
    os.path.join(BASE_DIR, '..', 'apps', 'user', 'static')
]

if "DYNO" in os.environ:

    # Override the sqlite
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)


    DEBUG = True
    # Append whitenoise middleware
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

    # This is the hostname for your site
    ALLOWED_HOSTS = ['afternoon-headland-18234.herokuapp.com']

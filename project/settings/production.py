# NOTE: os, BASE_DIR, DATABASES are defined in .base.py
from .base import *


ENVIRONMENT = 'production'

SOCIAL_AUTH_GITHUB_KEY = os.environ['GITHUB_KEY']
SOCIAL_AUTH_GITHUB_SECRET = os.environ['GITHUB_SECRET']

DEBUG = False
ALLOWED_HOSTS = ['*']

# Only when running in Heroku
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

if "DYNO" in os.environ:

    #Override the sqlite
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

    # Once service is succesfully deployed this should be False
    DEBUG = True # <== THIS NEEDS TO BE FALSE AFTER YOU GET EVERYTHING WORKING!

    # This is the hostname for your site
    ALLOWED_HOSTS = ['afternoon-headland-18234.herokuapp.com']

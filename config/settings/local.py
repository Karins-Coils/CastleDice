from .base import *

DEBUG = True

# don't want emails actually firing off during local dev!
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# default local DB setup using postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'CastleDice',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

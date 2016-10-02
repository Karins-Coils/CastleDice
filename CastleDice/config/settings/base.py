"""
Django settings for CastleDice project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
import json
from unipath import Path

from django.core.exceptions import ImproperlyConfigured

# assumes .django-env.json exists in the same folder as this settings file
ENV_FILE = Path(__file__).ancestor(1).child('.django-env.json')
BASE_DIR = Path(__file__).ancestor(3)


def get_env_var(var, default=None):
    """
    Retrieve the variable from the Environment, or a specified env file
    :param str|unicode var:
    :param default:
    :return: either the retrieved value from the env or file, or the default
    :raises ImproperlyConfigured:
        if the key is not found in either place, and no default is passed
    """
    env_value = None

    # try loading the env file and getting it from there
    try:
        with open(ENV_FILE) as f:
            environs = json.loads(f.read())
            env_value = environs.get(var)
    except IOError, ValueError:
        # if it wasn't there, try loading directly from the ENV
        env_value = os.environ.get(var)

    # still no value, and no default value
    if env_value is None and default is None:
        error_msg = "The environment variable {} was not found in the " \
                    "environment, nor in {}.".format(var, ENV_FILE)
        raise ImproperlyConfigured(error_msg)
    return env_value if env_value is not None else default


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

SECRET_KEY = get_env_var('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # django-annoying - https://github.com/skorokithakis/django-annoying
    'annoying',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # The Django sites framework is required
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'die',
    'game',
    'playermat'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',

)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            BASE_DIR.child('templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
            'debug': True
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
# Static asset configuration
STATIC_ROOT = BASE_DIR.child('staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    BASE_DIR.child('static'),
)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SITE_ID = 1

import dj_database_url

from .base import *

DATABASES['default'] = dj_database_url.parse(get_env_var('DATABASE_URL'))

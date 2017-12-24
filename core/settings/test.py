# flake8: noqa
from .base import *

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
    'USE_MIGRATIONS': True,
}
DEBUG = True

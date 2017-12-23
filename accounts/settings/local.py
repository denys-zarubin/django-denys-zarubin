# flake8: noqa
from .base import *

DEBUG = os.getenv('DEBUG', True)
PAGE_CACHE_SECONDS = 1
INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

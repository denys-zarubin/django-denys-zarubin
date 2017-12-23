# flake8: noqa
from .base import *

DEBUG = os.getenv('DEBUG', True)
PAGE_CACHE_SECONDS = 1
SECRET_KEY = "12345"

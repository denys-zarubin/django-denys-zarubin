# flake8: noqa
from .base import *

# If you want to use mysql and run-tests memory, uncomment this lines.
"""
DATABASES['OPTIONS']: {
                'init_command': 'SET storage_engine=MEMORY'
            }
"""

# For inner tests. Do not use if have database specific ORM queries.
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
    'USE_MIGRATIONS': True,
}
DEBUG = True

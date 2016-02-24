"""local dev config for harshp.com

"""

from .base.base import *
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['*', ]

STATIC_URL = '/static/'
if DEBUG:
    STATIC_ROOT = 'static'
    MEDIA_ROOT = ''
else:
    PROJECT_PATH = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
    STATIC_ROOT = ''  # PROJECT_PATH + '/static/'
    MEDIA_ROOT = PROJECT_PATH + '/media/'

MEDIA_URL = '/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'harshp_dot_com',
        'USER': os.getenv('HARSHP_MYSQL_ID', 'harshp'),
        'PASSWORD': os.getenv('HARSHP_MYSQL_PASS', ''),
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

import sys
if 'test' in sys.argv or 'test_coverage' in sys.argv:
    # Covers regular testing and django-coverage
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
    DEBUG = False
    TEST_RUNNER = 'django_slowtests.DiscoverSlowestTestsRunner'
    NUM_SLOW_TESTS = 100
    import logging
    logging.disable(logging.CRITICAL)

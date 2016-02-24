"""dev config connecting to remote harshp.com server

"""

from .base.base import *

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

STATIC_URL = '/static/'
if DEBUG:
    STATIC_ROOT = ''
    MEDIA_ROOT = ''
else:
    PROJECT_PATH = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
    STATIC_ROOT = ''  # PROJECT_PATH + '/static/'
    MEDIA_ROOT = PROJECT_PATH + '/media/'

MEDIA_URL = '/media/'

# MySQL
# DEV WITH SSH TUNNEL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'harshp_dot_com',
        'USER': 'harshp',
        'PASSWORD': os.environ.get('HARSHP_MYSQL_PASS', ''),
        'HOST': '127.0.0.1',
        'PORT': '33306',
    }
}

FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'storages.backends.s3boto.S3BotoStorage',
            'OPTIONS': {
                'location': MEDIA_ROOT,
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.by_date',
        },
        'thumbnails': {
            'ENGINE': 'storages.backends.s3boto.S3BotoStorage',
            'OPTIONS': {
                'location': MEDIA_ROOT,
            },
        },
    },
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

REDACTOR_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

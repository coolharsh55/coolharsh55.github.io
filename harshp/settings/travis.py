"""travis config for CI server for harshp.com

"""

from .base.base import *

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*', ]
# ALLOWED_HOSTS = ['.harshp.com', '.harshp.com.',] # TEMPORARY

# AWS and S3
AWS_STORAGE_BUCKET_NAME = 'harshp-media'
AWS_ACCESS_KEY_ID = os.environ.get('HARSHP_AWS_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('HARSHP_AWS_KEY', '')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_QUERYSTRING_AUTH = False
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_SECURE_URLS = False       # use http instead of https
AWS_QUERYSTRING_AUTH = False     # complex authentication-related requests
AWS_HEADERS = {
    'Cache-Control': 'max-age=86400',
}

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_HOST = 's3.eu-west-1.amazonaws.com'

STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
STATIC_ROOT = '/static/'
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN + 'media/'
MEDIA_ROOT = '/media/'

# MySQL
# DEV WITH SSH TUNNEL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'harshp_dot_com',
        'USER': 'travis',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

TEST_RUNNER = 'django_slowtests.DiscoverSlowestTestsRunner'
NUM_SLOW_TESTS = 100
import logging
logging.disable(logging.CRITICAL)

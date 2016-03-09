"""static and media files settings for harshp_com"""

import os
from .basepath import BASE_DIR

STATICFILES_DIRS = [
    BASE_DIR + '/static/',
]

THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    # 'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

MODE = os.environ.get('HARSHP_COM_MODE', 'dev')

if MODE == 'production' or MODE == 'test_prod':
    # django-storages | boto | AWS S3
    AWS_STORAGE_BUCKET_NAME = 'harshp-staticmedia'
    AWS_ACCESS_KEY_ID = os.environ.get('HARSHP_COM_AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.environ.get('HARSHP_COM_AWS_SECRET_KEY')
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_SECURE_URLS = False
    AWS_QUERYSTRING_AUTH = False
    AWS_HEADERS = {
        'Cache-Control': 'max-age=86400',
    }
    # AWS_S3_HOST = 's3.eu-west-1.amazonaws.com'

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
    STATIC_ROOT = '/static/'
    MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN + 'media/'
    MEDIA_ROOT = '/media/'

elif MODE == 'dev':
    STATIC_URL = '/static/'

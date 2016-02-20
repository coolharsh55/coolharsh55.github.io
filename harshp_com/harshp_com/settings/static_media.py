"""static and media files settings for harshp_com"""

from .basepath import BASE_DIR

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR + '/static/',
]

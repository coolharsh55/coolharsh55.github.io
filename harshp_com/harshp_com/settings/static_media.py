"""static and media files settings for harshp_com"""

import os
from .basepath import BASE_DIR

STATICFILES_DIRS = [
    BASE_DIR + '/static/',
]

MODE = os.environ.get('HARSHP_COM_MODE', 'dev')

if MODE == 'production':
    pass
elif MODE == 'dev':
    STATIC_URL = '/static/'

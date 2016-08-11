"""database settings for harshp_com"""

import os
import sys

from .basepath import BASE_DIR

DATABASE_SQLITE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}

DATABASE_POSTGRES = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'harshp_com',
    'USER': 'harshp_db_admin',
    'HOST': 'localhost',
    'PORT': 5432,
}

DATABASES = {'default': DATABASE_POSTGRES}

MODE = os.environ.get('HARSHP_COM_MODE', 'dev')

if MODE == 'production':
    DATABASES['default']['PASSWORD'] = os.environ.get(
        'HARSHP_COM_POSTGRES_PASSWORD', None)
elif MODE == 'test_prod':
    # TODO: establish production database over ssh
    pass
elif MODE == 'dev':
    DATABASES['default']['PASSWORD'] = 'harshp_com'

# test settings
if sys.argv[1] == "test":
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}

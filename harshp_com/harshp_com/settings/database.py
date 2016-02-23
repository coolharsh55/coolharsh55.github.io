"""database settings for harshp_com"""

import os

from .basepath import BASE_DIR

DATABASE_SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASE_POSTGRES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'harshp_com',
        'USER': 'harshp_db_admin',
        'PASSWORD': os.environ.get('HARSHP_DB_PASS', None),
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

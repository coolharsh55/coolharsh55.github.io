import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['*', ]

STATIC_URL = '/static/'
if DEBUG:
    STATIC_ROOT = ''
else:
    PROJECT_PATH = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
    STATIC_ROOT = PROJECT_PATH + '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = ''

SECRET_KEY = os.environ.get('HARSHP_SECRET_KEY', '')

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

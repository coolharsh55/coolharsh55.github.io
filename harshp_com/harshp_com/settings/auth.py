"""auth settings for harshp_com"""

import os

MODE = os.environ.get('HARSHP_COM_MODE', 'dev')
TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY', None)
TELEGRAM_API_NOTIF_KEY = os.environ.get('TELEGRAM_API_NOTIF_KEY', None)

# PRODUCTION
if MODE == 'production':

    SECRET_KEY = os.environ.get('HARSHP_COM_DJANGO_KEY', None)
    ALLOWED_HOSTS = ['.harshp.com']

    # CSRF
    CSRF_COOKIE_SECURE = True

    # SESSION
    SESSION_COOKIE_AGE = 18000  # 5 HOURS
    SESSION_COOKIE_SECURE = True
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# DEVELOPMENT
elif MODE == 'dev' or MODE == 'test_prod':

    SECRET_KEY = os.environ.get(
        'HARSHP_COM_DJANGO_KEY',
        'y&v5_r#l09fj!q2s)o&j8fh2tx4$5ig8%uak%$mr^nx)54&ugh')
    ALLOWED_HOSTS = ['*']


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'),
    },
]

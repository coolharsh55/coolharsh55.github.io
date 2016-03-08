"""apps settings for harshp_com"""

import os

INSTALLED_APPS = [
    # django-jet admin theme
    'jet.dashboard',
    'jet',

    # default django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # third-party apps and plugins
    # social metadata
    'meta',
    # django-robots: robots.txt
    'robots',
    # django-subdomains
    'subdomains',

    # harshp_com apps
    'articles',
    'blog',
    'brainbank',
    'dev',
    'friends',
    'hobbies',
    'journal',
    'lifeX',
    'me',
    'poems',
    'research',
    'sitebase',
    'stories',
]

MODE = os.environ.get('HARSHP_COM_MODE', 'dev')

if MODE == 'production' or MODE == 'test_prod':
    INSTALLED_APPS.extend([
        # django-storages
        'storages',
    ])

elif MODE == 'dev':
    INSTALLED_APPS.extend([])

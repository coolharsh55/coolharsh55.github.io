"""apps settings for harshp_com"""

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
    # django-subdomains
    'subdomains',

    # harshp_com apps
    'sitebase',
    'blog',
]

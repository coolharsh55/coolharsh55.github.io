"""apps config for harshp.com

"""

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

ADMIN_APPS = (
    # admin
    'suit',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'bootstrap3',
    'ckeditor',
    'meta',
    'storages',
    'subdomains',
    'redactor',
    'robots',
)

HARSHP_APPS = (
    # my apps
    'sitedata',
    'blog',
    'stories',
    'poems',
    'articles',
    'lifeX',
    'brainbank',
    'friends',
    'hobbies',
    'devblog',
)

FILER_APPS = (
    # django-filer
    'easy_thumbnails',
    'filer',
    'mptt',
)

INSTALLED_APPS = DJANGO_APPS + \
    ADMIN_APPS + \
    THIRD_PARTY_APPS + \
    HARSHP_APPS + \
    FILER_APPS

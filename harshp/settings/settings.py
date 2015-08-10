import os
from django.conf import global_settings

PROJECT_PATH = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))

# ######## EMAILS START ##########
# For email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'harshp_dot_com'
EMAIL_HOST_PASSWORD = os.getenv('HARSHP_SENDGRID_KEY', '')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# ####### EMAILS END ############


# ####### CKEDITOR START ##########
CKEDITOR_UPLOAD_PATH = '/media/'
CKEDITOR_JQUERY_URL = '''
    //ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js'''
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}
# ####### CKEDITOR END ############


# ####### SUIT ADMIN START ##########
SUIT_CONFIG = {
    'ADMIN_NAME': 'harshp.com',
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
    'SEARCH_URL': 'admin:auth_user_changelist',
    'MENU_OPEN_FIRST_CHILD': False,
    'MENU_ICONS': {
        'sites': 'icon-star',
        'auth': 'icon-lock',
    },
    'MENU': (
        {'app': 'robots', 'label': 'robots.txt', 'icon': 'icon-wrench'},
        'sites',
        {'app': 'blog', 'label': 'Blog', 'icon': 'icon-pencil'},
        {'app': 'stories', 'label': 'Stories', 'icon': 'icon-book'},
        {'app': 'poems', 'label': 'Poems', 'icon': 'icon-asterisk'},
        {'app': 'articles', 'label': 'Articles', 'icon': 'icon-tag'},
        {'app': 'brainbank', 'label': 'Brain Bank', 'icon': 'icon-qrcode'},
        {'app': 'lifex', 'label': 'Life X', 'icon': 'icon-road'},
        {'app': 'hobbies', 'label': 'Hobbies', 'icon': 'icon-time'}
    ),

}
# ####### SUIT ADMIN END ############

ADMINS = (
    ('Harshvardhan Pandit', 'me@harshp.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

SECRET_KEY = os.environ.get('HARSHP_SECRET_KEY', '')

# Additional locations of static files
STATICFILES_DIRS = (
    PROJECT_PATH + '/static/',
    'sitedata/static/',
    'blog/static/',
    'stories/static/',
    'poems/static/',
    'stories/static/',
    'articles/static/',
    'lifeX/static/',
    'brainbank/static/',
    'friends/static/',
    'hobbies/static/',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'harshp.multihost.MultiHostMiddleware',
)

ROOT_URLCONF = 'harshp.urls'

SUBDOMAIN_URLCONFS = {
    None: 'harshp.urls',  # no subdomain, e.g. ``example.com``
    'www': 'harshp.urls',
    'admin': 'harshp.adminurls',
    'articles': 'articles.urls',
    'blog': 'blog.urls',
    'brainbank': 'brainbank.urls',
    'friends': 'friends.urls',
    'lifex': 'lifeX.urls',
    'poems': 'poems.urls',
    'stories': 'stories.urls',
    'hobbies': 'hobbies.urls',
}

WSGI_APPLICATION = 'harshp.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_PATH + '/templates/',
    'sitedata/templates/',
    'blog/templates',
    'stories/templates',
    'poems/templates',
    'articles/templates',
    'lifeX/templates',
    'brainbank/templates',
    'friends/templates',
    'hobbies/templates',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    "harshp.context_processors.site",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # admin
    'suit',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # other apps
    'bootstrap3',
    'ckeditor',
    # 'django_seed',
    'meta',
    'storages',
    'subdomains',
    'robots',

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
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

BOOTSTRAP3 = {
    'jquery_url': '''
        https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js''',
    'base_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/',
    'css_url': None,
    'theme_url': None,
    'javascript_url': None,
    'javascript_in_head': False,
    'include_jquery': True,
}

# ################ SOCIAL META TAGS ##################

META_SITE_PROTOCOL = 'http'
# META_SITE_DOMAIN ='harshp.com'
# META_SITE_TYPE = ''
META_SITE_NAME = 'harshp.com'
META_INCLUDE_KEYWORDS = []
META_DEFAULT_KEYWORDS = []
# META_IMAGE_URL = ''
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_GOOGLEPLUS_PROPERTIES = True
META_USE_SITES = True

# ####################################################
SECRET_KEY = os.environ.get('HARSHP_SECRET_KEY', '')
MODE = os.environ.get('HARSHP_MODE', 'local')
# MODE = 'dev'
# DEBUG = True
if MODE == 'prod':
    from prod import *
    # print 'production'
elif MODE == 'dev':
    from dev import *
    # print 'dev'
elif MODE == 'travis':
    from prod import *
    DATABASES['default']['USER'] = 'travis'
    DATABASES['default']['PASSWORD'] = ''
else:
    from local import *
    # print 'local'

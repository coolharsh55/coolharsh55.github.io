"""template config for harshp.com

"""

import os
from django.conf import global_settings

PROJECT_PATH = os.path.realpath(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__))))

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
    'django.core.context_processors.request',)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

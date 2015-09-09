"""staticfiles config for harshp.com

"""

import os

PROJECT_PATH = os.path.realpath(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__))))

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
    'devblog/static/',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

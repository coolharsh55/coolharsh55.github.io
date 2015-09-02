"""urls for stories
"""

from django.conf.urls import patterns, include, url
from django.conf import settings
from harshp.settings.local import STATIC_ROOT

storiesurlpatterns = patterns(
    '',
    # INDEX
    url(
        r'^$',
        'stories.views.index',
        name='index'
    ),

    # STORY
    url(
        r'^(?P<story>[\w-]+)/$',
        'stories.views.story',
        name='post'
    ),
)

handler404 = 'harshp.views.handler404'
handler500 = 'harshp.views.handler500'

urlpatterns = patterns(
    '',
    url(r'', include(storiesurlpatterns, namespace='stories')),
)

# if DEBUG is True it will be served automatically
if settings.DEBUG is False and settings.MODE == 'local':
    urlpatterns += patterns(
        '',
        url(
            r'^static/(?P<path>.*)$',
            'django.views.static.serve',
            {
                'document_root': STATIC_ROOT
            }
        ),
    )

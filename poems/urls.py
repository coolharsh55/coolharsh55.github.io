"""urls for poems
"""

from django.conf.urls import patterns, include, url
from django.conf import settings
from harshp.settings.local import STATIC_ROOT

poemsurlpatterns = patterns(
    '',
    # INDEX
    url(
        r'^$',
        'poems.views.index',
        name='index'
    ),

    # POEM
    url(
        r'^(?P<poem>[\w-]+)/$',
        'poems.views.poem',
        name='post'
    ),
)

handler404 = 'harshp.views.handler404'
handler500 = 'harshp.views.handler500'

urlpatterns = patterns(
    '',
    url(r'', include(poemsurlpatterns, namespace='poems')),
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

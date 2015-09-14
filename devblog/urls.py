"""urls for dev blog
"""

from django.conf.urls import patterns, include, url
from django.conf import settings
from harshp.settings.local import STATIC_ROOT

devblogurlpatterns = patterns(
    # blog index
    '',
    url(
        r'^blog/$',
        'devblog.views.blog_index',
        name='blog_index',
    ),

    # blog post
    url(
        r'^blog/(?P<blog_post>[\w\d-]+)/$',
        'devblog.views.blog_post',
        name='blog_post',
    ),

    # series index
    url(
        r'^series/$',
        'devblog.views.series_index',
        name='series_index'
    ),

    # series page
    url(
        r'^series/(?P<series>[\2\d-]+)/$',
        'devblog.views.series_page',
        name='series_page',
    ),

)

handler404 = 'harshp.views.handler404'
handler500 = 'harshp.views.handler500'

urlpatterns = patterns(
    '',
    url(r'', include(devblogurlpatterns, namespace='devblog')),
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

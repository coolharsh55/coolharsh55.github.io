"""urls for dev blog
"""

from django.conf.urls import patterns, include, url
from django.conf import settings
from harshp.settings.local import STATIC_ROOT

devblogurlpatterns = patterns(
    '',
    # dev home
    url(
        r'^$',
        'devblog.views.home',
        name='dev_home'
    ),

    # blog index
    url(
        r'^blog/$',
        'devblog.views.blog_index',
        name='blog_index',
    ),

    # all series index
    url(
        r'^blog/series/$',
        'devblog.views.series_index',
        name='series_index'
    ),

    # specific series index
    url(
        r'^blog/series/(?P<series>[\w\d-]+)/$',
        'devblog.views.blog_series',
        name='blog_series'
    ),

    # series page, can contain 'blog' as series
    url(
        r'^blog/series/(?P<series>[\w\d-]+)/(?P<blog_post>[\w\d-]+)/$',
        'devblog.views.blog_post',
        name='blog_post',
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

"""urls for dev blog
"""

from django.conf.urls import patterns, include, url

devblogurlpatterns = patterns(
    # index
    '',
    url(
        r'^$',
        'devblog.views.index',
        name='index',
    ),

    # blog post
    url(
        r'^/(?P<blogpost>[\w\d-]+)/$',
        'devblog.views.blogpost',
        name='blogpost',
    )

)

handler404 = 'harshp.views.handler404'
handler500 = 'harshp.views.handler500'

urlpatterns = patterns(
    '',
    url(r'', include(devblogurlpatterns, namespace='devblog')),
)

"""urls for blog
"""

from django.conf.urls import patterns, include, url

blogurlpatterns = patterns(
    '',
    # INDEX
    url(
        r'^$',
        'blog.views.index',
        name='index'
    ),

    # BLOGPOST
    url(
        r'^(?P<blogpost>[\w-]+)/$',
        'blog.views.blogpost',
        name='post'
    ),
)

urlpatterns = patterns(
    '',
    url(r'', include(blogurlpatterns, namespace='blog')),
)

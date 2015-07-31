"""urls for Articles
"""

from django.conf.urls import patterns, include, url

articlesurlpatterns = patterns(
    '',
    # INDEX
    url(
        r'^$',
        'articles.views.index',
        name='index'
    ),

    # ARTICLE
    url(
        r'^(?P<article>[\w-]+)/$',
        'articles.views.article',
        name='post'
    ),
)

urlpatterns = patterns(
    '',
    url(
        r'',
        include(articlesurlpatterns, namespace='articles')
    ),
)

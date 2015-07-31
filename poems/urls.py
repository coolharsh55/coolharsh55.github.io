"""urls for poems
"""

from django.conf.urls import patterns, include, url

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

urlpatterns = patterns(
    '',
    url(r'', include(poemsurlpatterns, namespace='poems')),
)

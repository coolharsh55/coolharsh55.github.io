"""urls for stories
"""

from django.conf.urls import patterns, include, url

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

urlpatterns = patterns(
    '',
    url(r'', include(storiesurlpatterns, namespace='stories')),
)

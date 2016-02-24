"""urls for hobbies

    book_index, book
    movie_index, movie
    tvshow_index, tvshow
    game_index, game
"""

from django.conf.urls import patterns, include, url
from django.conf import settings
from harshp.settings.local import STATIC_ROOT

hobbiesurlpatterns = patterns(
    '',
    # HOBBY INDEX
    url(
        r'^$',
        'hobbies.views.hobby_index',
        name='hobby_index',
    ),

    # GENERIC INDEX
    url(
        r'^(?P<hobbytype>[\w-]+)/$',
        'hobbies.views.type_index',
        name='type_index',
    ),

    # GENERIC OBJECT
    url(
        r'^(?P<hobbytype>[\w-]+)/(?P<hobbytitle>[\w-]+)/$',
        'hobbies.views.type_item',
        name='type_item',
    ),
)

handler404 = 'harshp.views.handler404'
handler500 = 'harshp.views.handler500'

urlpatterns = patterns(
    '',
    url(r'', include(hobbiesurlpatterns, namespace='hobbies')),
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

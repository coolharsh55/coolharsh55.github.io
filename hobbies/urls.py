"""urls for hobbies

    book_index, book
    movie_index, movie
    tvshow_index, tvshow
    game_index, game
"""

from django.conf.urls import patterns, include, url

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

urlpatterns = patterns(
    '',
    url(r'', include(hobbiesurlpatterns, namespace='hobbies')),
)

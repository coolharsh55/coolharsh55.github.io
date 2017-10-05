"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

movie_urlpatterns = [
    url(r'^$', views.movie_homepage, name='index'),
    url(r'^lists/(?P<slug>[\w-]+)/$', views.movie_list, name='list'),
    url(r'^watchlist/$', views.watchlist, name='watchlist'),
]

books_urlpatterns = [
    url(r'^$', views.books_homepage, name='index'),
    url(r'^lists/(?P<slug>[\w-]+)/$', views.book_list, name='list'),
]

videogame_urlpatterns = [
    url(r'^$', views.videogame_homepage, name='index'),
    # url(r'^lists/(?P<slug>[\w-]+)/$', views.videogame_list, name='list'),
    # url(r'^gamelist/$', views.gamelist, name='gamelist'),
]

music_urlpatterns = [
    url(r'^$', views.music_homepage, name='index'),
    # url(r'^lists/(?P<slug>[\w-]+)/$', views.music_list, name='list'),
    # url(r'^playlist/$', views.playlist, name='playlist'),
]

photography_urlpatterns = [
    url(r'^$', views.photography_homepage, name='index'),
    # url(r'^lists/(?P<slug>[\w-]+)/$', views.photography_list, name='list'),
    # url(r'^photoshootlist/$', views.watchlist, name='watchlist'),
]

origami_urlpatterns = [
    url(r'^$', views.origami_homepage, name='index'),
    # url(r'^lists/(?P<slug>[\w-]+)/$', views.origami_list, name='list'),
    # url(r'^craftlist/$', views.craftlist, name='craftlist'),
]

teacoffee_urlpatterns = [
    url(r'^$', views.teacoffee_homepage, name='index'),
    # url(r'^lists/(?P<slug>[\w-]+)/$', views.teacoffee_list, name='list'),
    # url(r'^drinklist/$', views.drinklist, name='drinklist'),
]

polymathy_urlpatterns = [
    url(r'^$', views.polymathy_homepage, name='index'),
    # url(r'^lists/(?P<slug>[\w-]+)/$', views.polymathy_list, name='list'),
    # url(r'^learnlist/$', views.learnlist, name='learnlist'),
]

hobbies_urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^movies/', include(movie_urlpatterns, namespace='movies')),
    url(r'^books/', include(books_urlpatterns, namespace='books')),
    url(r'^videogames/',
        include(videogame_urlpatterns, namespace='videogames')),
    url(r'^music/', include(music_urlpatterns, namespace='music')),
    url(r'^photography/',
        include(photography_urlpatterns, namespace='photography')),
    url(r'^origami/', include(origami_urlpatterns, namespace='origami')),
    url(r'^teacoffee/', include(teacoffee_urlpatterns, namespace='teacoffee')),
    url(r'^polymathy/', include(polymathy_urlpatterns, namespace='polymathy')),
]

urlpatterns = [
    url(r'', include(hobbies_urlpatterns, namespace='hobbies')),
]

handler404 = 'harshp_com.views.handler404'

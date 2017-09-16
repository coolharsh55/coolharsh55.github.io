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
]

videogame_urlpatterns = [
    url(r'^$', views.videogame_homepage, name='index'),
]

music_urlpatterns = [
    url(r'^$', views.music_homepage, name='index'),
]

photography_urlpatterns = [
    url(r'^$', views.photography_homepage, name='index'),
]

origami_urlpatterns = [
    url(r'^$', views.origami_homepage, name='index'),
]

teacoffee_urlpatterns = [
    url(r'^$', views.teacoffee_homepage, name='index'),
]

polymathy_urlpatterns = [
    url(r'^$', views.polymathy_homepage, name='index'),
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

"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

movie_urlpatterns = [
    url(r'^$', views.movie_homepage, name='index'),
    url(r'^lists/(?P<slug>[\w-]+)/$', views.movie_list, name='list')
]

hobbies_urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^movies/', include(movie_urlpatterns, namespace='movies'))
]

urlpatterns = [
    url(r'', include(hobbies_urlpatterns, namespace='hobbies')),
]

handler404 = 'harshp_com.views.handler404'

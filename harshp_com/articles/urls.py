"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

articles_urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^series/$', views.series_list, name='series-list'),
    url(r'^series/(?P<series_slug>[\w-]+)/$', views.series, name='series'),
    url(
        r'^series/(?P<series_slug>[\w-]+)/(?P<slug>[\w-]+)/$',
        views.series_post, name='article'),
    url(r'^post/(?P<slug>[\w-]+)/$', views.post, name='article'),
]

urlpatterns = [
    url(r'', include('harshp_com.urls_commons')),
    url(r'', include(articles_urlpatterns, namespace='articles')),
]

handler404 = 'harshp_com.views.handler404'

"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

stories_urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^series/$', views.series_list, name='series-list'),
    url(r'^series/(?P<slug>[\w-]+)/$', views.series, name='series'),
    url(
        r'^series/(?P<slug_series>[\w-]+)/(?P<slug_story>[\w-]+)/$',
        views.series_story, name='story'),
    url(r'^story/(?P<slug>[\w-]+)/$', views.story, name='story'),
]

urlpatterns = [
    url(r'', include('harshp_com.urls_commons')),
    url(r'', include(stories_urlpatterns, namespace='stories')),
]

handler404 = 'harshp_com.views.handler404'

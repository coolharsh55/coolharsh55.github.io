"""urls config for poems at harshp_com"""

from django.conf.urls import include, url

from . import views

poems_urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^(?P<slug>[\w-]+)/$', views.poem, name='poem'),
]

urlpatterns = [
    url(r'', include('harshp_com.urls_commons')),
    url(r'', include(poems_urlpatterns, namespace='poems')),
]

handler404 = 'harshp_com.views.handler404'

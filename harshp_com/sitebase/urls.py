"""sitebase urls for harshp_com"""

from django.conf.urls import include, url

from . import views

tag_urlpatterns = [
    url(r'^tags/$', views.tags, name='list'),
    url(r'^tags/(?P<tag>[\w-]+)/$', views.tag, name='get'),
]

author_urlpatterns = [
    url(r'^authors/$', views.authors, name='list'),
    url(r'^authors/(?P<author>[\w-]+)/$', views.author, name='get'),
]

sitebase_urlpatterns = [
    url(r'', include(tag_urlpatterns, namespace='tags')),
    url(r'', include(author_urlpatterns, namespace='authors')),
]

urlpatterns = [
    url(r'', include(sitebase_urlpatterns, namespace='sitebase')),
]

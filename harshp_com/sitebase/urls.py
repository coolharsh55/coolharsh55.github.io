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

feedback_urlpatterns = [
    url(r'^$', views.feedbacks, name='list'),
    url(r'^add/(?P<url>.+)/$', views.feedback_add, name='add'),
    url(r'^(?P<pk>\d+)/$', views.feedback_view, name='view'),
]

sitebase_urlpatterns = [
    url(r'', include(tag_urlpatterns, namespace='tags')),
    url(r'', include(author_urlpatterns, namespace='authors')),
]

urlpatterns = [
    url(r'', include(sitebase_urlpatterns, namespace='sitebase')),
    url(r'feedback/', include(feedback_urlpatterns, namespace='feedback')),
]

handler404 = 'harshp_com.views.handler404'

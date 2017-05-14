"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

brainbank_urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^ideas/$', views.ideas, name='ideas'),
    url(
        r'^ideas/posts/highlighted/$',
        views.highlighted, name='highlighted'),
    url(
        r'^ideas/posts/deliverables/$',
        views.deliverables, name='deliverables'),
    url(r'^ideas/(?P<slug>[\w-]+)/$', views.idea, name='idea'),
    url(
        r'^ideas/(?P<idea_slug>[\w-]+)/(?P<slug>[\w-]+)/$',
        views.post, name='post'),
]

urlpatterns = [
    url(r'', include(brainbank_urlpatterns, namespace='brainbank')),
]

handler404 = 'harshp_com.views.handler404'

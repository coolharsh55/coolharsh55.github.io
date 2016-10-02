"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

tag_urlpatterns = [
    url(r'^$', views.tags, name='list'),
    url(r'^(?P<slug>[\w-]+)/$', views.tag, name='get'),
]

entries_urlpatterns = [
    url(r'^$', views.entries, name='list'),
    url(r'^(?P<entry_id>[\d]+)/$', views.entry, name='get'),
    # TODO: filter by year, month, date
    # TODO: filter by custom range
]

section_urlpatterns = [
    url(r'^$', views.sections, name='list'),
    url(r'^(?P<slug>[\w-]+)/$', views.section, name='get'),
]

journal_urlpatterns = [
    url(r'^$', views.auth, name='auth'),
    url(r'^tags/', include(tag_urlpatterns, namespace='tags')),
    url(r'^entries/', include(entries_urlpatterns, namespace='entries')),
    url(r'^sections/', include(section_urlpatterns, namespace='sections')),
    url(r'logout/$', views.logout_user, name='logout'),
]

urlpatterns = [
    url(r'', include('harshp_com.urls_commons')),
    url(r'', include(journal_urlpatterns, namespace='journal')),
]

handler404 = 'harshp_com.views.handler404'

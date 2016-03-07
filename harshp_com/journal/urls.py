"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

journal_urlpatterns = [
    url(r'^$', views.list, name='list'),
]

urlpatterns = [
    url(r'', include(journal_urlpatterns, namespace='journal')),
]

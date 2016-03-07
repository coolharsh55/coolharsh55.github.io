"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

brainbank_urlpatterns = [
    url(r'^$', views.list, name='list'),
]

urlpatterns = [
    url(r'', include(brainbank_urlpatterns, namespace='brainbank')),
]

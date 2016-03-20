"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

research_urlpatterns = [
    url(r'^$', views.home, name='home'),
]

urlpatterns = [
    url(r'', include('harshp_com.urls_commons')),
    url(r'', include(research_urlpatterns, namespace='research')),
]

"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

friends_urlpatterns = [
    url(r'^$', views.home, name='home'),
]

urlpatterns = [
    url(r'', include('harshp_com.urls_commons')),
    url(r'', include(friends_urlpatterns, namespace='friends')),
]

handler404 = 'harshp_com.views.handler404'

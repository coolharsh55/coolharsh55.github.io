"""urls for me section at harshp_com"""

from django.conf.urls import include, url

from . import views

me_urlspatterns = [
    url(r'^$', views.homepage, name='home'),
]

urlpatterns = [
    url(r'', include(me_urlspatterns, namespace='me')),
]

handler404 = 'harshp_com.views.handler404'

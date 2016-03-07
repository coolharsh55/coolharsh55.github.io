"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

lifeX_urlpatterns = [
    url(r'^$', views.home, name='home'),
]

urlpatterns = [
    url(r'', include(lifeX_urlpatterns, namespace='lifeX')),
]

"""urls for me section at harshp_com"""

from django.conf.urls import include, url

from . import views

me_urlspatterns = [

]

urlpatterns = [
    url(r'', include(me_urlspatterns, namespace='me')),
]

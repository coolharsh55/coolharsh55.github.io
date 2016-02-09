"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

blog_urlpatterns = [
    url(r'^$', views.test, name='test'),
]

urlpatterns = [
    url(r'', include(blog_urlpatterns, namespace='blog')),
]

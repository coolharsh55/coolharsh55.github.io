from django.conf.urls import url

from harshp_com import views

urlpatterns = [
    # stub
    url(r'^stub/$', views.stub, name='stub'),
    url(r'^privacy-policy/$', views.privacy_policy, name='privacy-policy'),
]

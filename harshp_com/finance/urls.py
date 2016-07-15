"""urls config for finance at harshp_com"""

from django.conf.urls import include, url

from . import views

finance_urlspatterns = [

]

urlpatterns = [
    url(r'', include('harshp_com.urls_commons')),
    url(r'', include(finance_urlspatterns, namespace='finance')),
]

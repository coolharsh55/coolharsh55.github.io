"""admin urls for harshp_com"""

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', admin.site.urls),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
]

handler404 = 'harshp_com.views.handler404'

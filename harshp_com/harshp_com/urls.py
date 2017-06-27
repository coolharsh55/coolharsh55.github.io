"""harshp_com URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    # base
    url(r'^$', views.home, name='home'),
    # stub
    url(r'^stub/$', views.stub, name='stub'),
    url(r'^contact/$', views.contact, name='contact'),
    # admin
    url(r'^manage/jobs/', include('django_rq.urls')),
    url(r'^manage/', admin.site.urls),
    # url(r'^jet/', include('jet.urls', 'jet')),
    # url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    # robots.txt
    url(r'^robots\.txt', include('robots.urls')),

    # sitebase
    url(r'', include('sitebase.urls')),

    # apps
    url(r'^blog/lifeX/', include('lifeX.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^brainbank/', include('brainbank.urls')),
    url(r'^dev/', include('dev.urls')),
    url(r'^hobbies/', include('hobbies.urls')),
    url(r'^personal/finance/', include('finance.urls')),
    url(r'^personal/journal/', include('journal.urls')),
    url(r'^me/', include('me.urls')),
    url(r'^poems/', include('poems.urls')),
    url(r'^research/', include('research.urls')),
    url(r'^stories/', include('stories.urls')),

    # custom
    url(r'^errors/404', views.handler404),
    url(r'^errors/500', views.handler500),
]

admin.site.site_name = 'harshp_com'
handler404 = views.handler404
handler500 = views.handler500


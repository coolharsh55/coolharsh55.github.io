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
    # commons
    url(r'^$', views.home, name='home'),
    url(r'', include('harshp_com.urls_commons')),

    # admin
    url(r'', include('harshp_com.adminurls')),

    # filer
    url(r'^filer/', include('filer.urls')),
    # robots.txt
    url(r'^robots\.txt', include('robots.urls')),

    # sitebase
    url(r'', include('sitebase.urls')),

    # apps
    url(r'', include('articles.urls')),
    url(r'', include('blog.urls')),
    url(r'', include('lifeX.urls')),
    url(r'', include('me.urls')),
    url(r'', include('poems.urls')),
    url(r'', include('stories.urls')),

]

admin.site.site_name = 'harshp_com'

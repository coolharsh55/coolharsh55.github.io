"""urls for admin
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    # admin
    url(
        r'^ckeditor/',
        include('ckeditor.urls')
    ),
    url(
        r'^redactor/',
        include('redactor.urls')
    ),
    url(
        r'^doc/',
        include('django.contrib.admindocs.urls')
    ),
    url(
        r'^',
        include(admin.site.urls)
    ),
)

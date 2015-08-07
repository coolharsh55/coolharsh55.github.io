"""urls for sitedata
"""

from django.conf.urls import patterns, include, url

sitedataurlpatterns = patterns(
    '',
    # TAG INDEX
    url(
        r'^$',
        'sitedata.views.tag_index',
        name='tag_index'
    ),

    # TAG
    url(
        r'^(?P<tagname>[\w-]+)/$',
        'sitedata.views.tag',
        name='tagname'
    ),
)

urlpatterns = patterns(
    '',
    url(r'', include(sitedataurlpatterns, namespace='sitedata')),
)

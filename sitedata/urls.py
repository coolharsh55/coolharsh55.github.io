"""urls for sitedata
"""

from django.conf.urls import patterns, include, url

sitedataurlpatterns = patterns(
    '',
    # TAG INDEX
    url(
        r'^tags/$',
        'sitedata.views.tag_index',
        name='tag_index',
    ),

    # TAG
    url(
        r'^tags/(?P<tagname>[\w-]+)/$',
        'sitedata.views.tag',
        name='tagname',
    ),

    # FEEDBACK INDEX
    url(
        r'^feedback/$',
        'sitedata.views.feedback_index',
        name='feedback_index',
    ),

    # FEEDBACK
    url(
        r'^feedback/(?P<feedback_no>[\d]+)/$',
        'sitedata.views.feedback',
        name='feedback',
    ),

    # ADD FEEDBACK
    url(
        r'^feedback/add_new/(?P<url>.*|)/$',
        'sitedata.views.feedback_add',
        name='feedback_add',
    ),
)

urlpatterns = patterns(
    '',
    url(r'', include(sitedataurlpatterns, namespace='sitedata')),
)

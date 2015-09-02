"""urls for sitedata
"""

from django.conf.urls import patterns, include, url
from django.conf import settings
from harshp.settings.local import STATIC_ROOT

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
        r'^feedback/add_new/(?P<url>.*)$',
        'sitedata.views.feedback_add',
        name='feedback_add',
    ),
)

handler404 = 'harshp.views.handler404'
handler500 = 'harshp.views.handler500'

urlpatterns = patterns(
    '',
    url(r'', include(sitedataurlpatterns, namespace='sitedata')),
)

# if DEBUG is True it will be served automatically
if settings.DEBUG is False and settings.MODE == 'local':
    urlpatterns += patterns(
        '',
        url(
            r'^static/(?P<path>.*)$',
            'django.views.static.serve',
            {
                'document_root': STATIC_ROOT
            }
        ),
    )

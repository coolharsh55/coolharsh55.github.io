"""urls for brainbank
"""

from django.conf.urls import patterns, include, url
from django.conf import settings
from harshp.settings.local import STATIC_ROOT

brainbankurlpatterns = patterns(
    '',
    # INDEX
    url(
        r'^$',
        'brainbank.views.index',
        name='index'
    ),

    # IDEA
    url(
        r'^(?P<idea>[\w-]+)/$',
        'brainbank.views.brainbank_idea',
        name='idea'
    ),

    # DEMO
    url(
        r'^(?P<idea>[\w-]+)/demo-(?P<demo>[\w-]+)/$',
        'brainbank.views.brainbank_demo',
        name='demo'
    ),

    # POST
    url(
        r'^(?P<idea>[\w-]+)/(?P<post>[\w-]+)/$',
        'brainbank.views.brainbank_post',
        name='post'
    ),
)

handler404 = 'harshp.views.handler404'
handler500 = 'harshp.views.handler500'

urlpatterns = patterns(
    '',
    url(r'', include(brainbankurlpatterns, namespace='brainbank')),
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

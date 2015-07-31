"""urls for brainbank
"""

from django.conf.urls import patterns, include, url

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

urlpatterns = patterns(
    '',
    url(r'', include(brainbankurlpatterns, namespace='brainbank')),
)

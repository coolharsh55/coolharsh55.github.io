"""urls for lifeX
"""

from django.conf.urls import patterns, include, url

lifeXurlpatterns = patterns(
    '',

    # lifeX index
    url(
        r'^$',
        'lifeX.views.index',
        name='index'
    ),

    # PRESENTATION
    url(
        r'^presentation/UCC2014/$',
        'lifeX.views.presentation',
        name='lifeX_presentation_UCC2014'
    ),

    # IDEAS
    # all ideas
    url(
        r'^ideas/$',
        'lifeX.views.ideas',
        name='ideas'
    ),
    # category
    url(
        r'^ideas/(?P<category>[\w-]+)/$',
        'lifeX.views.category',
        name='category'
    ),
    # idea
    url(
        r'^ideas/(?P<category>[\w-]+)/(?P<idea>[\w-]+)/$',
        'lifeX.views.idea',
        name='idea'
    ),

    # EXPERIMENTS
    # all experiments weeks
    url(
        r'^experiments/$',
        'lifeX.views.experiments', name='experiments'),
    # experiment week
    url(
        r'^experiments/week(?P<week>[0-9]+)/$',
        'lifeX.views.week',
        name='week'
    ),
    # experiment post
    url(
        r'^experiments/week(?P<week>[0-9]+)/(?P<idea>[\w-]+)/$',
        'lifeX.views.post',
        name='post'
    ),

    # BLOG
    # all blog posts
    url(
        r'^blog/$',
        'lifeX.views.blog',
        name='blog'
    ),
    # blog post
    url(
        r'^blog/(?P<blogpost>[\w-]+)/$',
        'lifeX.views.blogpost',
        name='blogpost'
    ),
)

urlpatterns = patterns(
    '',
    url(r'', include(lifeXurlpatterns, namespace='lifeX')),
)

"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

ideas_urlpatterns = [
    # categories and ideas
    url(r'^$', views.ideas_list, name='list'),
    url(r'^categories/(?P<slug>[\w-]+)/$', views.category, name='category'),
    url(
        r'^categories/(?P<category_slug>[\w-]+)/'
        '(?P<slug>[\w-]+)/$',
        views.idea, name='idea'),
]

experiments_urlpatterns = [
    # weeks and experiments
    url(r'^$', views.experiments_list, name='list'),
    url(r'^week-(?P<number>[\d]+)/$', views.week, name='week'),
    url(
        r'^week-(?P<number>[\d]+)/(?P<slug>[\w-]+)/$',
        views.experiment, name='experiment'),
]

goals_urlpatterns = [
    # goals
    url(r'^$', views.goals, name='list'),
]

blog_urlpatterns = [
    # blog
    url(r'^$', views.blog_list, name='list'),
    url(r'^(?P<slug>[\w-]+)/$', views.blogpost, name='post'),
]

presentation_urlpatterns = [
    # presentation
    url(
        r'UCC2014/$',
        views.presentation_ucc2014, name='UCC2014')
]

lifeX_urlpatterns = [
    # home
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about_lifex, name='about'),
    url(r'ideas/', include(ideas_urlpatterns, namespace='ideas')),
    url(
        r'experiments/',
        include(experiments_urlpatterns, namespace='experiments')),
    url(r'goals/', include(goals_urlpatterns, namespace='goals')),
    url(r'blog/', include(blog_urlpatterns, namespace='blog')),
    url(
        r'presentation/',
        include(presentation_urlpatterns, namespace='presentation')),
]

urlpatterns = [
    url(r'', include('harshp_com.urls_commons')),
    url(r'', include(lifeX_urlpatterns, namespace='lifeX')),
]

handler404 = 'harshp_com.views.handler404'

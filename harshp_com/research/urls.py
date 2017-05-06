"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

phd_urlpatterns = [
    url(r'^$', views.phd_home, name='home'),
    url(r'^directed-study/$', views.phd_directed_study, name='directed-study')
]

msc_urlpatterns = [
    url(r'^$', views.msc_home, name='home')
]

b_engg_urlpatterns = [
    url(r'^$', views.b_engg_home, name='home')
]

blog_urlpatterns = [
    url(r'^$', views.blog_home, name='home'),
    # url(r'^featured/$', views.blog_featured, name='featured'),
    # url(r'^series/$', views.blog_series_list, name='series-list'),
    url(r'^series/(?P<series>[\w-]+)/$', views.blog_series, name='series'),
    url(
        r'^series/(?P<series>[\w-]+)/(?P<post>[\w-]+)/$',
        views.blog_post, name='post'),
]

research_urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^publications/$', views.publications, name='publications'),
    url(r'^interests/$', views.interests, name='interests'),
    url(r'^phd/', include(phd_urlpatterns, namespace='phd')),
    url(r'^msc/', include(msc_urlpatterns, namespace='msc')),
    url(r'^b-engg/', include(b_engg_urlpatterns, namespace='b-engg')),
    url(r'^blog/', include(blog_urlpatterns, namespace='blog')),
]

urlpatterns = [
    url(r'', include('harshp_com.urls_commons')),
    url(r'', include(research_urlpatterns, namespace='research')),
]

handler404 = 'harshp_com.views.handler404'

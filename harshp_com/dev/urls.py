"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from .views import guides_tutorials
from .views import resources
from .views import discussions
from .views import mystack
from .views import projects
from .views import base


guides_tutorials_urlpatterns =[
     # guides and tutorials
    url(r'', guides_tutorials.index, name='index'),
    url(
        r'^(?P<section>[\w-]+)/$', 
        guides_tutorials.dev_section, name='section'),
    url(
        r'^(?P<section>[\w-]+)/(?P<post>[\w-]+)/$', 
        guides_tutorials.dev_post, name='post'),
]

resources_urlpatterns =[
     # resources
    url(r'', resources.index, name='index'),
    url(
        r'^(?P<section>[\w-]+)/$', 
        resources.dev_section, name='section'),
    url(
        r'^(?P<section>[\w-]+)/(?P<post>[\w-]+)/$', 
        resources.dev_post, name='post'),
]

discussions_urlpatterns =[
     # discussions
    url(r'', discussions.index, name='index'),
    url(
        r'^(?P<section>[\w-]+)/$', 
        discussions.dev_section, name='section'),
    url(
        r'^(?P<section>[\w-]+)/(?P<post>[\w-]+)/$', 
        discussions.dev_post, name='post'),
]

mystack_urlpatterns =[
     # my stack
    url(r'', mystack.index, name='index'),
    url(
        r'^(?P<section>[\w-]+)/$', 
        mystack.dev_section, name='section'),
    url(
        r'^(?P<section>[\w-]+)/(?P<post>[\w-]+)/$', 
        mystack.dev_post, name='post'),
]

projects_urlpatterns =[
     # projects
    url(r'', projects.index, name='index'),
    url(
        r'^(?P<section>[\w-]+)/$', 
        projects.dev_section, name='section'),
    url(
        r'^(?P<section>[\w-]+)/(?P<post>[\w-]+)/$', 
        projects.dev_post, name='post'),
]

dev_urlpatterns = [
    # homepage
    url(r'^$', base.index, name='index'),
    url(
        r'^guides_tutorials/', include(guides_tutorials_urlpatterns, 
        namespace='guides_tutorials')),
    url(
        r'^resources/', include(resources_urlpatterns, 
        namespace='resources')),
    url(
        r'^discussions/', include(discussions_urlpatterns, 
        namespace='discussions')),
    url(
        r'^mystack/', include(mystack_urlpatterns, 
        namespace='mystack')),
    url(
        r'^projects/', include(projects, 
        namespace='projects')),
]

urlpatterns = [
    url(r'', include(dev_urlpatterns, namespace='dev')),
]

handler404 = 'harshp_com.handler404'

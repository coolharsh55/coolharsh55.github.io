"""urls for friends
"""

from django.conf.urls import patterns, include, url

friendsurlpatterns = patterns(
    '',
    url(
        r'^supriya_chavan/birthdays/2015$',
        'friends.views.sup_bday_2015',
        name='sup_bday_2015'
    ),
)

urlpatterns = patterns(
    '',
    url(r'', include(friendsurlpatterns, namespace='friends')),
)

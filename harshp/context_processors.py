"""context processors
"""
from django.contrib.sites.models import Site
from django.utils.functional import SimpleLazyObject


def site(request):
    """get site object
    """
    return {
        'site': SimpleLazyObject(
            lambda: 'http://%s' % Site.objects.get_current_site().domain
        ),
    }

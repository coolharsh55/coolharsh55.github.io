from django.contrib.sites.models import Site
from django.contrib.sites.models import get_current_site
from django.utils.functional import SimpleLazyObject


def site(request):
  return { 'site': SimpleLazyObject(lambda: 'http://%s' % Site.objects.get_current().domain),
	}
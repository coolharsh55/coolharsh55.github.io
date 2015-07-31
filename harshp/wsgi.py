import sys

sys.path.append('/opt/bitnami/apps')
sys.path.append('/opt/bitnami/apps/django/django_projects/harshp.com')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

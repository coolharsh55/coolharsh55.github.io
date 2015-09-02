"""base config settings for harshp.com

"""

import os

from admin import *
from apps import *
from bootstrap import *
from editors import *
from filer import *
from logging import *
from middleware import *
from seo import *
from static import *
from subdomains import *
from templates import *
from timezone import *

SECRET_KEY = os.environ.get('HARSHP_SECRET_KEY', '')
WSGI_APPLICATION = 'harshp.wsgi.application'

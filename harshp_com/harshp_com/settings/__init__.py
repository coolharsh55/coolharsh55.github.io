"""settings module for harshp_com"""

DEBUG = True

from .admin import *
from .apps import *
from .auth import *
from .basepath import *
from .database import *
DATABASE = DATABASE_SQLITE
from .i18n import *
from .logging import *
from .middleware import *
from .static_media import *
from .templates import *
from .url_conf import *
from .wsgi import *

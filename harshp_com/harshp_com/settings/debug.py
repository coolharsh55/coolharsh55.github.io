"""debug settings for harshp_com"""

import os
MODE = os.environ.get('HARSHP_COM_MODE', 'dev')

if MODE == 'production':
    if os.environ.get('HARSHP_COM_DEBUG', None):
        DEBUG = False
    else:
        DEBUG = True
elif MODE == 'dev':
    DEBUG = True

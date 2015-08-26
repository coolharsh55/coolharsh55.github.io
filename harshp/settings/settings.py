"""settings for harshp.com

"""

import os
MODE = os.environ.get('HARSHP_MODE', 'local')

if MODE == 'prod':
    from prod import *
    # print 'production'
elif MODE == 'dev':
    from dev import *
    # print 'dev'
elif MODE == 'travis':
    from travis import *
else:
    from local import *
    # print 'local'

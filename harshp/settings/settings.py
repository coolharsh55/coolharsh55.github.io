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
elif MODE == 'dev_nodb':
    from dev_nodb import *
    # print 'dev_nodb'
elif MODE == 'dev_noaws':
    from dev_noaws import *
    # print 'dev_noaws'
elif MODE == 'travis':
    from travis import *
else:
    from local import *
    # print 'local'

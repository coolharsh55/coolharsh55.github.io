"""basepath for harshp_com project source"""

import os

BASE_DIR = (
    # harshp_com
    os.path.dirname(
        # harshp_com
        os.path.dirname(
            # settings
            os.path.dirname(
                # basepath.py
                os.path.abspath(__file__)))))

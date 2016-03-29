"""important lifeX dates"""

import arrow


def get_start_date():
    """return the lifeX start date"""
    return arrow.get(1395619200).datetime

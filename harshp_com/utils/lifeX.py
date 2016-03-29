"""utils for lifeX at harshp_com"""

from datetime import timedelta

from lifeX.dates import get_start_date


def week_dates(number):
    """return the week start and end dates for the given week"""

    # get the week
    # the week number is reduced by one
    # since we consider the starting week as week 1
    date_start = get_start_date() + timedelta(weeks=number - 1)
    date_end = date_start + timedelta(days=6)

    return date_start, date_end

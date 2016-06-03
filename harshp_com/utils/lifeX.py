"""utils for lifeX at harshp_com"""

import arrow
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


def update_weeks_to_now():
    """create lifeX weeks until current week"""
    # get difference between now and lifeX start date
    now = arrow.now()
    start = get_start_date()
    diff = (now - start)
    # get difference in weeks
    diff = diff.days / 7
    # round up the week to get current week no
    curr_week = int(diff + 0.5)

    # get number of lifeX weeks in database
    # import here to avoid circular imports
    # no harm, since imports can be resolved at runtime
    # and imports do not cause overheads if called again
    from lifeX.models import LifeXWeek
    no_weeks = LifeXWeek.objects.all().count()

    # add required number of lifeX weeks to database
    for count in range(no_weeks, curr_week + 1):
        LifeXWeek().save()

"""load dictionary in templates
"""
from django import template
from django.contrib.sites.models import Site
from django.utils import timezone

register = template.Library()


@register.filter(name='getval')
def getval(dict, key):
    """dictionary key-value
    """
    return dict.get(key)


@register.filter(name='reltime')
def reltime(post):
    """relative time from post publication
    """
    published = post.get('published')
    return get_rel_time(published)


@register.simple_tag
def current_domain():
    """get domain sitename
    """
    return 'http://%s' % Site.objects.get_current().domain


@register.filter
def get_rel_time(published):
    """get relative time for post
    """
    # time = timedelta(days=1000)
    time = timezone.now()
    # time = pytz.timezone('UTC').localize(time)
    time = (time - published)
    if time.days > 0:  # more than a day
        if time.days < 30:  # less than a month
            time = str(time.days) + " day(s) ago on "
            time += published.strftime('%d-%a')
        elif time.days // 30 <= 12:  # less than a year
            time = str(int(round(time.days / 30))) + " month(s) ago on "
            time += published.strftime('%d-%b')
        else:
            time = str(time.days / 365) + " year(s) ago on "
            time += published.strftime('%d-%b-%y')
    elif time.seconds > 6000:  # more than 100 min
        time = str(time.seconds // 6000) + " hour(s) ago on "
    else:  # less than 100 min
        time = str(time.seconds // 60) + " min(s) ago on "
    return time


@register.filter
def classname(obj):
    """get object classname
    """
    classname = obj.__class__.__name__
    return classname

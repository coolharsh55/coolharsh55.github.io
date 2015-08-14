"""views for sitedata
"""

from itertools import chain
from django.http import Http404
from django.shortcuts import render_to_response
from sitedata.models import Tag
# from sitedata.social_meta import create_meta


def tag_index(request):
    try:
        tags = Tag.objects.all()
        # for tag in tags:
        #     tagcount(tag)

    except Exception as e:
        print e
    return render_to_response(
        'sitedata/tagindex.html',
        {
            'tags': tags,
        },
    )


def tag(request, tagname):
    try:
        tag = Tag.objects.get(slug=tagname)
        links = tagcount(tag)
    except Tag.DoesNotExist:
        return Http404('Tag does not exist')
    return render_to_response(
        'sitedata/tag.html',
        {
            'tag': tag,
            'links': links,
        }
    )

"""
TAG LINKING TO POST
t = tag
ts = [getattr(t, s).all() for s in dir(t) if s.endswith('_set')]
itertools.chain(*ts)
"""


def tagcount(tag, sort=True):
    """count of tag linked objects
    """
    count = 0
    xitems = []
    items = []
    for x in Tag.__dict__:
        if x.endswith('_set'):
            # count += getattr(tag, x).count()
            xitems.append(getattr(tag, x))
    for x in xitems:
        print x
        items.append(x.order_by('-published'))
    print items
    links = []
    for item in items:
        if item:
            links.append((item, item[0].__class__.__name__))
    # setattr(tag, 'count', count)
    return links

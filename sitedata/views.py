"""views for sitedata
"""

from django.http import Http404
from django.shortcuts import render_to_response
from sitedata.models import Tag
# from sitedata.social_meta import create_meta


def tag_index(request):
    try:
        tags = Tag.objects.all()
        for tag in tags:
            tagcount(tag)

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
        use_count = tagcount(tag)
    except Tag.DoesNotExist:
        return Http404('Tag does not exist')
    return render_to_response(
        'sitedata/tag.html',
        {
            'tag': tag,
            'use_count': use_count,
        }
    )


def tagcount(tag, sort=True):
    """count of tag linked objects
    """
    count = []
    for x in Tag.__dict__:
        if x.endswith('_set'):
            count.append((x[:-4], getattr(tag, x).count(), getattr(tag, x)))
    if sort:
        count.sort(key=lambda x: x[0])
        count.sort(key=lambda x: x[1], reverse=True)
    setattr(tag, 'count', sum([i[1] for i in count]))
    return count

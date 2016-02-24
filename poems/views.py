"""view for poems
"""

from django.http import Http404
from django.shortcuts import render_to_response
from .models import Poem
from sitedata.social_meta import create_meta


def index(request):
    """Index view showing all poems

    Args:
        request(HttpRequest)

    Returns:
        HttpResponse: 200 on success, 404 otherwise

    Raises:
        Http404: poem not found
    """
    poemposts = Poem.objects.order_by('-published').values()
    title = 'poems at harshp.com'
    description = 'poems composed and dreamed up by me'
    keywords = ['poem', 'harshp.com', 'coolharsh55', ]
    url = request.build_absolute_uri()
    meta = create_meta(
        title,
        description,
        keywords,
        url
    )
    return render_to_response(
        'poems/index.html',
        {
            'posts': poemposts,
            'page_url': url,
            'meta': meta,
        }
    )


def poem(request, poem):
    """view poem post

    Args:
        request(HttpRequest)

    Returns:
        HttpResponse: 200 on success, 404 otherwise

    Raises:
        Http404: poem not found
    """
    try:
        poempost = Poem.objects.get(slug=poem)
    except Poem.DoesNotExist:
        raise Http404('Poem Post does not exist...')
    # contruct meta tags
    title = poempost.title
    description = 'A beautiful poem at harshp.com'
    keywords = ['poem', ]
    for tag in poempost.tags.all():
        keywords.append(tag.tagname)
    url = request.build_absolute_uri()
    meta = create_meta(
        title,
        description,
        keywords,
        url,
        poempost.headerimage
    )
    return render_to_response(
        'poems/poem.html',
        {
            'post': poempost,
            'page_url': url,
            'meta': meta,
        }
    )

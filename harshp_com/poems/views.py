from django.shortcuts import get_object_or_404
from django.shortcuts import render

from utils.meta_generator import create_meta

from .models import Poem


def list(request):
    poems_latest = Poem.objects.filter(is_published=True)\
        .order_by('-date_published')
    poems_featured = Poem.objects.filter(highlight=True, is_published=True)\
        .order_by('-date_published')
    poems_count = Poem.objects.filter(is_published=True).count()
    poems_featured_count = Poem.objects\
        .filter(highlight=True, is_published=True)\
        .count()
    meta = create_meta(
        title='poems.harshp.com',
        description='poems for harshp.com',
        keywords=['blog', 'poem', 'poetry', 'harshp.com', 'coolharsh55'],
        url=request.build_absolute_uri(),
    )
    return render(request, 'poems/homepage.html', {
        'meta': meta,
        'poems_all': poems_latest,
        'poems_count': poems_count,
        'poems_featured': poems_featured[:5],
        'poems_featured_count': poems_featured_count,
        'poems_latest': poems_latest[:5],
    })


def poem(request, slug):
    """return requested Poem"""

    poem_post = get_object_or_404(Poem, slug=slug)
    return render(request, 'poems/poem.html', {'poem': poem_post})

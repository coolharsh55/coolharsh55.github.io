from django.shortcuts import render
from itertools import chain

from utils.meta_generator import create_meta

from articles.models import Article
from blog.models import BlogPost
from poems.models import Poem
from stories.models import Story


def _get_latest(model):
    return model.objects\
        .filter(is_published=True)\
        .order_by('-date_published')


def _get_featured(model):
    return model.objects\
        .filter(is_published=True, highlight=True)\
        .order_by('-date_published')


def home(request):
    meta = create_meta(
        title='harshp.com',
        description='personal website & project',
        keywords=['harshp.com', 'coolharsh55'],
        url=request.build_absolute_uri(),
    )

    latest_posts = [
        (post.__class__.__name__, post) for post in
        sorted(
            chain(
                _get_latest(Article)[:5],
                _get_latest(BlogPost)[:5],
                _get_latest(Poem)[:5],
                _get_latest(Story)[:5]),
            reverse=True,
            key=lambda p: p.date_published)[:5]
    ]

    featured_posts = [
        (post.__class__.__name__, post) for post in
        sorted(
            chain(
                _get_featured(Article)[:5],
                _get_featured(BlogPost)[:5],
                _get_featured(Poem)[:5],
                _get_featured(Story)[:5]),
            reverse=True,
            key=lambda p: p.date_published)[:5]
    ]

    return render(
        request, 'sitebase/homepage.html',
        {
            'meta': meta,
            'latest_posts': latest_posts,
            'featured_posts': featured_posts,
        })


def stub(request):
    return render(request, 'sitebase/stub.html')

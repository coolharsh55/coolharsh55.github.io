from django.shortcuts import render
from django.template import RequestContext
from itertools import chain

from utils.meta_generator import create_meta

from articles.models import Article
from blog.models import BlogPost
from lifeX.models import LifeXWeek
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
                _get_latest(Article)[:10],
                _get_latest(BlogPost)[:10],
                _get_latest(Poem)[:10],
                _get_latest(Story)[:10]),
            reverse=True,
            key=lambda p: p.date_published)[:10]
    ]

    featured_posts = [
        (post.__class__.__name__, post) for post in
        sorted(
            chain(
                _get_featured(Article)[:10],
                _get_featured(BlogPost)[:10],
                _get_featured(Poem)[:10],
                _get_featured(Story)[:10]),
            reverse=True,
            key=lambda p: p.date_published)[:10]
    ]

    latest_week = latest_week = LifeXWeek.objects.order_by('-number').first()

    return render(
        request, 'sitebase/homepage.html',
        {
            'meta': meta,
            'latest_posts': latest_posts,
            'latest_week': latest_week,
            'featured_posts': featured_posts,
        })


def stub(request):
    return render(request, 'sitebase/stub.html')


def privacy_policy(request):
    return render(request, 'sitebase/privacypolicy.html')


def handler404(request):
    response = render(
        request, 'sitebase/404.html', {},
        context_instance=RequestContext(request))
    response.status_code = 404
    return response

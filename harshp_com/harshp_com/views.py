from django.shortcuts import render
from django.template import RequestContext
from itertools import chain
from datetime import datetime
from utils.meta_generator import create_meta

from blog.models import BlogPost
from lifeX.models import LifeXWeek
from poems.models import Poem
from stories.models import Story
from dev.models import DevPost
from research.models import ResearchBlogPost


def _get_latest(model, string, nos):
    items = model.objects\
        .filter(is_published=True)\
        .order_by('-date_published')[:nos]
    return [(string, item) for item in items]


def _get_featured(model, string, nos):
    items = model.objects\
        .filter(is_published=True, highlight=True)\
        .order_by('-date_published')
    return [(string, item) for item in items]


def home(request):
    meta = create_meta(
        title='harshp.com',
        description='personal website & project',
        keywords=['harshp.com', 'coolharsh55'],
        url=request.build_absolute_uri(),
    )

    latest_posts = sorted(
            chain(
                _get_latest(BlogPost, 'blog', 10),
                _get_latest(Poem, 'poem', 10),
                _get_latest(Story, 'story', 10),
                _get_latest(DevPost, 'dev', 10),
                _get_latest(ResearchBlogPost, 'research', 10),
                ),
            reverse=True,
            key=lambda p: p[1].date_published)[:10]

    featured_posts = sorted(
            chain(
                _get_featured(BlogPost, 'blog', 10),
                _get_featured(Poem, 'poem', 10),
                _get_featured(Story, 'story', 10),
                _get_featured(DevPost, 'dev', 10),
                _get_featured(ResearchBlogPost, 'research', 10),
                ),
            reverse=True,
            key=lambda p: p[1].date_published)[:10]

    latest_week = latest_week = LifeXWeek.objects.order_by('-number').first()
    now = datetime.now()

    return render(
        request, 'sitebase/homepage.html',
        {
            'meta': meta,
            'latest_posts': latest_posts,
            'latest_week': latest_week,
            'featured_posts': featured_posts,
            'current_financial_month': '{}/{}'.format(now.year, now.month)
        })


def stub(request):
    return render(request, 'sitebase/stub.html')


def contact(request):
    return render(request, 'sitebase/contact.html')


def privacy_policy(request):
    return render(request, 'sitebase/privacypolicy.html')


def handler404(request):
    response = render(request, 'sitebase/404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, 'sitebase/500.html', {})
    response.status_code = 500
    return response


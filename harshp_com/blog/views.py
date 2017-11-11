from django.shortcuts import get_object_or_404
from django.shortcuts import render

from utils.meta_generator import create_meta
from utils.pagecommons import pagecommon

from .models import BlogPost
from .models import BlogSeries


def list(request):
    posts_latest = BlogPost.objects.filter(is_published=True)\
        .order_by('-date_published').select_related('series')
    posts_featured = BlogPost.objects\
        .filter(highlight=True, is_published=True)\
        .order_by('-date_published').select_related('series')
    posts_featured_count = BlogPost.objects\
        .filter(highlight=True, is_published=True)\
        .order_by('-date_published').select_related('series').count()
    posts_count = BlogPost.objects.filter(is_published=True).count()
    series = BlogSeries.objects.all()
    series_count = BlogSeries.objects.all().count()
    meta = create_meta(
        title='blog.harshp.com',
        description='blog for harshp.com',
        keywords=['blog', 'harshp.com', 'coolharsh55'],
        url=request.build_absolute_uri(),
    )
    template_objects = {
        'meta': meta,
        'posts_all': posts_latest,
        'posts_count': posts_count,
        'posts_featured': posts_featured,
        'posts_featured_recent': posts_featured[:5],
        'posts_featured_count': posts_featured_count,
        'posts_latest': posts_latest[:5],
        'series_all': series,
        'series_count': series_count
    }
    pagecommon(request, template_objects)
    return render(request, 'blog/homepage.html', template_objects)


def featured(request):
    """return series list"""

    posts = BlogPost.objects.filter(highlight=True).select_related('series')
    template_objects = {
        'posts': posts
    }
    pagecommon(request, template_objects)
    return render(request, 'blog/featured.html', template_objects)


def series_list(request):
    """return series list"""

    series = [
        (s, s.blogpost_set.order_by('date_published'))
        for s in BlogSeries.objects.order_by('title')]
    template_objects = {'series': series}
    pagecommon(request, template_objects)
    return render(request, 'blog/series_list.html', template_objects)


def series(request, series):
    """return requested Blog Series"""

    series = get_object_or_404(BlogSeries, slug=series)
    template_objects = {
            'series': series,
            'posts': series.blogpost_set.order_by('-date_published')
        }
    pagecommon(request, template_objects)
    return render(
        request, 'blog/series.html', template_objects)


def series_post(request, series, post):
    """return requested Blog Post for Blog Series"""

    series = get_object_or_404(BlogSeries, slug=series)
    post = get_object_or_404(BlogPost, series=series, slug=post)
    template_objects = {'series': series, 'post': post}
    pagecommon(request, template_objects)
    return render(request, 'blog/series_post.html', template_objects)


def post(request, post):
    """return requested Blog Post"""

    post = get_object_or_404(BlogPost, series=None, slug=post)
    template_objects = {
        'meta': post.get_seo_meta(),
        'post': post}
    pagecommon(request, template_objects)
    return render(request, 'blog/post.html', template_objects)

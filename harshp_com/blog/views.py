from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse

from utils.meta_generator import create_meta

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
    return render(request, 'blog/homepage.html', {
        'meta': meta,
        'posts_all': posts_latest,
        'posts_count': posts_count,
        'posts_featured': posts_featured[:5],
        'posts_featured_count': posts_featured_count,
        'posts_latest': posts_latest[:5],
        'series_all': series[:5],
        'series_count': series_count})


def series_list(request):
    return HttpResponse('OK')


def series(request, series):
    """return requested Blog Series"""

    series = get_object_or_404(BlogSeries, slug=series)
    return render(request, 'blog/series.html', {'series': series})


def series_post(request, series, post):
    """return requested Blog Post for Blog Series"""

    series = get_object_or_404(BlogSeries, slug=series)
    post = get_object_or_404(BlogPost, series=series, slug=post)
    return render(request, 'blog/series_post.html', {
        'series': series, 'post': post})


def post(request, post):
    """return requested Blog Post"""

    post = get_object_or_404(BlogPost, series=None, slug=post)
    return render(request, 'blog/post.html', {
        'meta': post.get_seo_meta(),
        'post': post})

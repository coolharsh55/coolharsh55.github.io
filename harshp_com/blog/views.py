from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse

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
    return render(request, 'blog/homepage.html', {
        'posts_all': posts_latest,
        'posts_count': posts_count,
        'posts_featured': posts_featured[:10],
        'posts_featured_count': posts_featured_count,
        'posts_latest': posts_latest[:10],
        'series_all': series[:10],
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
    return render(request, 'blog/post.html', {'post': post})

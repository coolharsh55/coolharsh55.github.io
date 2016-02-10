from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse

from .models import BlogPost
from .models import BlogSeries


def list(request):
    return HttpResponse('OK')


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

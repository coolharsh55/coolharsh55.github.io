from django.http import Http404
from django.shortcuts import render

from .models import DevBlogPost
from .models import DevBlogSeries


def index(request):
    """index view for dev
    """
    return Http404('Not Implemented')


def blog_index(request):
    """index view for dev blog
    """
    posts = DevBlogPost.objects.all()
    return render(
        request,
        'devblog/blog_index.html',
        {
            'posts': posts,
        }
    )


def blog_post(request, blog_post):
    """view for dev blog post
    """
    try:
        post = DevBlogPost.objects.get(slug=blog_post)
    except DevBlogPost.DoesNotExist:
        raise Http404('dev blog does not exist')
    return render(
        request,
        'devblog/devblog.html',
        {
            'post': post,
        }
    )


def series_index(request):
    """index view for dev blog series
    """
    series = DevBlogSeries.objects.all()
    return render(
        request,
        'devblog/series_index.html',
        {
            'series': series,
        }
    )


def series_page(request, series):
    """page for dev blog series
    """
    try:
        series = DevBlogSeries.objects.get(slug=series)
    except DevBlogSeries.DoesNotExist:
        raise Http404('dev blog does not exist')
    return render(
        request,
        'devblog/devseries.html',
        {
            'series': series,
        }
    )

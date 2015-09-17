from django.http import Http404
from django.shortcuts import render

from .models import DevBlogPost
from .models import DevBlogSeries


def home(request):
    """homepage for dev

    shows all blog posts and series
    """
    posts = DevBlogPost.objects.filter(draft=False, future=None).order_by('-published')
    series = DevBlogSeries.objects.all()
    return render(
        request,
        'devblog/homepage.html',
        {
            'posts': posts,
            'series': series,
        }
    )


def blog_index(request):
    """index view for dev blog
    """
    posts = DevBlogPost.objects.filter(draft=False, future=None)
    return render(
        request,
        'devblog/blog_index.html',
        {
            'posts': posts,
        }
    )


def blog_post(request, series, blog_post):
    """view for dev blog post
    """
    try:
        if series == 'blog':
            series = None
        else:
            series = DevBlogSeries.objects.get(slug=series)
        post = DevBlogPost.objects.get(slug=blog_post, series=series)
    except DevBlogSeries.DoesNotExist:
        raise Http404('dev blog series does not exist')
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


def blog_series(request, series):
    """page for dev blog series
    """
    try:
        series = DevBlogSeries.objects.get(slug=series)
        posts = series.devblogpost_set.all()
        posts = sorted(posts, key=lambda obj: obj.published)
    except DevBlogSeries.DoesNotExist:
        raise Http404('dev blog does not exist')
    return render(
        request,
        'devblog/devseries.html',
        {
            'series': series,
            'posts': posts,
        }
    )

from django.shortcuts import get_object_or_404
from django.shortcuts import render

from utils.meta_generator import create_meta

from .models import Article
from .models import ArticleSeries


def list(request):
    posts_latest = Article.objects.filter(is_published=True)\
        .order_by('-date_published').select_related('series')
    posts_featured = Article.objects\
        .filter(highlight=True, is_published=True)\
        .order_by('-date_published').select_related('series')
    posts_featured_count = Article.objects\
        .filter(highlight=True, is_published=True)\
        .order_by('-date_published').select_related('series').count()
    posts_count = Article.objects.filter(is_published=True).count()
    series = ArticleSeries.objects.all()
    series_count = ArticleSeries.objects.all().count()
    meta = create_meta(
        title='articles.harshp.com',
        description='articles for harshp.com',
        keywords=['articles', 'harshp.com', 'coolharsh55'],
        url=request.build_absolute_uri(),
    )
    return render(request, 'articles/homepage.html', {
        'meta': meta,
        'posts_all': posts_latest,
        'posts_count': posts_count,
        'posts_featured': posts_featured,
        'posts_featured_recent': posts_featured[:5],
        'posts_featured_count': posts_featured_count,
        'posts_latest': posts_latest[:5],
        'series_all': series[:5],
        'series_count': series_count})


def series_list(request):
    series = [
        (s, s.articles_set.order_by('date_published'))
        for s in ArticleSeries.objects.order_by('title')]

    return render(request, 'article/series_list.html', {'series': series})


def series(request, series_slug):
    """return requested Blog Series"""

    series = get_object_or_404(ArticleSeries, slug=series_slug)
    return render(
        request, 'articles/series.html', {
            'series': series,
            'posts': series.article_set.order_by('-date_published')
        })


def series_post(request, series_slug, slug):
    """return requested Blog Post for Blog Series"""

    series = get_object_or_404(ArticleSeries, slug=series_slug)
    post = get_object_or_404(Article, series=series, slug=slug)
    return render(request, 'articles/series_post.html', {
        'series': series, 'post': post})


def post(request, slug):
    """return requested Blog Post"""

    post = get_object_or_404(Article, series=None, slug=slug)
    return render(request, 'articles/post.html', {
        'meta': post.get_seo_meta(),
        'post': post})

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse

from utils.meta_generator import create_meta

from .models import Story
from .models import StorySeries


def list(request):
    stories_latest = Story.objects.filter(is_published=True)\
        .order_by('-date_published').select_related('series')
    stories_featured = Story.objects\
        .filter(highlight=True, is_published=True)\
        .order_by('-date_published').select_related('series')
    stories_featured_count = Story.objects\
        .filter(highlight=True, is_published=True)\
        .order_by('-date_published').select_related('series').count()
    stories_count = Story.objects.filter(is_published=True).count()
    series = StorySeries.objects.all()
    series_count = StorySeries.objects.all().count()
    meta = create_meta(
        title='stories.harshp.com',
        description='stories at harshp.com',
        keywords=['stories', 'harshp.com', 'coolharsh55'],
        url=request.build_absolute_uri(),
    )
    return render(request, 'stories/homepage.html', {
        'meta': meta,
        'stories_all': stories_latest,
        'stories_count': stories_count,
        'stories_featured': stories_featured[:5],
        'stories_featured_count': stories_featured_count,
        'stories_latest': stories_latest[:5],
        'series_all': series[:5],
        'series_count': series_count})


def series_list(request):
    return HttpResponse('OK')


def series(request, series):
    """return requested Story Series"""

    series = get_object_or_404(StorySeries, slug=series)
    return render(request, 'stories/series.html', {'series': series})


def series_story(request, series, story):
    """return requested Story Story for Story Series"""

    series = get_object_or_404(StorySeries, slug=series)
    story = get_object_or_404(Story, series=series, slug=story)
    return render(request, 'stories/series_story.html', {
        'series': series, 'story': story})


def story(request, slug):
    """return requested Story Story"""

    story = get_object_or_404(Story, series=None, slug=slug)
    return render(request, 'stories/story.html', {
        'meta': story.get_seo_meta(),
        'story': story})
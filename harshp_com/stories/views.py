from django.shortcuts import get_object_or_404
from django.shortcuts import render

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
        'stories_featured': stories_featured,
        'stories_featured_recent': stories_featured[:5],
        'stories_featured_count': stories_featured_count,
        'stories_latest': stories_latest[:5],
        'series_all': series[:5],
        'series_count': series_count})


def series_list(request):
    series = [
        (s, s.story_set.order_by('date_published'))
        for s in StorySeries.objects.order_by('title')]

    return render(request, 'stories/series_list.html', {'series': series})


def series(request, slug):
    """return requested Story Series"""

    series_obj = get_object_or_404(StorySeries, slug=slug)
    return render(request, 'stories/series.html', {
        'series': series_obj,
        'stories': series_obj.story_set.order_by('-date_published')
        })


def series_story(request, slug_series, slug_story):
    """return requested Story Story for Story Series"""

    series_obj = get_object_or_404(StorySeries, slug=slug_series)
    story_obj = get_object_or_404(Story, series=series_obj, slug=slug_story)
    return render(request, 'stories/series_story.html', {
        'series': series_obj, 'story': story_obj})


def story(request, slug):
    """return requested Story Story"""

    story_obj = get_object_or_404(Story, series=None, slug=slug)
    return render(request, 'stories/story.html', {
        'meta': story_obj.get_seo_meta(),
        'story': story_obj})

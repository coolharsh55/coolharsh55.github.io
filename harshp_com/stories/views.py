from django.shortcuts import get_object_or_404
from django.shortcuts import render
from utils.pagecommons import pagecommon
from utils.meta_generator import create_meta

from .models import Story
from .models import StorySeries


def list(request):
    stories_all = Story.objects.filter(is_published=True)\
        .order_by('-date_published').select_related('series')
    meta = create_meta(
        title='stories.harshp.com',
        description='stories at harshp.com',
        keywords=['stories', 'harshp.com', 'coolharsh55'],
        url=request.build_absolute_uri(),
    )
    template_objects = {
        'meta': meta,
        'stories': stories_all,
    }
    pagecommon(request, template_objects)
    return render(request, 'stories/homepage.html', template_objects)


def series_list(request):
    series = [
        (s, s.story_set.order_by('date_published'))
        for s in StorySeries.objects.order_by('title')]
    template_objects = {'series': series}
    pagecommon(request, template_objects)
    return render(request, 'stories/series_list.html', template_objects)


def series(request, slug):
    """return requested Story Series"""

    series_obj = get_object_or_404(StorySeries, slug=slug)
    template_objects = {
        'series': series_obj,
        'stories': series_obj.story_set.order_by('-date_published')
        }
    pagecommon(request, template_objects)
    return render(request, 'stories/series.html', template_objects)


def series_story(request, slug_series, slug_story):
    """return requested Story Story for Story Series"""

    series_obj = get_object_or_404(StorySeries, slug=slug_series)
    story_obj = get_object_or_404(Story, series=series_obj, slug=slug_story)
    template_objects = {
        'series': series_obj, 'story': story_obj}
    pagecommon(request, template_objects)
    return render(request, 'stories/series_story.html', template_objects)


def story(request, slug):
    """return requested Story Story"""
    story_obj = get_object_or_404(Story, series=None, slug=slug)
    template_objects = {
        'meta': story_obj.get_seo_meta(),
        'story': story_obj,
        }
    pagecommon(request, template_objects)
    return render(request, 'stories/story.html', template_objects)

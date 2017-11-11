from django.shortcuts import get_object_or_404
from django.shortcuts import render
from utils.pagecommons import pagecommon
from .models import ResearchBlogSeries, ResearchBlogPost


def home(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'research/homepage.html', template_objects)


def publications(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'research/publications.html', template_objects)


def interests(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'research/interests.html', template_objects)


def phd_home(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'research/phd/homepage.html', template_objects)


def phd_directed_study(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(
        request, 'research/phd/directed_study.html', template_objects)


def msc_home(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'research/msc/homepage.html', template_objects)


def b_engg_home(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'research/b_engg/homepage.html', template_objects)


def blog_home(request):
    series = ResearchBlogSeries.objects.order_by('title')
    posts = ResearchBlogPost.objects\
        .filter(is_published=True).order_by('-date_published')
    template_objects = {
        'series': series,
        'posts': posts
        }
    pagecommon(request, template_objects)
    return render(request, 'research/blog/homepage.html', template_objects)


def blog_series(request, series):
    series = get_object_or_404(ResearchBlogSeries, slug=series)
    template_objects = {
        'series': series,
        'posts': series.researchblogpost_set.order_by('-date_published')
        }
    pagecommon(request, template_objects)
    return render(
        request, 'research/blog/series.html', template_objects)


def blog_post(request, series, post):
    series = get_object_or_404(ResearchBlogSeries, slug=series)
    post = get_object_or_404(ResearchBlogPost, series=series, slug=post)
    template_objects = {'post': post}
    pagecommon(request, template_objects)
    return render(request, 'research/blog/post.html', template_objects)

from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import LifeXIdea, LifeXCategory
from .models import LifeXWeek, LifeXExperiment
from .models import LifeXBlog


def home(request):
    latest_week = LifeXWeek.objects.order_by('number').first()
    print(latest_week.experiments.all())
    blogposts = LifeXBlog.objects.order_by('-date_published')[:5]
    return render(
        request, 'lifeX/homepage.html',
        {'latest_week': latest_week, 'blogposts': blogposts})


def about_lifex(request):
    return render(request, 'lifeX/about_lifeX.html')


def ideas_list(request):
    """list of all ideas grouped together by category"""

    categories = []

    for category in \
            LifeXCategory.objects\
            .order_by('name').prefetch_related('ideas'):
        categories.append(
            (category, sorted(category.ideas.all(), key=lambda i: i.title)))
    print(categories)

    return render(request, 'lifeX/ideas.html', {'categories': categories})


def category(request, slug):
    """category of lifeX idea"""
    category = get_object_or_404(LifeXCategory, slug=slug)
    return render(request, 'lifeX/category.html', {'category': category})


def idea(request, category_slug, slug):
    """lifeX idea"""
    idea = get_object_or_404(
        LifeXIdea, slug=slug, category__slug=category_slug)
    return render(request, 'lifeX/idea.html', {'idea': idea, 'rating': 3})


def experiments_list(request):
    """lifeX experiments ordered by weeks"""
    weeks = LifeXWeek.objects.order_by('-number')
    return render(request, 'lifeX/experiments.html', {'weeks': weeks})


def week(request, number):
    """lifeX experiment week"""
    week = get_object_or_404(LifeXWeek, number=number)
    return render(request, 'lifeX/week.html', {'week': week})


def experiment(request, number, slug):
    """lifeX experiment"""
    experiment = get_object_or_404(
        LifeXExperiment, slug=slug, week__number=number)
    return render(
        request, 'lifeX/experiment.html', {'experiment': experiment})


def blog_list(request):
    """lifeX blog"""
    posts = LifeXBlog.objects.order_by('date_published')

    return render(request, 'lifeX/blog_list.html', {'posts': posts})


def blogpost(request, slug):
    """lifeX blog post"""
    post = get_object_or_404(LifeXBlog, slug=slug)
    return render(request, 'lifeX/blog_post.html', {'post': post})


def presentation_ucc2014(request):
    """lifeX presentation given at UCC in 2014"""
    return render(request, 'lifeX/presentation_ucc2014.html')

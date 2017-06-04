from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.db.models.functions import Lower

from .models import BrainbankIdea, BrainbankPost


def list(request):
    data = [
        (series,
            series.posts.filter(is_published=True).order_by('-date_published'))
        for series in BrainbankIdea.objects.order_by('title')]
    return render(
        request, 'brainbank/homepage.html',
        {
            'data': data
        })


def idea(request, slug):
    idea = get_object_or_404(BrainbankIdea, slug=slug)
    posts = idea.posts.filter(is_published=True).order_by('-date_published')
    return render(
        request, 'brainbank/idea.html', {'idea': idea, 'posts': posts})


def post(request, idea_slug, slug):
    post = get_object_or_404(BrainbankPost, idea__slug=idea_slug, slug=slug)
    return render(
        request, 'brainbank/post.html',
        {
            'post': post,
        })

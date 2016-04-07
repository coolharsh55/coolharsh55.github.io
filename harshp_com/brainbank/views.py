from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.db.models.functions import Lower

from .models import BrainbankIdea, BrainbankPost


def list(request):
    latest_posts = BrainbankPost.objects.filter(
        is_published=True).order_by('-date_published')[:5]
    ideas = BrainbankIdea.objects.order_by('title')[:5]
    ideas_count = BrainbankIdea.objects.count()
    highlighted_posts = BrainbankPost.objects\
        .filter(is_published=True, highlight=True)\
        .order_by('-date_published')
    highlighted_posts_count = BrainbankPost.objects\
        .filter(is_published=True, highlight=True).count()
    deliverable_posts = BrainbankPost.objects\
        .filter(is_published=True, deliverable=True)\
        .order_by('-date_published')
    deliverable_posts_count = BrainbankPost.objects\
        .filter(is_published=True, deliverable=True).count()
    posts_all = BrainbankPost.objects.filter(
        is_published=True).order_by('-date_published')
    posts_count = BrainbankPost.objects.count()
    return render(
        request, 'brainbank/homepage.html',
        {
            'latest_posts': latest_posts,
            'ideas': ideas,
            'ideas_count': ideas_count,
            'highlighted_posts': highlighted_posts,
            'highlighted_posts_count': highlighted_posts_count,
            'deliverable_posts': deliverable_posts,
            'deliverable_posts_count': deliverable_posts_count,
            'posts_all': posts_all,
            'posts_count': posts_count,
        })


def ideas(request):
    ideas = [
        (
            b,
            b.posts.filter(is_published=True).order_by('-date_published'),
            b.posts.filter(is_published=True).count(),
            b.posts.filter(is_published=True, highlight=True).count(),
            b.posts.filter(is_published=True, deliverable=True).count())
        for b in BrainbankIdea.objects.order_by(Lower('title'))]

    return render(request, 'brainbank/ideas.html', {'ideas': ideas})


def idea(request, slug):
    try:
        idea = BrainbankIdea.objects.get(slug=slug)
        posts = idea.posts\
            .filter(is_published=True).order_by('-date_published')
        no_posts = idea.posts\
            .filter(is_published=True).order_by('-date_published').count()
        highlighted_posts = idea.posts\
            .filter(is_published=True, highlight=True)\
            .order_by('-date_published')
        no_highlited = highlighted_posts.count()
        deliverable_posts = idea.posts\
            .filter(is_published=True, deliverable=True)\
            .order_by('-date_published')
        no_deliverable = deliverable_posts.count()
    except BrainbankIdea.DoesNotExist:
        return Http404('Invalid Idea: No such idea exists.')
    return render(
        request, 'brainbank/idea.html',
        {
            'idea': idea,
            'posts': posts,
            'no_posts': no_posts,
            'highlighted': highlighted_posts,
            'no_highlited': no_highlited,
            'deliverables': deliverable_posts,
            'no_deliverable': no_deliverable,
        })


def highlighted(request):
    posts = BrainbankPost.objects\
        .filter(is_published=True, highlight=True)\
        .order_by('-date_published')
    return render(request, 'brainbank/highlighted.html', {'posts': posts})


def deliverables(request):
    posts = BrainbankPost.objects\
        .filter(is_published=True, deliverable=True)\
        .order_by('-date_published')
    return render(request, 'brainbank/deliverables.html', {'posts': posts})


def post(request, idea_slug, slug):
    post = get_object_or_404(BrainbankPost, idea__slug=idea_slug, slug=slug)
    idea = post.idea
    no_posts = idea.posts\
        .filter(is_published=True).order_by('-date_published').count()
    no_highlited = idea.posts\
        .filter(is_published=True, highlight=True)\
        .order_by('-date_published').count()
    no_deliverable = idea.posts\
        .filter(is_published=True, deliverable=True)\
        .order_by('-date_published').count()
    return render(
        request, 'brainbank/post.html',
        {
            'post': post,
            'idea': idea,
            'no_posts': no_posts,
            'no_highlited': no_highlited,
            'no_deliverable': no_deliverable,
        })

from collections import namedtuple
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import LifeXIdea, LifeXCategory
from .models import LifeXWeek, LifeXExperiment
from .models import LifeXGoal
from .models import LifeXBlog


def _goals_data():
    # Depth-first crawl over lifeX goals

    # each node in stack contains a goal and its json
    Node = namedtuple('Node', ['goal', 'json'])
    # get the root node - it has no parent
    root = LifeXGoal.objects.get(parent=None)
    # build it's json
    goal_json = {'name': root.title, 'children': []}
    # initialize the stack with the root node
    goal_stack = [Node(root, goal_json)]

    # keep going until stack has items
    while len(goal_stack) > 0:
        # pop node from stack
        node = goal_stack.pop()
        # if node has children, process them
        if node.goal.lifexgoal_set.all().count() > 0:
            for goal in node.goal.lifexgoal_set.all():
                # create new json dict to hold this goal
                json_dict = {'name': goal.title, 'children': []}
                # add children to node's json
                node.json['children'].append(json_dict)
                goal_stack.append(Node(goal, json_dict))

    return goal_json


def home(request):
    latest_week = LifeXWeek.objects.order_by('-number').first()
    blogposts = LifeXBlog.objects\
        .filter(is_published=True).order_by('-date_published')[:5]
    return render(
        request, 'lifeX/homepage.html', {
            'latest_week': latest_week,
            'blogposts': blogposts, 'goals': _goals_data()})


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


def goals(request):
    """lifeX goals"""
    return render(request, 'lifeX/goals.html', {'goals': _goals_data()})


def blog_list(request):
    """lifeX blog"""
    posts = LifeXBlog.objects\
        .filter(is_published=True).order_by('date_published')

    return render(request, 'lifeX/blog_list.html', {'posts': posts})


def blogpost(request, slug):
    """lifeX blog post"""
    post = get_object_or_404(LifeXBlog, slug=slug, is_published=True)
    return render(request, 'lifeX/blog_post.html', {'post': post})


def presentation_ucc2014(request):
    """lifeX presentation given at UCC in 2014"""
    return render(request, 'lifeX/presentation_UCC2014.html')

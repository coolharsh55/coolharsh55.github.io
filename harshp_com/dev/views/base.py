from django.shortcuts import get_object_or_404
from django.shortcuts import render

from utils.meta_generator import create_meta

from dev.models import DevSection
from dev.models import DevPost


def index(request):
    guides = DevSection.objects\
        .filter(section_type=DevSection.GUIDES_TUTORIALS)\
        .order_by('title')
    resources = DevSection.objects\
        .filter(section_type=DevSection.RESOURCES)\
        .order_by('title')
    discussions = DevSection.objects\
        .filter(section_type=DevSection.DISCUSSION)\
        .order_by('title')
    mystack = DevSection.objects\
        .filter(section_type=DevSection.MYSTACK)\
        .order_by('title')
    projects = DevSection.objects\
        .filter(section_type=DevSection.PROJECT)\
        .order_by('title')
    all_posts = DevPost.objects\
        .filter(is_published=True)\
        .order_by('-date_published')\
        .select_related('section')
    latest_posts = DevPost.objects\
        .filter(is_published=True)\
        .order_by('-date_published')[:10]
    return render(request, 'dev/homepage.html', {
        'guides': guides,
        'resources': resources,
        'discussions': discussions,
        'mystack': mystack,
        'projects': projects,
        'all_posts': all_posts,
        'latest_posts': latest_posts})

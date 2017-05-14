from django.shortcuts import get_object_or_404
from django.shortcuts import render

from utils.meta_generator import create_meta

from dev.models import DevSection
from dev.models import DevPost


def index(request):
    db_sections = DevSection.objects\
        .filter(section_type=DevSection.RESOURCES)\
        .order_by('title')
    # sections = [
    #     (section, section.devpost_set.count())
    #     for section in db_sections]
    posts = DevPost.objects\
        .filter(
            section__section_type=DevSection.RESOURCES, 
            is_published=True)\
        .order_by('-date_published')
    sections = {}
    for post in posts:
        if post.section not in sections:
            sections[post.section] = []
        sections[post.section].append(post)
    data = [(section, post) for section, post in sections.items()]

    meta = create_meta(
        title='Resources',
        description='Resources',
        keywords=[
            'guide', 'tutorials', 'how-to', 
            'harshp.com', 'coolharsh55'],
        url=request.build_absolute_uri())
    return render(request, 'dev/resources/index.html', {
        'meta': meta,
        'section_type_title': 'resources',
        # 'section_type_url': reverse('dev:res:index', subdomain='dev'),
        'data': data})


def dev_section(request, section): 
    section = get_object_or_404(
        DevSection, 
        slug=section, section_type=DevSection.RESOURCES)
    return render(request, 'dev/resources/section.html', {
        'section': section,
        'posts': section.devpost_set.order_by('-date_published'),
        'section_type': 'resources',
        # 'section_type_url': reverse('dev:res:index', subdomain='dev'),
        })


def dev_post(request, section, post):
    section = get_object_or_404(
        DevSection, 
        slug=section, section_type=DevSection.RESOURCES)
    post = get_object_or_404(
        DevPost, 
        slug=post, section=section, 
        section__section_type=DevSection.RESOURCES)
    return render(request, 'dev/resources/post.html', {
        'meta': post.get_seo_meta(),
        'section_type': 'resources',
        # 'section_type_url': reverse('dev:res:index', subdomain='dev'),
        'post': post,
        'section': section})

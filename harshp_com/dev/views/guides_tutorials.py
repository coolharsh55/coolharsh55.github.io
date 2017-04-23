from django.shortcuts import get_object_or_404
from django.shortcuts import render
from subdomains.utils import reverse

from utils.meta_generator import create_meta

from dev.models import DevSection
from dev.models import DevPost


def index(request):
    db_sections = DevSection.objects\
        .filter(section_type=DevSection.GUIDES_TUTORIALS)\
        .order_by('title')
    # sections = [
    #     (section, section.devpost_set.count())
    #     for section in db_sections]
    posts = DevPost.objects\
        .filter(
            section__section_type=DevSection.GUIDES_TUTORIALS, 
            is_published=True)\
        .order_by('-date_published')
    sections = {}
    for post in posts:
        if post.section not in sections:
            sections[post.section] = []
        sections[post.section].append(post)
    data = [(section, post) for section, post in sections.items()]

    meta = create_meta(
        title='Guides and Tutorials',
        description='Guides and Tutorials',
        keywords=[
            'guide', 'tutorials', 'how-to', 
            'harshp.com', 'coolharsh55'],
        url=request.build_absolute_uri())
    return render(request, 'dev/guides_tutorials/index.html', {
        'meta': meta,
        'section_type_title': 'guides & tutorials',
        'section_type_url': reverse('dev:guide:index', subdomain='dev'),
        'data': data})


def dev_section(request, section): 
    section = get_object_or_404(
        DevSection, 
        slug=section, section_type=DevSection.GUIDES_TUTORIALS)
    return render(request, 'dev/guides_tutorials/section.html', {
        'section': section,
        'posts': section.devpost_set.order_by('-date_published'),
        'section_type': 'guides & tutorials',
        'section_type_url': reverse('dev:guide:index', subdomain='dev'),
        })


def dev_post(request, section, post):
    section = get_object_or_404(
        DevSection, 
        slug=section, section_type=DevSection.GUIDES_TUTORIALS)
    post = get_object_or_404(
        DevPost, 
        slug=post, section=section, 
        section__section_type=DevSection.GUIDES_TUTORIALS)
    return render(request, 'dev/guides_tutorials/post.html', {
        'meta': post.get_seo_meta(),
        'section_type': 'guides & tutorials',
        'section_type_url': reverse('dev:guide:index', subdomain='dev'),
        'post': post,
        'section': section})

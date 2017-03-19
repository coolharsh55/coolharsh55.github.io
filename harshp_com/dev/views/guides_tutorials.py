from django.shortcuts import get_object_or_404
from django.shortcuts import render

from utils.meta_generator import create_meta

from dev.models import DevSection
from dev.models import DevPost


def index(request):
    db_sections = DevSection.objects\
        .filter(section_type=DevSection.GUIDES_TUTORIALS)\
        .order_by('title')\
        .select_related('post')
    sections = [
        (section, section.devpost_set.count())
        for section in db_sections]
    posts = DevPost.objects\
        .filter(
            section__section_type=DevSection.GUIDES_TUTORIALS, 
            is_published=True)\
        .order_by('-date_published')
    meta = create_meta(
        title='Guides and Tutorials',
        description='Guides and Tutorials',
        keywords=[
            'guide', 'tutorials', 'how-to', 
            'harshp.com', 'coolharsh55'],
        url=request.build_absolute_uri())
    return render(request, 'dev/guides_tutorials/index.html', {
        'meta': meta,
        'sections': sections,
        'posts': posts})


def dev_section(request, section): 
    section = get_object_or_404(
        DevSection, 
        slug=section, section_type=DevSection.GUIDES_TUTORIALS)
    return render(request, 'dev/guides_tutorials/section.html', {
        'section': section})


def dev_post(request, section, post):
    post = get_object_or_404(
        DevPost, 
        slug=post, section=section, 
        section__section_type=GUIDES_TUTORIALS)
    section = post.section
    return render(request, 'dev/guides_tutorials/post.html', {
        'meta': post.get_seo_meta(),
        'post': post,
        'section': section})

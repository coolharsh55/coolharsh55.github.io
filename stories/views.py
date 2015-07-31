"""views for stories
"""

from django.http import Http404
from django.shortcuts import render_to_response
from .models import StoryPost
from sitedata.social_meta import create_meta


def index(request, page=''):
    """index view to display all stories
    """
    try:
        storyposts = StoryPost.objects.order_by('-published').values()
        title = 'stories at harshp.com'
        description = 'stories written and dreamed up by me'
        keywords = ['stories', 'harshp.com', 'coolharsh55', ]
        url = request.build_absolute_uri()
        meta = create_meta(title, description, keywords, url)
    except StoryPost.DoesNotExist:
        raise Http404('Story does not exist...')

    return render_to_response(
        'stories/index.html',
        {
            'posts': storyposts,
            'page_url': url,
            'meta': meta,
        }
    )


def story(request, story):
    """view story
    """
    try:
        storypost = StoryPost.objects.get(slug=story)
        # contruct meta tags
        title = storypost.title
        description = 'An intriguing story at harshp.com'
        keywords = ['story', ]
        for tag in storypost.tags.all():
            keywords.append(tag.tagname)
        url = request.build_absolute_uri()
        meta = create_meta(
            title, description, keywords, url, storypost.headerimage)
    except StoryPost.DoesNotExist:
        raise Http404('Story does not exist...')

    return render_to_response(
        'stories/story.html',
        {
            'post': storypost,
            'page_url': url,
            'meta': meta,
        }
    )

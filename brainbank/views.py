"""views for brainbank
"""

from django.http import Http404
from django.shortcuts import render_to_response
from .models import BrainBankIdea
from .models import BrainBankPost
from .models import BrainBankDemo
from sitedata.social_meta import create_meta


# INDEX
def index(request):
    """Brainbank Index page
        Shows all available ideas ordered by date
        Shows all posts and demos associated with the idea

    Args:
        request(HttpRequest)

    Returns:
        HttpResponse: 200 on success, 404 otherwise

    Raises:
        Http404: brainbank idea does not exist
    """
    try:
        ideas = BrainBankIdea.objects.order_by('-published').all()
        title = 'brainbank at harshp.com'
        description = 'a brainbank of my ideas'
        keywords = ['idea', 'brainbank', 'harshp.com', 'coolharsh55', ]
        url = request.build_absolute_uri()
        meta = create_meta(
            title,
            description,
            keywords,
            url
        )
    except BrainBankIdea.DoesNotExist:
        raise Http404('Error loading Brainbank...')
    return render_to_response(
        'brainbank/index.html',
        {
            'ideas': ideas,
            'page_url': url,
            'meta': meta,
        }
    )


# IDEA
def brainbank_idea(request, idea):
    """Brainbank Idea page
    Shows information about the idea
    Shows all posts and demos associated with the idea

    Args:
        request(HttpRequest)
        idea(str): slug in url

    Returns:
        HttpResponse: 200 on success, 404 otherwise

    Raises:
        Http404: brainbank idea does not exist
    """
    try:
        idea = BrainBankIdea.objects.get(slug=idea)
        # contruct meta tags
        title = idea.title
        description = 'A brainbank idea at harshp.com'
        keywords = ['idea', 'brainbank', ]
        url = request.build_absolute_uri()
        meta = create_meta(
            title,
            description,
            keywords,
            url,
        )
    except BrainBankIdea.DoesNotExist:
        raise Http404('Brainbank Idea does not exist...')
    return render_to_response(
        'brainbank/idea.html',
        {
            'idea': idea,
            'page_url': url,
            'meta': meta,
        }
    )


# DEMO
def brainbank_demo(request, idea, demo):
    """Brainbank Demo for Idea
    Shows the demo with custom css and js
    Shows link to related idea

    Args:
        request(HttpRequest)
        idea(str): idea slug
        demo(str): demo slug

    Returns:
        HttpResponse: 200 on success, 404 otherwise

    Raises:
        Http404: brainbank demo does not exist
    """
    try:
        demo = BrainBankDemo.objects.get(slug=demo)
        # contruct meta tags
        title = demo.title
        description = 'A brainbank idea demo at harshp.com'
        keywords = ['brainbank', 'idea', 'demo', ]
        # for tag in demo.tags.all():
        # 	keywords.append(tag.tagname)
        url = request.build_absolute_uri()
        meta = create_meta(
            title,
            description,
            keywords,
            url,
        )
    except BrainBankDemo.DoesNotExist:
        raise Http404('Brainbank Idea Demo does not exist...')
    return render_to_response(
        'brainbank/demo.html',
        {
            'demo': demo,
            'page_url': url,
            'meta': meta,
        }
    )


# POST
def brainbank_post(request, idea, post):
    """
    Brainbank Post for Idea
    Shows a post with custom css and js
    Shows link to related idea
    Args:
        request(HttpRequest)
        idea(str): idea slug
        post(str): post slug

    Returns:
        HttpResponse: 200 on success, 404 otherwise

    Raises:
        Http404: brainbank post does not exist
    """
    try:
        post = BrainBankPost.objects.get(slug=post)
        # contruct meta tags
        title = post.title
        description = 'A brainbank idea post at harshp.com'
        keywords = ['brainbank', 'idea', 'post', ]
        for tag in post.tags.all():
            keywords.append(tag.tagname)
        url = request.build_absolute_uri()
        meta = create_meta(title, description, keywords, url,)
    except BrainBankPost.DoesNotExist:
        raise Http404('Brainbank Idea Post does not exist...')
    return render_to_response(
        'brainbank/post.html',
        {
            'post': post,
            'page_url': url,
            'meta': meta,
        }
    )

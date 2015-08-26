"""views for lifeX
"""

from django.http import Http404
from django.shortcuts import render_to_response

from lifeX.models import LifeXCategory
from lifeX.models import LifeXIdea
from lifeX.models import LifeXWeek
from lifeX.models import LifeXPost
from lifeX.models import LifeXBlog
from sitedata.social_meta import create_meta


# INDEX
def index(request):
    """lifeX homepage
    Some information about lifeX
    Links to ideas, weeks
    Latest week and its experiments

    Args:
        request(HttpRequest)

    Returns:
        HttpResponse: 200 on success, 404 on failure

    Raises:
        Http404: lifeX week does not exist
    """
    latest_week = LifeXWeek.objects.latest('number')
    # contruct meta tags
    title = 'Life Experiments'
    description = 'life and experiments at harshp.com'
    keywords = ['lifeX', 'experiments', 'life', ]
    url = request.build_absolute_uri()
    meta = create_meta(
        title,
        description,
        keywords,
        url,
    )
    return render_to_response(
        'lifeX/index.html',
        {
            'latest_week': latest_week,
            'page_url': url, 'meta': meta,
        }
    )


# IDEAS - ALL IDEAS
def ideas(request):
    """
    lifeX ideas
    All Ideas organized by Categories

    Args:
        request(HttpRequest)

    Returns:
        HttpResponse: 200 on success, 404 on failure

    Raises:
        Http404: idea does not exist
    """
    categories = LifeXCategory.objects.order_by('name')
    # contruct meta tags
    title = 'Life Experiment Ideas'
    description = 'lifeX experiment ideas at harshp.com'
    keywords = ['lifeX', 'experiments', 'idea', 'life', ]
    url = request.build_absolute_uri()
    meta = create_meta(
        title,
        description,
        keywords,
        url,
    )
    return render_to_response(
        'lifeX/ideas.html',
        {
            'categories': categories,
            'page_url': url, 'meta': meta,
        }
    )


# IDEAS - CATEGORY
def category(request, category):
    """
    lifeX category
    All Ideas within the Category
    Status of each Idea (experimented/retry)

    Args:
        request(HttpRequest)
        category(slug): category name in url

    Returns:
        HttpResponse: 200 on success, 404 on failure

    Raises:
        Http404: category does not exist
    """
    try:
        category = LifeXCategory.objects.get(slug=category)
    except LifeXCategory.DoesNotExist:
        raise Http404('Life Experiment Idea Category does not exist...')
    # contruct meta tags
    title = category.name
    description = 'A collection of lifeX ideas at harshp.com'
    keywords = ['lifeX', 'experiments', 'life', 'idea', ]
    url = request.build_absolute_uri()
    meta = create_meta(
        title,
        description,
        keywords,
        url,
    )
    return render_to_response(
        'lifeX/category.html',
        {
            'category': category,
            'page_url': url,
            'meta': meta,
        }
    )


# IDEAS - IDEA
def idea(request, category, idea):
    """
    lifeX idea
    Show Idea and associated information
    Status (experimented/retry)
    Link to each week and post that uses that idea

    Args:
        request(HttpRequest)
        category(slug): category name in url
        idea(slug): idea title in url

    Returns:
        HttpResponse: 200 on success, 404 on failure

    Raises:
        Http404: lifeX idea does not exist
    """
    try:
        category = LifeXCategory.objects.get(slug=category)
        idea = LifeXIdea.objects.get(category=category, slug=idea)
    except LifeXIdea.DoesNotExist:
        raise Http404('Life Experiment Idea does not exist...')
    except LifeXCategory.DoesNotExist:
        raise Http404('Life Experiment Idea does not exist...')
    # contruct meta tags
    title = idea.title
    description = 'A lifeX idea at harshp.com'
    keywords = ['lifeX', 'experiments', 'life', 'idea', ]
    url = request.build_absolute_uri()
    meta = create_meta(
        title,
        description,
        keywords,
        url,
    )
    return render_to_response(
        'lifeX/idea.html',
        {
            'idea': idea,
            'page_url': url,
            'meta': meta,
        }
    )


# EXPERIMENTS - ALL WEEKS
def experiments(request):
    """
    lifeX experiments
    All weeks and associated posts
    All ideas associated with each week

    Args:
        request(HttpRequest)

    Returns:
        HttpResponse: 200 on success, 404 on failure

    Raises:
        Http404: lifeX week does not exist
    """
    weeks = LifeXWeek.objects.order_by('-number')
    # contruct meta tags
    title = 'Life Experiment Weeks'
    description = 'All the weeks of lifeX at harshp.com'
    keywords = ['lifeX', 'experiments', 'life', 'idea', ]
    url = request.build_absolute_uri()
    meta = create_meta(
        title,
        description,
        keywords,
        url,
    )
    return render_to_response(
        'lifeX/experiments.html',
        {
            'weeks': weeks,
            'page_url': url,
            'meta': meta,
        }
    )


# EXPERIMENTS - WEEK
def week(request, week):
    """
    lifeX week
    All posts and ideas associated with a week
    Show if the idea is marked for retry

    Args:
        request(HttpRequest)
        week(slug): week number in url

    Returns:
        HttpResponse: 200 on success, 404 on failure

    Raises:
        Http404: lifeX week does not exist
    """
    # TODO: show if the idea is marked for retry
    try:
        week = LifeXWeek.objects.get(number=week)
    except LifeXWeek.DoesNotExist:
        raise Http404('Life Experiment Week does not exist...')
    # contruct meta tags
    title = str(week)
    description = 'A lifeX week at harshp.com'
    keywords = ['lifeX', 'experiments', 'life', 'idea', ]
    url = request.build_absolute_uri()
    meta = create_meta(
        title,
        description,
        keywords,
        url,
    )
    return render_to_response(
        'lifeX/week.html',
        {
            'week': week,
            'page_url': url,
            'meta': meta,
        }
    )


# EXPERIMENTS - POST
def post(request, week, idea):
    """
    lifeX experiment post
    Show associated week and idea
    Show other ideas and posts in this week

    Args:
        request(HttpRequest)
        week(slug): week number in url
        idea(slug): idea title in url

    Returns:
        HttpResponse: 200 on success, 404 on failure

    Raises:
        Http404: lifeX week, post, or idea does not exist
    """
    # TODO: show other ideas and posts in this week
    try:
        week = LifeXWeek.objects.get(number=week)
        idea = LifeXIdea.objects.get(slug=idea)
        post = LifeXPost.objects.get(week=week, idea=idea)
    except (
        LifeXPost.DoesNotExist,
        LifeXWeek.DoesNotExist,
        LifeXIdea.DoesNotExist,
    ):
        raise Http404('Life Experiment Post does not exist...')
    # contruct meta tags
    title = post.title
    description = 'A lifeX post at harshp.com'
    keywords = ['lifeX', 'experiments', 'life', 'post', ]
    for tag in post.tags.all():
        keywords.append(tag.tagname)
    url = request.build_absolute_uri()
    meta = create_meta(
        title,
        description,
        keywords,
        url,
    )
    return render_to_response(
        'lifeX/post.html',
        {
            'post': post,
            'page_url': url,
            'meta': meta,
        }
    )


# BLOG - ALL BLOG POSTS
def blog(request):
    """
    lifeX blog
    Show all blog posts as links
    OR Show all blog posts as paged posts

    Args:
        request(HttpRequest)

    Returns:
        HttpResponse: 200 on success, 404 on failure

    Raises:
        Http404: lifeX blog does not exist
    """
    # TODO: pagination for blog posts
    blogposts = LifeXBlog.objects.order_by('-published')
    # contruct meta tags
    title = 'LifeX Blog'
    description = 'LifeX blog at harshp.com'
    keywords = ['blog', 'lifeX', 'experiments', 'life', ]
    url = request.build_absolute_uri()
    meta = create_meta(
        title,
        description,
        keywords,
        url,
        None
    )
    return render_to_response(
        'lifeX/blog.html',
        {
            'blogposts': blogposts,
            'page_url': url,
            'meta': meta,
        }
    )


# BLOG - BLOGPOST
def blogpost(request, blogpost):
    """
    lifeX blog post
    Show blog post

    Args:
        request(HttpRequest)
        blogpost(slug) blog post title in url

    Returns:
        HttpResponse: 200 on success, 404 on failure

    Raises:
        Http404: lifeX blog does not exist
    """
    try:
        blogpost = LifeXBlog.objects.get(slug=blogpost)
    except LifeXBlog.DoesNotExist:
        raise Http404('Blog Post does not exist...')
    # contruct meta tags
    title = blogpost.title
    description = 'A Life Experiments blog post at harshp.com'
    keywords = ['blog', 'lifeX', 'experiments', 'life', ]
    for tag in blogpost.tags.all():
        keywords.append(tag.tagname)
    url = request.build_absolute_uri()
    meta = create_meta(
        title,
        description,
        keywords,
        url,
        blogpost.headerimage
    )
    return render_to_response(
        'lifeX/blogpost.html',
        {
            'post': blogpost,
            'page_url': url,
            'meta': meta,
        }
    )


# LIFEX presentation
def presentation(request):
    """
    LifeX - A Presentation

    Args:
        request(HttpRequest)

    Returns:
        HttpResponse: 200 on success

    Raises:
        None
    """
    title = 'Life Experiments - A Presentation'
    description = '''
        A presentation on Life Experiments.
        What lifeX is, why it is so awesome,
        and why I feel we all should apply it.'''
    keywords = ['lifeX', 'experiments', 'life', 'idea', 'presentation', ]
    url = request.build_absolute_uri()
    meta = create_meta(
        title,
        description,
        keywords,
        url,
    )
    return render_to_response(
        'lifeX/presentation_UCC2014.html',
        {
            'meta': meta,
            'page_url': url,
        },
    )

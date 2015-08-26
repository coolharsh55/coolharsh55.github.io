"""views for blog
"""

from django.http import Http404
from django.shortcuts import render_to_response
from blog.models import BlogPost
from sitedata.social_meta import create_meta


def index(request):
    """index view for blogs

    shows all blog posts sorted by last published

    Args:
        request(HttpRequest)

    Returns:
        HttpResponse: 200 on success, 404 otherwise

    Raises:
        Http404: blog post not found
    """
    blogposts = BlogPost.objects.order_by('-published').values()
    title = 'blog at harshp.com'
    description = 'a blog with my thoughts and reflections'
    keywords = ['blog', 'harshp.com', 'coolharsh55', ]
    url = request.build_absolute_uri()
    meta = create_meta(
        title,
        description,
        keywords,
        url
    )
    return render_to_response(
        'blog/index.html', {
            'posts': blogposts,
            'meta': meta,
        },
    )


def blogpost(request, blogpost):
    """view for blog post

    Args:
        request(HttpRequest)
        blogpost(str): slug of blog post in url

    Returns:
        HttpResponse: 200 on success, 404 on error

    Raises:
        Http404: blog post not found
    """
    try:
        blogpost = BlogPost.objects.get(slug=blogpost)
    except BlogPost.DoesNotExist:
        raise Http404('Blog Post does not exist...')
    # contruct meta tags
    title = blogpost.title
    description = 'A blog post at harshp.com'
    keywords = ['blog', ]
    for tag in blogpost.tags.all():
        keywords.append(tag.tagname)
    url = request.build_absolute_uri()
    meta = create_meta(
        title, description, keywords, url, blogpost.headerimage)
    return render_to_response(
        'blog/blogpost.html',
        {
            'post': blogpost,
            'page_url': url,
            'meta': meta,
        }
    )

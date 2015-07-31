"""views for articles
"""

from django.http import Http404
from django.shortcuts import render_to_response
from .models import Article
from sitedata.social_meta import create_meta


def index(request):
    """index view for article homepage

    show all articles sorted by last published

    Args:
        request: HttpRequest

    Returns:
        HttpResponse: 200 on success, 404 on Not found

    Raises:
        Http404: article not found
    """
    try:
        articles = Article.objects.order_by('-published').values()
        title = 'articles at harshp.com'
        description = 'articles written by me'
        keywords = ['article', 'harshp.com', 'coolharsh55', ]
        url = request.build_absolute_uri()
        meta = create_meta(
            title,
            description,
            keywords,
            url
        )
    except Article.DoesNotExist:
        raise Http404('Article does not exist...')
    return render_to_response(
        'articles/index.html',
        {
            'posts': articles,
            'page_url': url,
            'meta': meta,
        }
    )


def article(request, article):
    """view for article post

    Args:
        request(HttpRequest): request for article
        article(str): article requested through url

    Returns:
        HttpResponse: 200 on success, 404 otherwise

    Raises:
        Http404: article not found
    """
    try:
        article = Article.objects.get(slug=article)
        # contruct meta tags
        title = article.title
        description = 'An article at harshp.com'
        keywords = ['article', ]
        for tag in article.tags.all():
            keywords.append(tag.tagname)
        url = request.build_absolute_uri()
        meta = create_meta(
            title,
            description,
            keywords,
            url,
            article.headerimage
        )
    except Article.DoesNotExist:
        raise Http404('Article does not exist...')
    return render_to_response(
        'articles/article.html',
        {
            'post': article,
            'page_url': url,
            'meta': meta,
        }
    )

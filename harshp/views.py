"""views for harshp
"""

from django.http import Http404
from django.shortcuts import render_to_response

from blog.models import BlogPost
from stories.models import StoryPost
from poems.models import Poem
from articles.models import Article
from lifeX.models import LifeXWeek
from lifeX.models import LifeXBlog
from brainbank.models import BrainBankPost
from sitedata.social_meta import create_meta
from hobbies.models import Book
from hobbies.models import Movie
from hobbies.models import TVShow
from hobbies.models import Game
# from django.db.models import Q


def home(request):
    """homepage for harshp.com

    show all the latest posts in different apps

    Args:
        request(HttpResponse)

    Returns:
        HttpResponse: 200 on success, 404 on error

    Raises:
        Http404: error retrieving posts
    """
    try:
        blogs = BlogPost.objects.order_by('-published')[:3]
        stories = StoryPost.objects.order_by('-published')[:3]
        poems = Poem.objects.order_by('-published')[:3]
        articles = Article.objects.order_by('-published')[:3]
        brainbank_posts = BrainBankPost.objects.order_by('-published')[:3]
        lifexweek = LifeXWeek.objects.latest('number')
        lifexposts = LifeXBlog.objects.order_by('-published')[:3]
        books = Book.objects.filter(date_end=None, finished=False)[:5]
        movies = Movie.objects.order_by('-date_seen')[:5]
        tvshows = TVShow.objects.order_by('-date_start')[:5]
        games = Game.objects.order_by('-date_start')[:5]
        description = """
            The personal website of Harshvardhan Pandit (coolharsh55)"""
        keywords = ['harshp.com', 'blog', 'stories', 'poems', ]
        meta = create_meta(
            'harshp.com',
            description,
            keywords,
            url=request.build_absolute_uri(),
        )
    except (BlogPost.DoesNotExist,
            StoryPost.DoesNotExist,
            Poem.DoesNotExist,
            Article.DoesNotExist,
            LifeXWeek.DoesNotExist,
            LifeXBlog.DoesNotExist,
            BrainBankPost.DoesNotExist,
            Book.DoesNotExist,
            Movie.DoesNotExist,
            TVShow.DoesNotExist,
            Game.DoesNotExist):
        raise Http404('Error retrieving website data...')
    return render_to_response(
        'harshp/index.html',
        {
            'blogs': blogs,
            'stories': stories,
            'poems': poems,
            'articles': articles,
            'brainbank_posts': brainbank_posts,
            'lifeXweek': lifexweek,
            'lifeXposts': lifexposts,
            'books': books,
            'movies': movies,
            'tvshows': tvshows,
            'games': games,
            'meta': meta,
        }
    )


def changelog(request):
    """changelog

    show the project changelog

    Args:
        request(HttpResponse)

    Returns:
        HttpResponse: 200 on success, 404 on error

    Raises:
        None
    """
    return render_to_response('harshp/changelog.html')


def privacypolicy(request):
    """privacy policy

    show the privacy policy for website

    Args:
        request(HttpResponse)

    Returns:
        HttpResponse: 200 on success, 404 on error

    Raises:
        None
    """
    return render_to_response('harshp/privacypolicy.html')

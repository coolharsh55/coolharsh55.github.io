"""tests for harshp site views

"""

from django.test import Client
from django.test import TestCase

from subdomains.utils import reverse
from django_seed import Seed

from blog.models import BlogPost
from stories.models import StoryPost
from poems.models import Poem
from articles.models import Article
from lifeX.models import LifeXWeek
from lifeX.models import LifeXBlog
from brainbank.models import BrainBankIdea
from brainbank.models import BrainBankPost
from hobbies.models import Book
from hobbies.models import Movie
from hobbies.models import TVShow
from hobbies.models import Game


class SiteViewTest(TestCase):

    """tests for site-wide views
    """

    def setUp(self):
        """setup tests
        """
        self.client = Client()

    def test_privacy_policy_url(self):
        """test privacy policy url
        """
        url = reverse(
            viewname='privacypolicy',
            subdomain=None)
        self.assertIsNotNone(url)

    def test_privacy_policy_view(self):
        """test privacy policy view
        """
        url = reverse(
            viewname='privacypolicy',
            subdomain=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_changelog_url(self):
        """test privacy policy url
        """
        url = reverse(
            viewname='changelog',
            subdomain=None)
        self.assertIsNotNone(url)

    def test_changelog_view(self):
        """test privacy policy view
        """
        url = reverse(
            viewname='changelog',
            subdomain=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class HomepageTest(TestCase):

    """tests for homepage
    """

    def setUp(self):
        """setup tests for homepage
        """
        self.client = Client()
        self.seeder = Seed.seeder()
        self.seeder.add_entity(BlogPost, 10)
        self.seeder.add_entity(Article, 10)
        self.seeder.add_entity(Poem, 10)
        self.seeder.add_entity(StoryPost, 10)
        self.seeder.add_entity(BrainBankIdea, 10)
        self.seeder.add_entity(BrainBankPost, 10)
        self.seeder.add_entity(LifeXWeek, 10)
        self.seeder.add_entity(LifeXBlog, 10)
        self.seeder.add_entity(Book, 10)
        self.seeder.add_entity(Movie, 10)
        self.seeder.add_entity(TVShow, 10)
        self.seeder.add_entity(Game, 10)
        self.seeder.execute()

    def test_url(self):
        """test homepage url
        """
        url = reverse(
            viewname='home',
            subdomain=None)
        self.assertIsNotNone(url)

    def test_view(self):
        """test homepage view
        """
        url = reverse(
            viewname='home',
            subdomain=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

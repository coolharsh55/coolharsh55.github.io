"""tests for Hobbies

"""

from django.test import Client
from django.test import TestCase
from django.utils.timezone import now as time_now
from itertools import izip as zip
from random import randint

from django_seed import Seed
from subdomains.utils import reverse

from .models import Book
from .models import Movie
from .models import TVShow
from .models import Game

HTTP_HOST = 'hobbies.example.com'


class BookTest(TestCase):

    """Tests for Books
    """

    def setUp(self):
        """setup tests for books
        """
        self.client = Client()
        self.seeder = Seed.seeder()
        self.seeder.add_entity(Book, 10)
        self.seeder.execute()

    def tearDown(self):
        """clean up after the tests
        """
        self.client = None
        self.seeder = None
        Book.objects.all().delete()

    def test_save(self):
        """test saving books
        """
        book = Book()
        book.title = 'somerandombook'
        book.date_start = time_now()
        book.save()
        self.assertIsNotNone(book.slug)
        self.assertIsNotNone(book.published)
        self.assertIsNotNone(book.modified)
        self.assertIsNone(book.date_end)
        self.assertIsNone(book.headerimage)
        self.assertEqual(len(book.tags.all()), 0)
        self.assertFalse(book.finished)
        book.save()

    def test_duplicates(self):
        """test duplicates for books
        """
        book1 = Book()
        book1.title = 'somerandombook'
        book1.date_start = time_now()
        book1.save()
        book2 = Book()
        book2.title = book1.title
        book2.date_start = book1.date_start
        book2.save()
        self.assertEqual(book1.title, book2.title)
        self.assertEqual(book1.date_start, book2.date_start)
        self.assertNotEqual(book1.slug, book2.slug)

    def test_date_end_before_date_start(self):
        """test that date end can never be before date start
        """
        book = Book.objects.all()[0]
        book.date_end = time_now()
        book.date_start = time_now()
        book.save()
        self.assertEqual(book.date_start, book.date_end)

    def test_str(self):
        """test str representation of book
        """
        book = Book.objects.all()[randint(0, Book.objects.count() - 1)]
        self.assertTrue(book.title in book.__str__())

    def test_abs_url(self):
        """test absolute url for books
        """
        book = Book.objects.all()[randint(0, Book.objects.count() - 1)]
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'books', 'hobbytitle': book.slug, })
        self.assertEqual(url, book.get_absolute_url())

    def test_url(self):
        """test url for books
        """
        book = Book.objects.all()[randint(0, Book.objects.count() - 1)]
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'books', 'hobbytitle': book.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_view(self):
        """test view for books
        """
        book = Book.objects.all()[randint(0, Book.objects.count() - 1)]
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'books', 'hobbytitle': book.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['item'], book)
        self.assertEqual(response.context['hobbytype'], 'books')
        description = response.context['description']
        self.assertTrue(str(book.date_start) in description)
        self.assertTrue(str(book.date_end) in description)

    def test_index_view(self):
        """test index view for books
        """
        url = reverse(
            viewname='hobbies:type_index',
            subdomain='hobbies',
            kwargs={'hobbytype': 'books', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        items = [
            (i, str(i.date_start), str(i.date_end))
            for i in Book.objects.all()
        ]
        response_items = response.context['items']
        self.assertEqual(len(items), len(response_items))
        for i, ri in zip(items, response_items):
            self.assertTrue(len(i) == 3)
            self.assertTrue(len(ri) == 2)
            self.assertEqual(i[0], ri[0])
            self.assertTrue(i[1] in ri[1])
            self.assertTrue(i[2] in ri[1])

    def test_404(self):
        """test 404 for non-existant books
        """
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'books', 'hobbytitle': 'randombook', })
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)


class MovieTest(TestCase):

    """Tests for Movies
    """

    def setUp(self):
        """setup tests for movies
        """
        self.client = Client()
        self.seeder = Seed.seeder()
        self.seeder.add_entity(Movie, 10)
        self.seeder.execute()

    def tearDown(self):
        """clean up after the tests
        """
        self.client = None
        self.seeder = None
        Movie.objects.all().delete()

    def test_save(self):
        """test saving movies
        """
        movie = Movie()
        movie.title = 'somerandommovie'
        movie.date_seen = time_now()
        movie.save()
        self.assertIsNotNone(movie.slug)
        self.assertIsNotNone(movie.published)
        self.assertIsNotNone(movie.modified)
        self.assertIsNone(movie.headerimage)
        self.assertEqual(len(movie.tags.all()), 0)
        self.assertFalse(movie.finished)
        movie.save()

    def test_duplicates(self):
        """test duplicates for movies
        """
        movie1 = Movie()
        movie1.title = 'somerandommovie'
        movie1.date_seen = time_now()
        movie1.save()
        movie2 = Movie()
        movie2.title = movie1.title
        movie2.date_seen = movie1.date_seen
        movie2.save()
        self.assertEqual(movie1.title, movie2.title)
        self.assertEqual(movie1.date_seen, movie2.date_seen)
        self.assertNotEqual(movie1.slug, movie2.slug)

    def test_str(self):
        """test str representation of movie
        """
        movie = Movie.objects.all()[randint(0, Movie.objects.count() - 1)]
        self.assertTrue(movie.title in movie.__str__())

    def test_abs_url(self):
        """test absolute url for movies
        """
        movie = Movie.objects.all()[randint(0, Movie.objects.count() - 1)]
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'movies', 'hobbytitle': movie.slug, })
        self.assertEqual(url, movie.get_absolute_url())

    def test_url(self):
        """test url for movies
        """
        movie = Movie.objects.all()[randint(0, Movie.objects.count() - 1)]
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'movies', 'hobbytitle': movie.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_view(self):
        """test view for movies
        """
        movie = Movie.objects.all()[randint(0, Movie.objects.count() - 1)]
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'movies', 'hobbytitle': movie.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['item'], movie)
        self.assertEqual(response.context['hobbytype'], 'movies')
        description = response.context['description']
        self.assertTrue(str(movie.date_seen) in description)

    def test_index_view(self):
        """test index view for movies
        """
        url = reverse(
            viewname='hobbies:type_index',
            subdomain='hobbies',
            kwargs={'hobbytype': 'movies', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        items = [
            (i, str(i.date_seen))
            for i in Movie.objects.all()
        ]
        response_items = response.context['items']
        self.assertEqual(len(items), len(response_items))
        for i, ri in zip(items, response_items):
            self.assertTrue(len(i) == 2)
            self.assertTrue(len(ri) == 2)
            self.assertEqual(i[0], ri[0])
            self.assertTrue(i[1] in ri[1])

    def test_404(self):
        """test 404 for non-existant movies
        """
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'movies', 'hobbytitle': 'randommovie', })
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)


class TVShowTest(TestCase):

    """Tests for TVShows
    """

    def setUp(self):
        """setup tests for tvshows
        """
        self.client = Client()
        self.seeder = Seed.seeder()
        self.seeder.add_entity(TVShow, 10)
        self.seeder.execute()

    def tearDown(self):
        """clean up after the tests
        """
        self.client = None
        self.seeder = None
        TVShow.objects.all().delete()

    def test_save(self):
        """test saving tvshows
        """
        tvshow = TVShow()
        tvshow.title = 'somerandomtvshow'
        tvshow.date_start = time_now()
        tvshow.save()
        self.assertIsNotNone(tvshow.slug)
        self.assertIsNotNone(tvshow.published)
        self.assertIsNotNone(tvshow.modified)
        self.assertIsNone(tvshow.date_end)
        self.assertIsNone(tvshow.headerimage)
        self.assertEqual(len(tvshow.tags.all()), 0)
        self.assertFalse(tvshow.finished)
        tvshow.save()

    def test_date_end_before_date_start(self):
        """test that date end can never be before date start
        """
        tvshow = TVShow.objects.all()[0]
        tvshow.date_end = time_now()
        tvshow.date_start = time_now()
        tvshow.save()
        self.assertEqual(tvshow.date_start, tvshow.date_end)

    def test_duplicates(self):
        """test duplicates for tvshows
        """
        tvshow1 = TVShow()
        tvshow1.title = 'somerandomtvshow'
        tvshow1.date_start = time_now()
        tvshow1.save()
        tvshow2 = TVShow()
        tvshow2.title = tvshow1.title
        tvshow2.date_start = tvshow1.date_start
        tvshow2.save()
        self.assertEqual(tvshow1.title, tvshow2.title)
        self.assertEqual(tvshow1.date_start, tvshow2.date_start)
        self.assertNotEqual(tvshow1.slug, tvshow2.slug)

    def test_str(self):
        """test str representation of book
        """
        tvshow = TVShow.objects.all()[randint(0, TVShow.objects.count() - 1)]
        self.assertTrue(tvshow.title in tvshow.__str__())

    def test_abs_url(self):
        """test absolute url for tvshows
        """
        tvshow = TVShow.objects.all()[randint(0, TVShow.objects.count() - 1)]
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'tvshows', 'hobbytitle': tvshow.slug, })
        self.assertEqual(url, tvshow.get_absolute_url())

    def test_url(self):
        """test url for tvshows
        """
        tvshow = TVShow.objects.all()[randint(0, TVShow.objects.count() - 1)]
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'tvshows', 'hobbytitle': tvshow.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_view(self):
        """test view for tvshows
        """
        tvshow = TVShow.objects.all()[randint(0, TVShow.objects.count() - 1)]
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'tvshows', 'hobbytitle': tvshow.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['item'], tvshow)
        self.assertEqual(response.context['hobbytype'], 'tvshows')
        description = response.context['description']
        self.assertTrue(str(tvshow.date_start) in description)
        self.assertTrue(str(tvshow.date_end) in description)

    def test_index_view(self):
        """test index view for tvshows
        """
        url = reverse(
            viewname='hobbies:type_index',
            subdomain='hobbies',
            kwargs={'hobbytype': 'tvshows', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        items = [
            (i, str(i.date_start), str(i.date_end))
            for i in TVShow.objects.all()
        ]
        response_items = response.context['items']
        self.assertEqual(len(items), len(response_items))
        for i, ri in zip(items, response_items):
            self.assertTrue(len(i) == 3)
            self.assertTrue(len(ri) == 2)
            self.assertEqual(i[0], ri[0])
            self.assertTrue(i[1] in ri[1])
            self.assertTrue(i[2] in ri[1])

    def test_404(self):
        """test 404 for non-existant books
        """
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'tvshows', 'hobbytitle': 'randomtvshow', })
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)


class GameTest(TestCase):

    """Tests for Games
    """

    def setUp(self):
        """setup tests for games
        """
        self.client = Client()
        self.seeder = Seed.seeder()
        self.seeder.add_entity(Game, 10)
        self.seeder.execute()

    def tearDown(self):
        """clean up after the tests
        """
        self.client = None
        self.seeder = None
        Game.objects.all().delete()

    def test_save(self):
        """test saving games
        """
        game = Game()
        game.title = 'somerandomgame'
        game.date_start = time_now()
        game.save()
        self.assertIsNotNone(game.slug)
        self.assertIsNotNone(game.published)
        self.assertIsNotNone(game.modified)
        self.assertIsNone(game.date_end)
        self.assertIsNone(game.headerimage)
        self.assertEqual(len(game.tags.all()), 0)
        self.assertFalse(game.finished)
        game.save()

    def test_date_end_before_date_start(self):
        """test that date end can never be before date start
        """
        game = Game.objects.all()[0]
        game.date_end = time_now()
        game.date_start = time_now()
        game.save()
        self.assertEqual(game.date_start, game.date_end)

    def test_duplicates(self):
        """test duplicates for games
        """
        # TODO: figure out a way to test for duplicates
        # without raising errors in atomic blocks

    def test_str(self):
        """test str representation of game
        """
        game = Game.objects.all()[randint(0, Game.objects.count() - 1)]
        self.assertTrue(game.title in game.__str__())

    def test_abs_url(self):
        """test absolute url for games
        """
        game = Game.objects.all()[randint(0, Game.objects.count() - 1)]
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'games', 'hobbytitle': game.slug, })
        self.assertEqual(url, game.get_absolute_url())

    def test_url(self):
        """test url for games
        """
        game = Game.objects.all()[randint(0, Game.objects.count() - 1)]
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'games', 'hobbytitle': game.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_index_url(self):
        """test index url for games
        """
        url = reverse(
            viewname='hobbies:type_index',
            subdomain='hobbies',
            kwargs={'hobbytype': 'games', })
        self.assertIsNotNone(url)

    def test_view(self):
        """test view for games
        """
        game = Game.objects.all()[randint(0, Game.objects.count() - 1)]
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'games', 'hobbytitle': game.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['item'], game)
        self.assertEqual(response.context['hobbytype'], 'games')
        description = response.context['description']
        self.assertTrue(str(game.date_start) in description)
        self.assertTrue(str(game.date_end) in description)

    def test_index_view(self):
        """test index view for games
        """
        url = reverse(
            viewname='hobbies:type_index',
            subdomain='hobbies',
            kwargs={'hobbytype': 'games', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        game_items = [
            (g, str(g.date_start), str(g.date_end))
            for g in Game.objects.all()
        ]
        response_game_items = response.context['items']
        self.assertEqual(len(game_items), len(response_game_items))
        for g, rg in zip(game_items, response_game_items):
            self.assertTrue(len(g) == 3)
            self.assertTrue(len(rg) == 2)
            self.assertEqual(g[0], rg[0])
            self.assertTrue(g[1] in rg[1])
            self.assertTrue(g[2] in rg[1])

    def test_404(self):
        """test 404 for non-existant games
        """
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'games', 'hobbytitle': 'randomgame', })
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)


class HobbyViewTests(TestCase):

    """tests for hobby views and indexes
    """

    def setUp(self):
        """setup tests for hobby views and indexes
        """
        self.client = Client()
        seeder = Seed.seeder()
        seeder.add_entity(Book, 10)
        seeder.add_entity(Movie, 10)
        seeder.add_entity(TVShow, 10)
        seeder.add_entity(Game, 10)
        seeder.execute()

    def tearDown(self):
        """clean up after tests
        """
        for book in Book.objects.all():
            book.delete()
        for movie in Movie.objects.all():
            movie.delete()
        for tvshow in TVShow.objects.all():
            tvshow.delete()
        for game in Game.objects.all():
            game.delete()

    def test_404_invalid_hobby_in_type_item_view(self):
        """test invalid hobby passed to get item in view
        """
        book = Book.objects.latest('published')
        url = reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'randomhobby', 'hobbytitle': book.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

    def test_404_invalid_hobby_in_type_index_view(self):
        """test 404 for invalid item
        """
        url = reverse(
            viewname='hobbies:type_index',
            subdomain='hobbies',
            kwargs={'hobbytype': 'randomhobby', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

    def test_hobby_index_view(self):
        """test hobby index view
        """
        url = reverse(
            viewname='hobbies:hobby_index',
            subdomain='hobbies')
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        # TODO: check objects returned

    def test_hobby_index_url(self):
        """test url for hobby index
        """
        url = reverse(
            viewname='hobbies:hobby_index',
            subdomain='hobbies')
        self.assertIsNotNone(url)

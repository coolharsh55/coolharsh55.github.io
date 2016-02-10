from autofixture import AutoFixture
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Author
from .models import Post
from .models import Tag

HTTP_HOST = "example.com"


class TagTests(TestCase):
    """tests for Tag"""

    def setUp(self):
        self.client = Client()
        self.fixture = AutoFixture(Tag)

    def tearDown(self):
        Tag.objects.all().delete()

    def populate(self, num):
        self.fixture.create(num)

    def test_save(self):
        tag = Tag()
        tag.name = 'test tag'
        tag.save()
        self.assertIsNotNone(tag.pk)
        self.assertIsNotNone(tag.slug)

    def test_unique_slug(self):
        self.populate(10)

    def test_str(self):
        self.populate(1)
        t = Tag.objects.all()[0]
        self.assertEqual(t.name, str(t))

    def test_url(self):
        self.populate(1)
        t = Tag.objects.all()[0]
        self.assertEqual(
            t.get_absolute_url(), reverse(
                'sitebase:tags:get', args=[t.slug]))

    def test_tags_url(self):
        self.assertIsNotNone(reverse('sitebase:tags:list'))


class AuthorTests(TestCase):
    """tests for Author"""

    def setUp(self):
        self.client = Client()
        self.fixture = AutoFixture(Author)

    def tearDown(self):
        Author.objects.all().delete()

    def populate(self, num):
        self.fixture.create(num)

    def test_save(self):
        author = Author()
        author.name = 'test Author'
        author.email = 'author@example.com'
        author.short_bio = 'just an awesome author'
        author.save()
        self.assertIsNotNone(author.pk)
        self.assertIsNotNone(author.slug)

    def test_unique_slug(self):
        self.populate(10)

    def test_str(self):
        self.populate(1)
        a = Author.objects.all()[0]
        self.assertEqual(a.name, str(a))

    def test_url(self):
        self.populate(1)
        a = Author.objects.all()[0]
        self.assertEqual(
            a.get_absolute_url(), reverse(
                'sitebase:authors:get', args=[a.slug]))

    def test_authors_url(self):
        self.assertIsNotNone(reverse('sitebase:authors:list'))


class PostTests(TestCase):
    """tests for Posts"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_str(self):
        post = Post(title='test')
        self.assertEqual(post.title, str(post))

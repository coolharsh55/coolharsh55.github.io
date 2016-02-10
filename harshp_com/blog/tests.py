from autofixture import AutoFixture
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse

from sitebase.editors import EDITOR_TYPES

from .models import BlogPost
from .models import BlogSeries

HTTP_HOST = "example.com"


class BlogPostTests(TestCase):
    """tests for BlogPost"""

    def setUp(self):
        self.client = Client()
        self.fixture = AutoFixture(BlogPost)
        self.fixture_fk = AutoFixture(BlogPost, generate_fk=True)

    def tearDown(self):
        BlogPost.objects.all().delete()

    def populate(self, num, series=None):
        self.fixture.create(num)
        self.fixture_fk.create(num)

    def test_save(self):
        blog = BlogPost()
        blog.title = 'test BlogPost'
        blog.body = 'blog body'
        blog.save()
        self.assertIsNotNone(blog.pk)
        self.assertIsNotNone(blog.slug)

    def test_unique_slug(self):
        self.populate(10)

    def test_slug_immutable(self):
        self.populate(1)
        b = BlogPost.objects.all()[0]
        slug = b.slug
        b.title = 'mutable field'
        b.save()
        self.assertEqual(slug, b.slug)

    def test_str(self):
        self.populate(1)
        b = BlogPost.objects.all()[0]
        self.assertEqual(b.title, str(b))

    def test_url(self):
        self.populate(1)
        b = BlogPost.objects.filter(series=None)[0]
        self.assertEqual(
            b.get_absolute_url(), reverse(
                'blog:post', args=[b.slug]))
        series_fixture = AutoFixture(BlogSeries)
        series_fixture.create(1)
        b.series = BlogSeries.objects.all()[0]
        b.save()
        b = BlogPost.objects.filter(series__isnull=False)[0]
        self.assertEqual(
            b.get_absolute_url(), reverse(
                'blog:post', args=[b.series.slug, b.slug]))

    def test_body_types(self):
        self.populate(1)
        b = BlogPost.objects.filter(series=None)[0]
        try:
            for editortype, text in EDITOR_TYPES:
                b.body_type = editortype
                b.save()
        except Exception as e:
            self.fail('Failed: {}'.format(e))

    def test_blogs_url(self):
        self.assertIsNotNone(reverse('blog:list'))


class BlogSeriesTests(TestCase):
    """tests for BlogSeries"""

    def setUp(self):
        self.client = Client()
        self.fixture = AutoFixture(BlogSeries)

    def tearDown(self):
        BlogSeries.objects.all().delete()

    def populate(self, num):
        self.fixture.create(num)

    def test_save(self):
        series = BlogSeries()
        series.title = 'test BlogSeries'
        series.short_description = 'just some blog series'
        series.save()
        self.assertIsNotNone(series.pk)
        self.assertIsNotNone(series.slug)

    def test_unique_slug(self):
        self.populate(10)

    def test_slug_immutable(self):
        self.populate(1)
        series = BlogSeries.objects.all()[0]
        slug = series.slug
        series.title = 'mutable field'
        series.save()
        self.assertEqual(slug, series.slug)

    def test_duplicate_names(self):
        self.populate(1)
        series = BlogSeries.objects.all()[0]
        series.title='mutable field'
        try:
            series.save()
        except Exception as e:
            self.fail('Failed: {}'.format(e))

    def test_str(self):
        self.populate(1)
        series = BlogSeries.objects.all()[0]
        self.assertEqual(series.title, str(series))

    def test_url(self):
        self.populate(1)
        series = BlogSeries.objects.all()[0]
        self.assertEqual(
            series.get_absolute_url(), reverse(
                'blog:series', args=[series.slug]))

    def test_seriess_url(self):
        self.assertIsNotNone(reverse('blog:series-list'))

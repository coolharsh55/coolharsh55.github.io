"""tests for dev blog
"""

from datetime import timedelta
from django.core.urlresolvers import NoReverseMatch
from django.test import Client
from django.test import TestCase
from django.utils import timezone

from django_seed import Seed
from subdomains.utils import reverse

# from sitedata.models import CSSLink
from sitedata.models import JSLink

from .models import DevBlogPost
from .models import DevBlogSeries

HTTP_HOST = 'dev.example.com'


class DevBlogPostTest(TestCase):

    """tests for dev blog posts
    """

    def setUp(self):
        """setup tests
        """
        self.seeder = Seed.seeder()
        self.seeder.add_entity(DevBlogSeries, 10)
        self.seeder.execute()
        self.seeder.add_entity(DevBlogPost, 10, {
            'future': lambda x: timezone.now() + timedelta(days=+6),
        })
        self.seeder.execute()
        self.client = Client()

    def tearDown(self):
        """clean up after tests
        """
        DevBlogSeries.objects.all().delete()
        DevBlogPost.objects.all().delete()

    def test_str(self):
        """test string representation of dev blog post
        should return the post title
        """
        post = DevBlogPost.objects.all()[0]
        self.assertEqual(post.__str__(), post.title)

    def test_duplicate(self):
        """test duplicate dev blog posts
        should not allow duplicates
        """
        post1 = DevBlogPost.objects.all()[0]
        post2 = DevBlogPost(
            title=post1.title,
            body=post1.body,
            published=post1.published,
            series=post1.series,
            modified=post1.modified,
            headerimage=post1.headerimage,
            draft=post1.draft,
            future=post1.future,
        )
        with self.assertRaises(AssertionError):
            post2.save()

    def test_post_url(self):
        """test dev blog post url
        """
        post = DevBlogPost.objects.all()[0]
        series_slug = 'blog' if post.series.slug is None else post.series.slug
        url = reverse(
            viewname='devblog:blog_post',
            subdomain='dev',
            kwargs={'series': series_slug, 'blog_post': post.slug, })
        self.assertIsNotNone(url)
        self.assertEqual(post.get_absolute_url(), url)

    def test_valid_post_url(self):
        """test dev blog posts only accept valid post urls
        """
        post = DevBlogPost.objects.all()[0]
        with self.assertRaises(NoReverseMatch):
            reverse(
                viewname='devblog:blog_post',
                subdomain='dev',
                kwargs={'blog_post': post.title, })

    def test_index_url(self):
        """test index url for dev blog posts
        """
        url = reverse(
            viewname='devblog:blog_index',
            subdomain='dev',)
        self.assertIsNotNone(url)

    def test_save_without_series(self):
        """test save method of dev blog post
        """
        post = DevBlogPost()
        post.title = 'some random title'
        post.body = 'some random content'
        post.published = timezone.now()
        post.draft = True
        post.future = timezone.now() + timedelta(days=+6)
        post.save()
        self.assertIsNotNone(post.post_id)
        self.assertIsNotNone(post.slug)
        self.assertIsNotNone(post.modified)

    def test_save_with_series(self):
        """test save method of dev blog post
        """
        series = DevBlogSeries.objects.all()[0]
        post = DevBlogPost()
        post.title = 'some random title'
        post.body = 'some random content'
        post.published = timezone.now()
        post.series = series
        post.draft = True
        post.future = timezone.now() + timedelta(days=+6)
        post.save()
        self.assertIsNotNone(post.post_id)
        self.assertIsNotNone(post.slug)
        self.assertIsNotNone(post.series)
        self.assertIsNotNone(post.modified)

    def test_post_view(self):
        """test view for dev blog posts
        """
        post = DevBlogPost.objects.all()[0]
        url = post.get_absolute_url()
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_index_view(self):
        """test index view for dev blog posts
        """
        url = reverse(viewname='devblog:blog_index', subdomain='dev')
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_nonexistant_post_view(self):
        """test nonexistant dev blog post returns 404 with valid url
        """
        url = reverse(
            viewname='devblog:blog_post',
            subdomain='dev',
            kwargs={'series': 'blog', 'blog_post': 'some-random-post', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

    def test_nonexistant_series_view(self):
        """test nonexistant dev blog post returns 404 with valid url
        """
        post = DevBlogPost.objects.all()[0]
        url = reverse(
            viewname='devblog:blog_post',
            subdomain='dev',
            kwargs={'series': 'some-random-series', 'blog_post': post.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

    def test_code_prettify(self):
        """test code prettify library gets attached if the post contains code
        """
        # post with <code> tag
        post = DevBlogPost.objects.all()[0]
        post.body = """<html>
        <body>
            <pre>
            <code class='prettyprint'>
            def foo(*args, **kwargs):
                return None
            </code>
            </pre>
        </body>
        </html>"""

        # js link for code prettify
        code_prettify = JSLink()
        code_prettify.name = 'code-prettify'
        code_prettify.link = (
            'https://'
            'cdn.rawgit.com/'
            'google/code-prettify/master/loader/'
            'run_prettify.js')
        code_prettify.save()

        # remove js link if already attached
        if code_prettify in post.js.all():
            code_prettify.remove()

        # save object and test link is attached
        post.save()
        self.assertTrue(code_prettify in post.js.all())

        # coverage--> check that link is attached only once
        post.save()

    def test_future_timezone(self):
        """test future date validations are done with time-awareness
        """
        post = DevBlogPost.objects.all()[0]
        post.future = timezone.make_naive(
            timezone.now() + timedelta(days=+6))
        self.assertTrue(timezone.is_naive(post.future))
        post.save()
        self.assertTrue(timezone.is_aware(post.future))

    def test_future_set_in_past(self):
        """test ValueError is raised when
        future is set to a date in the past
        """
        post = DevBlogPost.objects.all()[0]
        post.future = timezone.now() + timedelta(days=-6)
        with self.assertRaises(ValueError):
            post.save()

    def test_post_without_future(self):
        """test posts without a future set
        """
        post = DevBlogPost.objects.all()[0]
        post.future = None
        post.save()
        self.assertIsNone(post.future)


class DevBlogSeriesTest(TestCase):

    """tests for dev blog posts
    """

    def setUp(self):
        """setup tests
        """
        self.seeder = Seed.seeder()
        self.seeder.add_entity(DevBlogSeries, 10)
        self.seeder.execute()
        self.seeder.add_entity(DevBlogPost, 10, {
            'future': lambda x: timezone.now() + timedelta(days=+6),
        })
        self.seeder.execute()
        self.client = Client()

    def tearDown(self):
        """clean up after tests
        """
        DevBlogPost.objects.all().delete()
        DevBlogSeries.objects.all().delete()

    def test_str(self):
        """test string representation of dev blog post
        should return the post title
        """
        series = DevBlogSeries.objects.all()[0]
        self.assertEqual(series.__str__(), series.name)

    # def test_duplicate(self):
    #     """test duplicate dev blog seriess
    #     should not allow duplicates
    #     """
    #     series1 = DevBlogSeries.objects.all()[0]
    #     series2 = DevBlogSeries(
    #         name=series1.name,
    #         description=series1.description,
    #     )
    #     with self.assertRaises(Exception):
    #         series2.save()

    def test_series_url(self):
        """test dev blog series url
        """
        series = DevBlogSeries.objects.all()[0]
        url = reverse(
            viewname='devblog:blog_series',
            subdomain='dev',
            kwargs={'series': series.slug, })
        self.assertIsNotNone(url)
        self.assertEqual(series.get_absolute_url(), url)

    def test_index_url(self):
        """test index url for dev blog seriess
        """
        url = reverse(
            viewname='devblog:series_index',
            subdomain='dev',)
        self.assertIsNotNone(url)

    def test_save(self):
        """test save method of dev blog series
        """
        series = DevBlogSeries()
        series.name = 'some random title'
        series.save()
        self.assertIsNotNone(series.pk)
        self.assertIsNotNone(series.slug)

    def test_slug_on_modify(self):
        """test slug does not change on name modification
        """
        series = DevBlogSeries.objects.all()[0]
        series_slug = series.slug
        series.name = 'this is a random name'
        series.save()
        self.assertEqual(series.slug, series_slug)

    def test_series_view(self):
        """test view for dev blog seriess
        """
        series = DevBlogSeries.objects.all()[0]
        url = series.get_absolute_url()
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_index_view(self):
        """test index view for dev blog seriess
        """
        url = reverse(viewname='devblog:series_index', subdomain='dev')
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_nonexistant_series_view(self):
        """test nonexistant dev blog series returns 404 with valid url
        """
        url = reverse(
            viewname='devblog:blog_series',
            subdomain='dev',
            kwargs={'series': 'some-random-series', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)


class HomepageTest(TestCase):

    """test the dev homepage
    """

    def setUp(self):
        """setup tests
        """
        self.seeder = Seed.seeder()
        self.seeder.add_entity(DevBlogSeries, 10)
        self.seeder.execute()
        self.seeder.add_entity(DevBlogPost, 10, {
            'future': lambda x: timezone.now() + timedelta(days=+6),
        })
        self.seeder.execute()
        self.client = Client()

    def tearDown(self):
        """clean up after tests
        """
        DevBlogPost.objects.all().delete()
        DevBlogSeries.objects.all().delete()

    def test_url(self):
        """test the homepage url
        """
        url = reverse(
            viewname='devblog:dev_home',
            subdomain='dev')
        self.assertIsNotNone(url)

    def test_view(self):
        """test the homepage view
        """
        url = reverse(
            viewname='devblog:dev_home',
            subdomain='dev')
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

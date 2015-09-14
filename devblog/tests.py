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

HTTP_HOST = 'dev.example.com'


class DevBlogPostTest(TestCase):

    """tests for dev blog posts
    """

    def setUp(self):
        """setup tests
        """
        self.seeder = Seed.seeder()
        self.seeder.add_entity(DevBlogPost, 10, {
            'future': lambda x: timezone.now() + timedelta(days=+6),
        })
        self.seeder.execute()
        self.client = Client()

    def tearDown(self):
        """clean up after tests
        """
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
            modified=post1.modified,
            headerimage=post1.headerimage,
            draft=post1.draft,
            future=post1.future,
        )
        post2.save()
        self.assertEqual(post1.title, post2.title)
        self.assertNotEqual(post1.slug, post2.slug)

    def test_post_url(self):
        """test dev blog post url
        """
        post = DevBlogPost.objects.all()[0]
        url = reverse(
            viewname='devblog:blog_post',
            subdomain='dev',
            kwargs={'blog_post': post.slug, })
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

    def test_save(self):
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
            kwargs={'blog_post': 'some-random-post', })
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

"""Tests for Blogs

"""

from django.core.urlresolvers import NoReverseMatch
from django.test import TestCase
from django.test import Client
from django.utils import timezone

from subdomains.utils import reverse

from sitedata.models import Tag

from .models import BlogPost

HTTP_HOST = 'blog.example.com'


class BlogPostsModelTest(TestCase):

    """Tests for BlogPost Models
    """

    def setUp(self):
        """create a test BlogPost
        """
        self.client = Client()
        tag = Tag(tagname='test tag')
        tag.save()
        blog = BlogPost(
            title='Test BlogPost',
            body='This is a test blog',
            published=timezone.now(),
        )
        blog.save()
        self.blog_slug = blog.slug
        blog.tags.add(tag)
        blog.save()
        self.assertIn(tag, blog.tags.all())

    def test_add_model(self):
        """test adding BlogPosts
        """
        blog = BlogPost.objects.get(title='Test BlogPost')
        self.assertIsNotNone(blog)

    def test_str(self):
        """test BlogPost.__str__ returns title
        """
        blog = BlogPost.objects.get(title='Test BlogPost')
        self.assertEqual(blog.__str__(), blog.title)

    def test_duplicate(self):
        """test duplicate BlogPosts get different slugs
        """
        blog1 = BlogPost.objects.get(title='Test BlogPost')
        blog2 = BlogPost(
            title=blog1.title,
            body=blog1.body,
            published=blog1.published,
        )
        blog2.save()
        self.assertEqual(blog1.title, blog2.title)
        self.assertNotEqual(blog1.slug, blog2.slug)

    def test_post_url(self):
        """test BlogPost urls are generated correctly
        """
        blog = BlogPost.objects.get(title='Test BlogPost')
        url = reverse(
            viewname='blog:post',
            subdomain='blog',
            kwargs={'blogpost': blog.slug, })
        self.assertEqual(blog.get_absolute_url(), url)

    def test_valid_post_url(self):
        """test BlogPost urls except valid keywords only
        """
        with self.assertRaises(NoReverseMatch):
            reverse(
                viewname='blog:post',
                subdomain='blog',
                kwargs={'blogpost': 'a!FQ#^VQ$!QC', })

    def test_save(self):
        """test BlogPost save() does not have unwanted side-effects
        """
        blog = BlogPost.objects.get(title='Test BlogPost')
        title = blog.title
        published = blog.published
        slug = blog.slug
        modified = blog.modified
        try:
            blog.save()
        except:
            self.fail('BlogPost save method raised an Exception.')
        else:
            self.assertEqual(blog.title, title)
            self.assertEqual(blog.published, published)
            self.assertEqual(blog.slug, slug)
            self.assertNotEqual(blog.modified, modified)

    def test_post_view(self):
        """test BlogPost view
        """
        blog = BlogPost.objects.get(slug=self.blog_slug)
        self.assertIsNotNone(blog)
        self.assertIsNotNone(blog.slug)
        url = reverse(
            viewname='blog:post',
            subdomain='blog',
            kwargs={'blogpost': blog.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_index_view(self):
        """test BlogPosts index view
        """
        url = reverse(
            viewname='blog:index',
            subdomain='blog')
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_nonexistant_blog_view(self):
        """test BlogPosts view with a non-existant blog
        """
        url = reverse(
            viewname='blog:post',
            subdomain='blog',
            kwargs={'blogpost': 'xyz', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

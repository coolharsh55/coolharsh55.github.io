"""Tests for Poems

"""

from django.core.urlresolvers import NoReverseMatch
from django.test import TestCase
from django.test import Client
from django.utils import timezone

from subdomains.utils import reverse

from sitedata.models import Tag

from .models import Poem

HTTP_HOST = 'poems.example.com'


class PoemsModelTest(TestCase):

    """Tests for Poem Models
    """

    def setUp(self):
        """create a test Poem
        """
        self.client = Client()
        tag = Tag(tagname='test tag')
        tag.save()
        poem = Poem(
            title='Test Poem',
            body='This is a test poem',
            published=timezone.now(),
        )
        poem.save()
        self.poem_slug = poem.slug
        poem.tags.add(tag)
        poem.save()
        self.assertIn(tag, poem.tags.all())

    def test_add_model(self):
        """test adding Poems
        """
        poem = Poem.objects.get(title='Test Poem')
        self.assertIsNotNone(poem)

    def test_str(self):
        """test Poem.__str__ returns title
        """
        poem = Poem.objects.get(title='Test Poem')
        self.assertEqual(poem.__str__(), poem.title)

    def test_duplicate(self):
        """test duplicate Poems get different slugs
        """
        poem1 = Poem.objects.get(title='Test Poem')
        poem2 = Poem(
            title=poem1.title,
            body=poem1.body,
            published=poem1.published,
        )
        poem2.save()
        self.assertEqual(poem1.title, poem2.title)
        self.assertNotEqual(poem1.slug, poem2.slug)

    def test_post_url(self):
        """test Poem urls are generated correctly
        """
        poem = Poem.objects.get(title='Test Poem')
        url = reverse(
            viewname='poems:post',
            subdomain='poems',
            kwargs={'poem': poem.slug, })
        self.assertEqual(poem.get_absolute_url(), url)

    def test_valid_post_url(self):
        """test Poem urls except valid keywords only
        """
        with self.assertRaises(NoReverseMatch):
            reverse(
                viewname='poems:post',
                subdomain='poem',
                kwargs={'poem': 'a!FQ#^VQ$!QC', })

    def test_save(self):
        """test Poem save() does not have unwanted side-effects
        """
        poem = Poem.objects.get(title='Test Poem')
        title = poem.title
        published = poem.published
        slug = poem.slug
        modified = poem.modified
        try:
            poem.save()
        except:
            self.fail('Poem save method raised an Exception.')
        else:
            self.assertEqual(poem.title, title)
            self.assertEqual(poem.published, published)
            self.assertEqual(poem.slug, slug)
            self.assertNotEqual(poem.modified, modified)

    def test_post_view(self):
        """test Poem view
        """
        poem = Poem.objects.get(slug=self.poem_slug)
        self.assertIsNotNone(poem)
        self.assertIsNotNone(poem.slug)
        url = reverse(
            viewname='poems:post',
            subdomain='poem',
            kwargs={'poem': poem.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_index_view(self):
        """test Poems index view
        """
        url = reverse(
            viewname='poems:index',
            subdomain='poem')
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_nonexistant_poem_view(self):
        """test Poems view with a non-existant poem
        """
        url = reverse(
            viewname='poems:post',
            subdomain='poems',
            kwargs={'poem': 'xyz', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

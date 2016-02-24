"""Tests for Stories

"""

from django.core.urlresolvers import NoReverseMatch
from django.test import TestCase
from django.test import Client
from django.utils import timezone

from subdomains.utils import reverse

from sitedata.models import Tag

from .models import StoryPost

HTTP_HOST = 'stories.example.com'


class StoryPostsModelTest(TestCase):

    """Tests for StoryPost Models
    """

    def setUp(self):
        """create a test StoryPost
        """
        self.client = Client()
        tag = Tag(tagname='test tag')
        tag.save()
        story = StoryPost(
            title='Test StoryPost',
            body='This is a test story',
            published=timezone.now(),
        )
        story.save()
        self.story_slug = story.slug
        story.tags.add(tag)
        story.save()
        self.assertIn(tag, story.tags.all())

    def test_add_model(self):
        """test adding StoryPosts
        """
        story = StoryPost.objects.get(title='Test StoryPost')
        self.assertIsNotNone(story)

    def test_str(self):
        """test StoryPost.__str__ returns title
        """
        story = StoryPost.objects.get(title='Test StoryPost')
        self.assertEqual(story.__str__(), story.title)

    def test_duplicate(self):
        """test duplicate StoryPosts get different slugs
        """
        story1 = StoryPost.objects.get(title='Test StoryPost')
        story2 = StoryPost(
            title=story1.title,
            body=story1.body,
            published=story1.published,
        )
        story2.save()
        self.assertEqual(story1.title, story2.title)
        self.assertNotEqual(story1.slug, story2.slug)

    def test_post_url(self):
        """test StoryPost urls are generated correctly
        """
        story = StoryPost.objects.get(title='Test StoryPost')
        url = reverse(
            viewname='stories:post',
            subdomain='stories',
            kwargs={'story': story.slug, })
        self.assertEqual(story.get_absolute_url(), url)

    def test_valid_post_url(self):
        """test StoryPost urls except valid keywords only
        """
        with self.assertRaises(NoReverseMatch):
            reverse(
                viewname='stories:post',
                subdomain='story',
                kwargs={'story': 'a!FQ#^VQ$!QC', })

    def test_save(self):
        """test StoryPost save() does not have unwanted side-effects
        """
        story = StoryPost.objects.get(title='Test StoryPost')
        title = story.title
        published = story.published
        slug = story.slug
        modified = story.modified
        try:
            story.save()
        except:
            self.fail('StoryPost save method raised an Exception.')
        else:
            self.assertEqual(story.title, title)
            self.assertEqual(story.published, published)
            self.assertEqual(story.slug, slug)
            self.assertNotEqual(story.modified, modified)

    def test_post_view(self):
        """test StoryPost view
        """
        story = StoryPost.objects.get(slug=self.story_slug)
        self.assertIsNotNone(story)
        self.assertIsNotNone(story.slug)
        url = reverse(
            viewname='stories:post',
            subdomain='story',
            kwargs={'story': story.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_index_view(self):
        """test StoryPosts index view
        """
        url = reverse(
            viewname='stories:index',
            subdomain='story')
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_nonexistant_story_view(self):
        """test StoryPosts view with a non-existant story
        """
        url = reverse(
            viewname='stories:post',
            subdomain='story',
            kwargs={'story': 'xyz', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

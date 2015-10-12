"""tests for BrainBank

"""

from django.test import Client
from django.test import TestCase
from django.utils.timezone import now as time_now

from django_seed import Seed
from subdomains.utils import reverse

from sitedata.models import Tag

from .models import BrainBankIdea
from .models import BrainBankPost
from .models import BrainBankDemo

HTTP_HOST = 'brainbank.example.com'


class BrainBankAIdeaTests(TestCase):

    """tests for BrainBank Ideas
    """

    def setUp(self):
        """setup brainbank ideas for tests
        """
        self.client = Client()
        self.seeder = Seed.seeder()
        self.seeder.add_entity(BrainBankIdea, 10)
        self.seeder.execute()

    def tearDown(self):
        """clean up after tests
        """
        BrainBankIdea.objects.all().delete()

    def test_idea_view(self):
        """test brainbank index view
        """
        idea = BrainBankIdea.objects.order_by('-published')[0]
        url = reverse(
            viewname='brainbank:idea',
            subdomain='brainbank',
            kwargs={'idea': idea.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['idea'], idea)
        self.assertEqual(response.context['page_url'], url)
        self.assertIsNotNone(response.context['meta'])

    def test_str(self):
        """test str for brainbank ideas
        """
        idea = BrainBankIdea.objects.order_by('-published')[0]
        self.assertEqual(idea.title, idea.__str__())

    def test_url(self):
        """test brainbank idea url
        """
        idea = BrainBankIdea.objects.order_by('-published')[0]
        url = reverse(
            viewname='brainbank:idea',
            subdomain='brainbank',
            kwargs={'idea': idea.slug, })
        self.assertIsNotNone(url)
        self.assertEqual(idea.get_absolute_url(), url)

    def test_duplicates(self):
        """test duplicate brainbank ideas do not have the same slug
        """
        idea1 = BrainBankIdea.objects.order_by('-published')[0]
        idea2 = BrainBankIdea()
        idea2.title = idea1.title
        idea2.published = time_now()
        idea2.save()
        self.assertIsNotNone(idea2.slug)
        self.assertNotEqual(idea1.slug, idea2.slug)
        slug = idea2.slug
        idea2.save()
        self.assertEqual(idea2.slug, slug)

    def test_doesnotexist(self):
        """test nonexistant ideas return 404
        """
        url = reverse(
            viewname='brainbank:idea',
            subdomain='brainbank',
            kwargs={'idea': 'randomnonexistantidea', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)


class BrainBankPostTests(TestCase):

    """tests for BrainBank Posts
    """

    def setUp(self):
        """setup brainbank posts for tests
        """
        self.client = Client()
        self.seeder = Seed.seeder()
        self.seeder.add_entity(BrainBankIdea, 10)
        self.seeder.add_entity(BrainBankPost, 10)
        self.seeder.execute()

    def test_post_view(self):
        """test brainbank index view
        """
        post = BrainBankPost.objects.order_by('-published')[0]
        url = reverse(
            viewname='brainbank:post',
            subdomain='brainbank',
            kwargs={'idea': post.idea.slug, 'post': post.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], post)
        self.assertEqual(response.context['page_url'], url)
        self.assertIsNotNone(response.context['meta'])

    def test_str(self):
        """test str for brainbank posts
        """
        post = BrainBankPost.objects.order_by('-published')[0]
        self.assertTrue(post.title in post.__str__())
        self.assertTrue(post.idea.title in post.__str__())

    def test_url(self):
        """test brainbank post url
        """
        post = BrainBankPost.objects.order_by('-published')[0]
        url = reverse(
            viewname='brainbank:post',
            subdomain='brainbank',
            kwargs={'idea': post.idea.slug, 'post': post.slug, })
        self.assertIsNotNone(url)
        self.assertEqual(post.get_absolute_url(), url)

    def test_duplicates(self):
        """test duplicate brainbank posts do not have the same slug
        """
        post1 = BrainBankPost.objects.order_by('-published')[0]
        post2 = BrainBankPost()
        post2.title = post1.title
        post2.body = post1.body
        post2.published = time_now()
        post2.slug = post1.slug
        post2.idea = post1.idea
        post2.save()
        self.assertIsNotNone(post2.slug)
        self.assertNotEqual(post1.slug, post2.slug)
        slug = post2.slug
        post2.save()
        self.assertEqual(post2.slug, slug)

    def test_doesnotexist(self):
        """test nonexistant posts return 404
        """
        url = reverse(
            viewname='brainbank:post',
            subdomain='brainbank',
            kwargs={'idea': 'randomidea', 'post': 'randompost', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

    def test_tags(self):
        """test posts have tags
        """
        self.seeder.add_entity(Tag, 10)
        inserts = self.seeder.execute()[Tag]
        tags = Tag.objects.filter(tagid__in=inserts)
        post = BrainBankPost.objects.order_by('-published')[0]
        for tag in tags:
            post.tags.add(tag)
        post.save()
        for tag in post.tags.all():
            self.assertTrue(tag in tags)

    def test_tags_in_view(self):
        """test post tags are added to keywords
        """
        tags = Tag.objects.all()[:10]
        post = BrainBankPost.objects.order_by('-published')[0]
        for tag in tags:
            if tag not in post.tags.all():
                post.tags.add(tag)
        post.save()
        url = reverse(
            viewname='brainbank:post',
            subdomain='brainbank',
            kwargs={'idea': post.idea.slug, 'post': post.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        response_tags = response.context['meta']['keywords']
        tagnames = [tag.tagname for tag in tags]
        for tagname in tagnames:
            self.assertTrue(tagname in response_tags)


class BrainBankCDemoTests(TestCase):

    """tests for BrainBank Demos
    """

    def setUp(self):
        """setup brainbank demos for tests
        """
        self.client = Client()
        self.seeder = Seed.seeder()
        self.seeder.add_entity(BrainBankIdea, 10)
        self.seeder.add_entity(BrainBankDemo, 10)
        self.seeder.execute()

    def test_demo_view(self):
        """test brainbank index view
        """
        demo = BrainBankDemo.objects.order_by('-published')[0]
        url = reverse(
            viewname='brainbank:demo',
            subdomain='brainbank',
            kwargs={'idea': demo.idea.slug, 'demo': demo.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['demo'], demo)
        self.assertEqual(response.context['page_url'], url)
        self.assertIsNotNone(response.context['meta'])

    def test_str(self):
        """test str for brainbank demos
        """
        demo = BrainBankDemo.objects.order_by('-published')[0]
        self.assertTrue(demo.title in demo.__str__())
        self.assertTrue(demo.idea.title in demo.__str__())

    def test_url(self):
        """test brainbank demo url
        """
        demo = BrainBankDemo.objects.order_by('-published')[0]
        url = reverse(
            viewname='brainbank:demo',
            subdomain='brainbank',
            kwargs={'idea': demo.idea.slug, 'demo': demo.slug, })
        self.assertIsNotNone(url)
        self.assertEqual(demo.get_absolute_url(), url)

    def test_duplicates(self):
        """test duplicate brainbank demos do not have the same slug
        """
        demo1 = BrainBankDemo.objects.order_by('-published')[0]
        demo2 = BrainBankDemo()
        fields = [(k, v) for k, v in demo1.__dict__.items() if k != 'id']
        demo2.__dict__.update(fields)
        demo2.save()
        self.assertIsNotNone(demo2.slug)
        self.assertNotEqual(demo1.slug, demo2.slug)
        slug = demo2.slug
        demo2.save()
        self.assertEqual(demo2.slug, slug)

    def test_doesnotexist(self):
        """test nonexistant demos return 404
        """
        url = reverse(
            viewname='brainbank:demo',
            subdomain='brainbank',
            kwargs={'idea': 'randomidea', 'demo': 'randomdemo', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

    def test_tags(self):
        """test demos have tags
        """
        self.seeder.add_entity(Tag, 10)
        inserts = self.seeder.execute()[Tag]
        tags = Tag.objects.filter(tagid__in=inserts)
        demo = BrainBankDemo.objects.order_by('-published')[0]
        for tag in tags:
            demo.tags.add(tag)
        demo.save()
        for tag in demo.tags.all():
            self.assertTrue(tag in tags)

    def test_tags_in_view(self):
        """test demo tags are added to keywords
        """
        tags = Tag.objects.all()[:10]
        demo = BrainBankDemo.objects.order_by('-published')[0]
        for tag in tags:
            if tag not in demo.tags.all():
                demo.tags.add(tag)
        demo.save()
        url = reverse(
            viewname='brainbank:demo',
            subdomain='brainbank',
            kwargs={'idea': demo.idea.slug, 'demo': demo.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        response_tags = response.context['meta']['keywords']
        tagnames = [tag.tagname for tag in tags]
        for tagname in tagnames:
            self.assertTrue(tagname in response_tags)


class BrainBankIndexTest(TestCase):

    """tests for brainbank index
    """

    def test_index_view(self):
        """test brainbank index view
        """
        ideas = list(BrainBankIdea.objects.order_by('-published'))
        url = reverse(
            viewname='brainbank:index',
            subdomain='brainbank')
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        response_ideas = list(response.context['ideas'])
        self.assertListEqual(ideas, response_ideas)

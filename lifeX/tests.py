"""Tests for LifeX

"""

from datetime import datetime
from django.test import Client
from django.test import TestCase
from django.utils.timezone import now as time_now
from django.utils.timezone import timedelta
from random import randint

from django_seed import Seed
from subdomains.utils import reverse

from sitedata.models import Tag

from .models import LIFEX_START_DATE
from .models import LifeXBlog
from .models import LifeXCategory
from .models import LifeXIdea
from .models import LifeXPost
from .models import LifeXWeek

HTTP_HOST = 'lifex.example.com'


class LifeXDatesTest(TestCase):

    """tests for lifeX significant dates
    """

    def test_start_date(self):
        """test start week for lifeX
        """
        start_date = datetime(2014, 03, 24)
        self.assertEqual(start_date, LIFEX_START_DATE)


class LifeXWeekTest(TestCase):

    """tests for lifeX weeks
    """

    def setUp(self):
        """setup tests for lifeX weeks
        """
        self.client = Client()
        self.seeder = Seed.seeder()
        self.seeder.add_entity(LifeXWeek, 10)
        self.seeder.execute()

    def tearDown(self):
        """clean up after tests
        """
        LifeXWeek.objects.all().delete()
        LifeXCategory.objects.all().delete()
        LifeXIdea.objects.all().delete()
        LifeXPost.objects.all().delete()
        LifeXBlog.objects.all().delete()

    def test_save(self):
        """test saving weeks
        """
        week = LifeXWeek()
        last_week_no = LifeXWeek.objects.order_by('-number')[0].number + 1
        week.save()
        self.assertEqual(week.number, last_week_no)

    def test_str(self):
        """test week returns start and end dates in str
        """
        week = LifeXWeek.objects.all()[
            randint(0, LifeXWeek.objects.count() - 1)
        ]
        self.assertTrue(week._start_week() in week.__str__())
        self.assertTrue(week._end_week() in week.__str__())

    def test_start_of_week(self):
        """test starting date of week
        """
        week = LifeXWeek.objects.all()[
            randint(0, LifeXWeek.objects.count() - 1)
        ]
        start_date = LIFEX_START_DATE + timedelta(weeks=week.number - 1)
        self.assertEqual(LifeXWeek.str_week(start_date), week._start_week())

    def test_end_of_week(self):
        """test ending date of week
        """
        week = LifeXWeek.objects.all()[
            randint(0, LifeXWeek.objects.count() - 1)
        ]
        end_date = LIFEX_START_DATE + timedelta(weeks=week.number - 1)
        self.assertEqual(LifeXWeek.str_week(end_date), week._start_week())

    def test_string_repr_of_week(self):
        """test string representation of week
        """
        week_date = LIFEX_START_DATE + timedelta(randint(0, 500))
        str_week = week_date.strftime('%d-%b-%Y')
        self.assertEqual(LifeXWeek.str_week(week_date), str_week)

    def test_abs_url(self):
        """test absolute url for the week
        """
        week = LifeXWeek.objects.all()[
            randint(0, LifeXWeek.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:week',
            subdomain='lifex',
            kwargs={'week': week.number, })
        self.assertEqual(url, week.get_absolute_url())

    def test_url(self):
        """test url of week
        """
        week = LifeXWeek.objects.all()[
            randint(0, LifeXWeek.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:week',
            subdomain='lifex',
            kwargs={'week': week.number, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

        url = reverse(
            viewname='lifeX:experiments',
            subdomain='lifex',)
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_week_index_view(self):
        """test index view for week
        """
        url = reverse(
            viewname='lifeX:experiments',
            subdomain='lifex',)
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        response_weeks = list(response.context['weeks'])
        weeks = list(LifeXWeek.objects.order_by('-number'))
        self.assertListEqual(response_weeks, weeks)

    def test_week_view(self):
        """test week view
        """
        week = LifeXWeek.objects.all()[
            randint(0, LifeXWeek.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:week',
            subdomain='lifex',
            kwargs={'week': week.number, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        response_week = response.context['week']
        self.assertEqual(response_week, week)

    def test_404(self):
        """test 404 for nonexistant weeks
        """
        week_no = LifeXWeek.objects.all().count() + 1
        url = reverse(
            viewname='lifeX:week',
            subdomain='lifex',
            kwargs={'week': week_no, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)


class LifeXCategoryTest(TestCase):

    """tests for LifeX Categories
    """

    def setUp(self):
        """setup tests for lifeX categories
        """
        self.client = Client()
        self.seeder = Seed.seeder()
        self.seeder.add_entity(LifeXCategory, 10)
        self.seeder.execute()

    def tearDown(self):
        """clean up after tests
        """
        LifeXWeek.objects.all().delete()
        LifeXCategory.objects.all().delete()
        LifeXIdea.objects.all().delete()
        LifeXPost.objects.all().delete()
        LifeXBlog.objects.all().delete()

    def test_save(self):
        """test saving categories
        """
        category = LifeXCategory()
        category.name = 'somerandomcategoryname'
        category.save()
        self.assertIsNotNone(category.pk)
        self.assertIsNotNone(category.slug)
        category.save()

    def test_str(self):
        """test category returns start and end dates in str
        """
        category = LifeXCategory.objects.all()[
            randint(0, LifeXCategory.objects.count() - 1)
        ]
        self.assertTrue(category.name in category.__str__())

    def test_abs_url(self):
        """test absolute url of category
        """
        category = LifeXCategory.objects.all()[
            randint(0, LifeXCategory.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:category',
            subdomain='lifex',
            kwargs={'category': category.slug, })
        self.assertEqual(url, category.get_absolute_url())

    def test_url(self):
        """test url of category
        """
        url = reverse(
            viewname='lifeX:ideas',
            subdomain='lifex',)
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

        category = LifeXCategory.objects.all()[
            randint(0, LifeXCategory.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:category',
            subdomain='lifex',
            kwargs={'category': category.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_category_ideas_view(self):
        """test ideas view for category
        """
        url = reverse(
            viewname='lifeX:ideas',
            subdomain='lifex',)
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        response_categories = list(response.context['categories'])
        categories = list(LifeXCategory.objects.order_by('name'))
        self.assertListEqual(response_categories, categories)

    def test_category_view(self):
        """test category view
        """
        category = LifeXCategory.objects.all()[
            randint(0, LifeXCategory.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:category',
            subdomain='lifex',
            kwargs={'category': category.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        response_category = response.context['category']
        self.assertEqual(response_category, category)

    def test_404(self):
        """test 404 for nonexistant categories
        """
        url = reverse(
            viewname='lifeX:category',
            subdomain='lifex',
            kwargs={'category': 'somerandomcategory', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)


class LifeXIdeaTest(TestCase):

    """tests for LifeX Categories
    """

    def setUp(self):
        """setup tests for lifeX ideas
        """
        self.client = Client()
        self.seeder = Seed.seeder()
        self.seeder.add_entity(LifeXCategory, 10)
        self.seeder.add_entity(LifeXIdea, 10)
        self.seeder.execute()

    def tearDown(self):
        """clean up after tests
        """
        LifeXWeek.objects.all().delete()
        LifeXCategory.objects.all().delete()
        LifeXIdea.objects.all().delete()
        LifeXPost.objects.all().delete()
        LifeXBlog.objects.all().delete()

    def test_save(self):
        """test saving ideas
        """
        idea = LifeXIdea()
        # idea.title = 'somerandomideaname'
        category = LifeXCategory.objects.all()[
            randint(0, LifeXCategory.objects.count() - 1)
        ]
        idea.category = category
        idea.save()
        self.assertIsNotNone(idea.pk)
        self.assertIsNotNone(idea.slug)
        idea.save()

    def test_str(self):
        """test idea returns start and end dates in str
        """
        def test_idea_str(idea):
            """repetitive tests for idea_str
            """
            if idea.retry:
                self.assertTrue('(try again) ' in idea.__str__())
            elif idea.experimented:
                self.assertTrue('(tried) ' in idea.__str__())
            else:
                self.assertTrue('(todo) ' in idea.__str__())

        idea = LifeXIdea.objects.all()[
            randint(0, LifeXIdea.objects.count() - 1)
        ]
        self.assertTrue(idea.title in idea.__str__())
        idea.retry = True
        test_idea_str(idea)
        idea.retry = False
        idea.experimented = True
        test_idea_str(idea)
        idea.experimented = False
        test_idea_str(idea)

    def test_abs_url(self):
        """test absolute url of idea
        """
        idea = LifeXIdea.objects.all()[
            randint(0, LifeXIdea.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:idea',
            subdomain='lifex',
            kwargs={'category': idea.category.slug, 'idea': idea.slug, })
        self.assertEqual(url, idea.get_absolute_url())

    def test_url(self):
        """test url of idea
        """
        idea = LifeXIdea.objects.all()[
            randint(0, LifeXIdea.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:idea',
            subdomain='lifex',
            kwargs={'category': idea.category.slug, 'idea': idea.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_idea_idea_view(self):
        """test idea view
        """
        idea = LifeXIdea.objects.all()[
            randint(0, LifeXIdea.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:idea',
            subdomain='lifex',
            kwargs={'category': idea.category.slug, 'idea': idea.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        response_idea = response.context['idea']
        self.assertEqual(response_idea, idea)

    def test_404(self):
        """test 404 for non-existant ideas
        """
        # 404 idea
        category = LifeXCategory.objects.all()[
            randint(0, LifeXIdea.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:idea',
            subdomain='lifex',
            kwargs={'category': category.slug, 'idea': 'somerandomidea', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

        # 404 category
        idea = LifeXIdea.objects.all()[
            randint(0, LifeXIdea.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:idea',
            subdomain='lifex',
            kwargs={'category': 'somerandomcategory', 'idea': idea.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)


class LifeXPostTest(TestCase):

    """tests for LifeX Categories
    """

    def setUp(self):
        """setup tests for lifeX posts
        """
        self.client = Client()
        self.seeder = Seed.seeder()
        self.seeder.add_entity(LifeXWeek, 10)
        self.seeder.add_entity(LifeXCategory, 10)
        self.seeder.add_entity(LifeXIdea, 10)
        self.seeder.execute()
        weeks = LifeXWeek.objects.all()
        ideas = LifeXIdea.objects.all()
        for i in range(0, 10):
            post = LifeXPost()
            post.title = 'random title #%s' % i
            post.body = 'random body'
            post.published = time_now()
            post.week = weeks[
                randint(0, len(weeks) - 1)]
            post.idea = ideas[
                randint(0, len(ideas) - 1)]
            post.save()

    def tearDown(self):
        """clean up after tests
        """
        LifeXWeek.objects.all().delete()
        LifeXCategory.objects.all().delete()
        LifeXIdea.objects.all().delete()
        LifeXPost.objects.all().delete()
        LifeXBlog.objects.all().delete()

    def test_save(self):
        """test saving posts
        """
        post = LifeXPost()
        post.name = 'somerandompostname'
        post.published = time_now()
        post.idea = LifeXIdea.objects.all()[0]
        post.week = LifeXWeek.objects.all()[0]
        post.save()
        self.seeder.add_entity(Tag, 10)
        self.seeder.execute()
        for tag in Tag.objects.all():
            post.tags.add(tag)
        self.assertIsNotNone(post.pk)
        self.assertIsNotNone(post.slug)

    def test_duplicate(self):
        """test duplicate posts
        """
        post1 = LifeXPost()
        post1.title = 'somerandompostname'
        post1.published = time_now()
        post1.idea = LifeXIdea.objects.all()[0]
        post1.week = LifeXWeek.objects.all()[0]
        post1.save()
        self.assertIsNotNone(post1.pk)
        self.assertIsNotNone(post1.slug)
        post2 = LifeXPost()
        post2.title = post1.title
        post2.published = post1.published
        post2.idea = post1.idea
        post2.week = post1.week
        with self.assertRaises(AssertionError):
            post2.save()

    def test_str(self):
        """test post returns start and end dates in str
        """
        post = LifeXPost.objects.all()[
            randint(0, LifeXPost.objects.count() - 1)
        ]
        self.assertTrue(post.title in post.__str__())
        self.assertTrue(str(post.week.number) in post.__str__())

    def test_abs_url(self):
        """test absolute url for post
        """
        post = LifeXPost.objects.all()[
            randint(0, LifeXPost.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:post',
            subdomain='lifex',
            kwargs={'week': post.week.number, 'idea': post.idea.slug})
        self.assertEqual(url, post.get_absolute_url())

    def test_url(self):
        """test url of post
        """
        post = LifeXPost.objects.all()[
            randint(0, LifeXPost.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:post',
            subdomain='lifex',
            kwargs={'week': post.week.number, 'idea': post.idea.slug})
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_post_view(self):
        """test post view
        """
        posts = LifeXPost.objects.exclude(tags=None).all()
        if not posts:
            post = LifeXPost.objects.all()[
                randint(0, LifeXPost.objects.count() - 1)
            ]
            self.seeder.add_entity(Tag, 10)
            self.seeder.execute()
            for tag in Tag.objects.all():
                post.tags.add(tag)
            post.save()
        else:
            post = posts[randint(0, len(posts) - 1)]

        url = reverse(
            viewname='lifeX:post',
            subdomain='lifex',
            kwargs={'week': post.week.number, 'idea': post.idea.slug})
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        response_post = response.context['post']
        self.assertEqual(response_post, post)

    def test_404(self):
        """test 404 for nonexistant posts
        """
        # 404 week
        idea = LifeXIdea.objects.all()[
            randint(0, LifeXIdea.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:post',
            subdomain='lifex',
            kwargs={'week': 0, 'idea': idea.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

        # 404 idea
        week = LifeXWeek.objects.all()[
            randint(0, LifeXWeek.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:post',
            subdomain='lifex',
            kwargs={'week': week.number, 'idea': 'somerandomidea', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

        # 404 idea
        week = LifeXWeek.objects.all()[
            randint(0, LifeXWeek.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:post',
            subdomain='lifex',
            kwargs={'week': week.number, 'idea': 'somerandomidea', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

        # 404 idea exists, but not in given week
        week = LifeXWeek.objects.all()[
            randint(0, LifeXWeek.objects.count() - 1)
        ]
        posts_in_week = week.lifexpost_set.all()
        ideas_in_week = [post.idea.pk for post in posts_in_week]
        ideas = LifeXIdea.objects.exclude(pk__in=ideas_in_week)
        if len(ideas) == 0:
            # there's nothing to test here
            return
        url = reverse(
            viewname='lifeX:post',
            subdomain='lifex',
            kwargs={'week': week.number, 'idea': ideas[0].slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)


class LifeXBlogTest(TestCase):

    """tests for LifeX Categories
    """

    def setUp(self):
        """setup tests for lifeX blogs
        """
        self.client = Client()
        self.seeder = Seed.seeder()
        self.seeder.add_entity(Tag, 10)
        self.seeder.execute()
        self.seeder.add_entity(LifeXBlog, 10)
        self.seeder.execute()

    def tearDown(self):
        """clean up after tests
        """
        LifeXWeek.objects.all().delete()
        LifeXCategory.objects.all().delete()
        LifeXIdea.objects.all().delete()
        LifeXPost.objects.all().delete()
        LifeXBlog.objects.all().delete()

    def test_save(self):
        """test saving blogs
        """
        blog = LifeXBlog()
        blog.title = 'somerandomblogtitle'
        blog.published = time_now()
        blog.save()
        self.assertIsNotNone(blog.pk)
        self.assertIsNotNone(blog.slug)

    def test_duplicate(self):
        """test duplicate blogs
        """
        blog1 = LifeXBlog()
        blog1.title = 'somerandomblogname'
        blog1.published = time_now()
        blog1.save()
        self.assertIsNotNone(blog1.pk)
        self.assertIsNotNone(blog1.slug)
        blog2 = LifeXBlog()
        blog2.title = blog1.title
        blog2.save()
        self.assertIsNotNone(blog2.pk)
        self.assertIsNotNone(blog2.slug)
        self.assertEqual(blog1.title, blog2.title)
        self.assertNotEqual(blog1.slug, blog2.slug)

    def test_str(self):
        """test blog returns start and end dates in str
        """
        blog = LifeXBlog.objects.all()[
            randint(0, LifeXBlog.objects.count() - 1)
        ]
        self.assertTrue(blog.title in blog.__str__())

    def test_abs_url(self):
        """test absolute url for blog
        """
        blog = LifeXBlog.objects.all()[
            randint(0, LifeXBlog.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:blogpost',
            subdomain='lifex',
            kwargs={'blogpost': blog.slug, })
        self.assertEqual(url, blog.get_absolute_url())

    def test_url(self):
        """test url of blog
        """
        url = reverse(
            viewname='lifeX:blog',
            subdomain='lifex',)
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

        blog = LifeXBlog.objects.all()[
            randint(0, LifeXBlog.objects.count() - 1)
        ]
        url = reverse(
            viewname='lifeX:blogpost',
            subdomain='lifex',
            kwargs={'blogpost': blog.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_blog_index_view(self):
        """test blogs view for blog
        """
        url = reverse(
            viewname='lifeX:blog',
            subdomain='lifex',)
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        response_blogs = list(response.context['blogposts'])
        blogs = list(LifeXBlog.objects.order_by('-published'))
        self.assertListEqual(response_blogs, blogs)

    def test_blog_view(self):
        """test blog view
        """
        blog = LifeXBlog.objects.all()[
            randint(0, LifeXBlog.objects.count() - 1)
        ]
        self.seeder.add_entity(Tag, 10)
        self.seeder.execute()
        for tag in Tag.objects.all():
            blog.tags.add(tag)
        blog.save()

        url = reverse(
            viewname='lifeX:blogpost',
            subdomain='lifex',
            kwargs={'blogpost': blog.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        response_blog = response.context['post']
        self.assertEqual(response_blog, blog)

    def test_404(self):
        """test 404 for non-existant blogs
        """
        url = reverse(
            viewname='lifeX:blogpost',
            subdomain='lifex',
            kwargs={'blogpost': 'somerandomblog', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)


class LifeXPresentationTest(TestCase):

    """tests for LifeX Presentation
    """

    def setUp(self):
        """setup tests for lifeX presentations
        """
        self.client = Client()

    def test_presentation_url(self):
        """test lifeX presentation url
        """
        url = reverse(
            viewname='lifeX:lifeX_presentation_UCC2014',
            subdomain='lifex')
        self.assertIsNotNone(url)

    def test_presentation_view(self):
        """test lifeX presentation view
        """
        url = reverse(
            viewname='lifeX:lifeX_presentation_UCC2014',
            subdomain='lifex')
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)


class LifeXIndexTest(TestCase):

    """tests for LifeX index
    """

    def setUp(self):
        """setup tests for lifeX index view
        """
        self.client = Client()

    def tearDown(self):
        """clean up after tests
        """
        LifeXWeek.objects.all().delete()
        LifeXCategory.objects.all().delete()
        LifeXIdea.objects.all().delete()
        LifeXPost.objects.all().delete()
        LifeXBlog.objects.all().delete()

    def test_index_url(self):
        """test lifeX index url
        """
        url = reverse(
            viewname='lifeX:index',
            subdomain='lifex')
        self.assertIsNotNone(url)

    def test_index_view(self):
        """test lifeX index view
        """
        seeder = Seed.seeder()
        seeder.add_entity(LifeXWeek, 10)
        seeder.execute()
        url = reverse(
            viewname='lifeX:index',
            subdomain='lifex')
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        latest_week = LifeXWeek.objects.latest('number')
        self.assertEqual(latest_week, response.context['latest_week'])

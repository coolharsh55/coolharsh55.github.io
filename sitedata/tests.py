"""Tests for Sitedata Models

"""

from django.core.urlresolvers import NoReverseMatch
from django.db import IntegrityError
from django.db import transaction
from django.test import Client
from django.test import TestCase
from django.utils.timezone import now as time_now
from django.utils.timezone import timedelta

from django_seed import Seed
from subdomains.utils import reverse

from articles.models import Article
from blog.models import BlogPost
from brainbank.models import BrainBankIdea
from brainbank.models import BrainBankPost
from hobbies.models import Book
from hobbies.models import Movie
from hobbies.models import TVShow
from hobbies.models import Game
from lifeX.models import LifeXCategory
from lifeX.models import LifeXIdea
from poems.models import Poem
from stories.models import StoryPost

from .forms import FeedbackForm
from .models import CSSLink
from .models import JSLink
from .models import Feedback
from .models import Tag
from .social_meta import create_meta
from .templatetags import dictionary
from .views import tagcount as tagcount_view

HTTP_HOST = 'example.com'


class TagModelTest(TestCase):

    """Tests for Tag Models
    """

    def setUp(self):
        """create a test Tag
        """
        self.client = Client()
        tag = Tag(tagname='test tag')
        tag.save()
        self.tag_slug = tag.slug

    def test_add_model(self):
        """test adding Tags
        """
        tag = Tag.objects.get(slug=self.tag_slug)
        self.assertIsNotNone(tag)

    def test_str(self):
        """test Tag.__str__ returns title
        """
        tag = Tag.objects.get(slug=self.tag_slug)
        self.assertEqual(tag.__str__(), tag.tagname)

    def test_duplicate(self):
        """test duplicate Tags get different slugs
        """
        tag1 = Tag.objects.get(slug=self.tag_slug)
        tag2 = Tag(tagname=tag1.tagname)
        with self.assertRaises(IntegrityError):
            tag2.save()

    def test_post_url(self):
        """test Tag urls are generated correctly
        """
        tag = Tag.objects.get(slug=self.tag_slug)
        url = reverse(
            viewname='sitedata:tagname',
            subdomain=None,
            kwargs={'tagname': tag.slug, })
        self.assertEqual(tag.get_absolute_url(), url)

    def test_valid_post_url(self):
        """test Tag urls except valid keywords only
        """
        with self.assertRaises(NoReverseMatch):
            reverse(
                viewname='sitedata:tagname',
                subdomain=None,
                kwargs={'tagname': 'a!FQ#^VQ$!QC', })

    def test_save(self):
        """test Tag save() does not have unwanted side-effects
        """
        tag = Tag.objects.get(slug=self.tag_slug)
        tagname = tag.tagname
        slug = tag.slug
        try:
            tag.save()
        except:
            self.fail('Tag save method raised an Exception.')
        else:
            self.assertEqual(tag.tagname, tagname)
            self.assertEqual(tag.slug, slug)

    def test_post_view(self):
        """test Tag view
        """
        tag = Tag.objects.get(slug=self.tag_slug)
        self.assertIsNotNone(tag)
        self.assertIsNotNone(tag.slug)
        url = reverse(
            viewname='sitedata:tagname',
            subdomain=None,
            kwargs={'tagname': tag.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_index_view(self):
        """test Tags index view
        """
        url = reverse(
            viewname='sitedata:tag_index',
            subdomain=None)
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)

    def test_nonexistant_tag_view(self):
        """test Tags view with a non-existant tag
        """
        url = reverse(
            viewname='sitedata:tagname',
            subdomain=None,
            kwargs={'tagname': 'xyz', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

    def test_tagcount(self):
        """test tagcount is correctly calculated
        """
        # create parent instances
        seeder = Seed.seeder()
        seeder.add_entity(LifeXCategory, 1)
        seeder.execute()
        tag_parents = [
            Article,
            BlogPost,
            BrainBankIdea,
            BrainBankPost,
            LifeXIdea,
            Book,
            Movie,
            TVShow,
            Game,
            Poem,
            StoryPost,
        ]
        for parent in tag_parents:
            seeder.add_entity(parent, 1)
        inserted = seeder.execute()
        # get tag object and attach to parent
        tag = Tag.objects.get(slug=self.tag_slug)
        for parent_class in inserted.keys():
            if parent_class not in tag_parents:
                continue
            parent = parent_class.objects.get(pk=inserted[parent_class][0])
            parent.tags.add(tag)
            parent.save()
        # assert tagcount from view
        self.assertEqual(len(tagcount_view(tag)), len(tag_parents))


class FeedbackTest(TestCase):

    """Tests for feedbacks on site
    """

    def setUp(self):
        """set up feedbacks in database for tests
        """
        self.client = Client()
        self.seeder = Seed.seeder()
        self.seeder.add_entity(Feedback, 10)
        self.seeder.execute()

    def tearDown(self):
        """clean up after tests
        """
        Feedback.objects.all().delete()

    def test_feedback_index_view(self):
        """test feedback index view and objects returned
        """
        feedbacks = list(Feedback.objects.order_by('-published'))
        url = reverse(
            viewname='sitedata:feedback_index',
            subdomain=None)
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        response_feedbacks = list(response.context['feedbacks'])
        self.assertListEqual(feedbacks, response_feedbacks)

    def test_feedback_view(self):
        """test feedback view and object returned
        """
        feedback = Feedback.objects.all()[0]
        self.assertIsNotNone(feedback)
        url = reverse(
            viewname='sitedata:feedback',
            subdomain=None,
            kwargs={'feedback_no': feedback.id, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        response_feedback = response.context['feedback']
        self.assertEqual(feedback, response_feedback)

    def test_feedback_duplicate(self):
        """test duplicate feedbacks are allowed
        """
        feedback1 = Feedback.objects.all()[0]
        feedback2 = Feedback()
        feedback2.title = feedback1.title
        feedback2.text = feedback1.text
        feedback2.published = feedback1.published
        feedback2.user_name = feedback1.user_name
        feedback2.user_email = feedback1.user_email
        feedback2.linked_post = feedback1.linked_post
        feedback2.reply = feedback1.reply
        feedback2.reply_date = feedback1.reply_date
        feedback2.save()
        self.assertNotEqual(feedback1.id, feedback2.id)

    def test_feedback_nonexistant(self):
        """test nonexistant feedbacks return 404
        """
        url = reverse(
            viewname='sitedata:feedback',
            subdomain=None,
            kwargs={'feedback_no': 0, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

    def test_feedback_url(self):
        """test feedback url is same as absolute url
        """
        feedback = Feedback.objects.all()[0]
        self.assertIsNotNone(feedback)
        url = reverse(
            viewname='sitedata:feedback',
            subdomain=None,
            kwargs={'feedback_no': feedback.id, })
        self.assertIsNotNone(url)
        self.assertEqual(feedback.get_absolute_url(), url)

    def test_feedback_form_add(self):
        """test adding feedback via form
        """
        feedback = Feedback.objects.all()[0]
        self.assertIsNotNone(feedback)
        fields = {}
        for field in feedback._meta.get_fields():
            fields[field.name] = getattr(feedback, field.name)
        form = FeedbackForm(fields)
        self.assertTrue(form.is_valid())

    def test_feedback_form_add_view(self):
        """test feedback form add view
        """
        feedback = Feedback.objects.all()[0]
        self.assertIsNotNone(feedback)
        fields = {}
        for field in feedback._meta.get_fields():
            fields[field.name] = getattr(feedback, field.name)
        url = reverse(
            viewname='sitedata:feedback_add',
            subdomain=None,
            args=(None, ))
        self.assertIsNotNone(url)
        response = self.client.post(url, fields)
        self.assertEqual(response.status_code, 302)

    def test_feedback_form_view(self):
        """test feedback form view
        """
        url = reverse(
            viewname='sitedata:feedback_add',
            subdomain=None,
            args=('test', ))
        self.assertIsNotNone(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_feedback_form_view_without_url(self):
        """test feedback form view without url parameter
        """
        url = reverse(
            viewname='sitedata:feedback_add',
            subdomain=None,
            args=('', ))
        self.assertIsNotNone(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_feedback_form_add_invalid_view(self):
        """test feedback does not accept invalid forms
        """
        fields = {}
        url = reverse(
            viewname='sitedata:feedback_add',
            subdomain=None,
            kwargs={'url': None, })
        self.assertIsNotNone(url)
        response = self.client.post(url, fields)
        self.assertEqual(response.status_code, 400)

    def test_feedback_add_without_reply(self):
        """test add feedback without reply
        """
        feedback = Feedback.objects.all()[0]
        self.assertIsNotNone(feedback)
        fields = {}
        for field in feedback._meta.get_fields():
            if not field.name.startswith('reply'):
                fields[field.name] = getattr(feedback, field.name)
        form = FeedbackForm(fields)
        self.assertTrue(form.is_valid())
        feedback = form.save()
        self.assertIsNotNone(feedback)

    def test_feedback_with_anonymous_user(self):
        """testadd feedback without user name
        """
        feedback = Feedback.objects.all()[0]
        self.assertIsNotNone(feedback)
        fields = {}
        for field in feedback._meta.get_fields():
            if not field.name.startswith('reply'):
                fields[field.name] = getattr(feedback, field.name)
        form = FeedbackForm(fields)
        self.assertTrue(form.is_valid())
        feedback = form.save()
        self.assertIsNotNone(feedback)
        feedback.reply = 'new reply'
        feedback.save()
        self.assertIsNotNone(feedback.reply_date)

    def test_feedback_reply(self):
        """test replying to saved feedback
        """
        feedback = Feedback.objects.all()[0]
        self.assertIsNotNone(feedback)
        fields = {}
        for field in feedback._meta.get_fields():
            if not field.name.startswith('user'):
                fields[field.name] = getattr(feedback, field.name)
        form = FeedbackForm(fields)
        self.assertTrue(form.is_valid())
        feedback = form.save()
        self.assertEqual(feedback.user_name, 'Anonymous')


class SocialMetaTest(TestCase):

    """Tests for social meta tags
    """

    def setUp(self):
        """set up tests for meta tags
        """
        pass

    def set_meta_tags(self):
        """simulate meta tags stored in settings
        """
        from django.conf import settings
        setattr(settings, 'META_USE_OG_PROPERTIES', True)
        setattr(settings, 'META_USE_TWITTER_PROPERTIES', True)
        setattr(settings, 'META_USE_GOOGLEPLUS_PROPERTIES', True)

    def unset_meta_tags(self):
        """simulate meta tags removed from settings
        """
        from django.conf import settings
        setattr(settings, 'META_USE_OG_PROPERTIES', False)
        setattr(settings, 'META_USE_TWITTER_PROPERTIES', False)
        setattr(settings, 'META_USE_GOOGLEPLUS_PROPERTIES', False)

    def test_meta_tags_are_set(self):
        """test meta tags are generated
        """
        # get meta
        self.set_meta_tags()
        meta = create_meta(
            title='title',
            description='description',
            keywords=['one', 'two', 'three'],
            url='http://example.com',
            image='http://example.com',
        )
        # check meta tags are set
        self.assertIsNotNone(meta)
        self.assertTrue(meta['use_og'])
        self.assertTrue(meta['use_facebook'])
        self.assertTrue(meta['use_twitter'])
        self.assertTrue(meta['use_googleplus'])
        # check meta tag values
        self.assertEqual(meta['twitter_site'], 'coolharsh55')
        self.assertEqual(meta['twitter_creator'], 'coolharsh55')

    def test_meta_tags_are_unset(self):
        """test meta tags are generated
        """
        # get meta
        self.unset_meta_tags()
        meta = create_meta(
            title='title',
            description='description',
            keywords=['one', 'two', 'three'],
            url='http://example.com',
            image='http://example.com',
        )
        # check meta tags are set
        self.assertIsNotNone(meta)
        self.assertFalse(meta.get('use_og', False))
        self.assertFalse(meta.get('use_facebook', False))
        self.assertFalse(meta.get('use_twitter', False))
        self.assertFalse(meta.get('use_googleplus', False))

    def test_meta_parameters(self):
        """test meta parameters raise ValueError
        """
        kwargs = {
            'title': 'title',
            'description': 'description',
            'keywords': ['one', 'two', 'three'],
            'url': 'http://example.com',
        }
        for x in kwargs.keys():
            temp = kwargs[x]
            kwargs[x] = None
            with self.assertRaises(ValueError):
                create_meta(**kwargs)
            kwargs[x] = temp
        # test image does not raise ValueError
        kwargs['image'] = 'http://example.com'
        meta = create_meta(**kwargs)
        self.assertIsNotNone(meta)
        self.assertIsNotNone(meta.get('image', None))
        kwargs['image'] = None
        meta = create_meta(**kwargs)
        self.assertIsNotNone(meta)
        self.assertIsNone(meta.get('image', None))


class DictionaryTemplateTagTest(TestCase):

    """tests for template tag dictionary
    """

    def setUp(self):
        """set up tests for dictionary
        """
        pass

    def test_dict_val(self):
        """test getval returns dictionary keys
        """
        d = {'key': 'value', }
        self.assertEqual(dictionary.getval(d, 'key'), d['key'])

    def test_current_domain(self):
        """test dictionary gets current domain
        """
        domain = dictionary.current_domain()
        self.assertTrue(HTTP_HOST in domain)

    def test_classname(self):
        """test dictionary returns class name of object
        """
        obj = object()
        self.assertEqual(dictionary.classname(obj), obj.__class__.__name__)

    def test_url_encode(self):
        """test dictionary encodes urls
        """
        url = 'http://example.com/this+sample?url=for:tests/'
        url_encoded = dictionary.encode_safe(url)
        self.assertNotEqual(url, url_encoded)

    def test_reltime(self):
        """test reltime returns correct timedelta strings
        """
        time_slots = (
            ('min', timedelta(minutes=30)),
            ('hour', timedelta(hours=2)),
            ('day', timedelta(days=15)),
            ('month', timedelta(weeks=15)),
            ('year', timedelta(weeks=150)),
        )
        for timeslot in time_slots:
            published = time_now() - timeslot[1]
            reltime = dictionary.reltime({'published': published, })
            self.assertTrue(timeslot[0] in reltime)


class CSSLinkTest(TestCase):

    """tests for CSS Link
    """

    def setUp(self):
        """set up tests
        """
        self.seeder = Seed.seeder()
        self.seeder.add_entity(CSSLink, 10)
        self.seeder.execute()

    def tearDown(self):
        """clean up after tests
        """
        CSSLink.objects.all().delete()

    def test_save(self):
        """test save method
        """
        css = CSSLink(
            name='test css link',
            link='https://example.com/',
        )
        css.save()
        self.assertIsNotNone(css.pk)

    def test_link(self):
        """test only valid links are accepted
        """
        css = CSSLink.objects.all()[0]
        css.link = 'abcde'
        # TODO: test for error
        css.save()

    def test_str(self):
        """test str method
        """
        css = CSSLink.objects.all()[0]
        self.assertEqual(css.__str__(), css.name)

    def test_duplicates(self):
        """test duplicates are not allowed
        """
        css1 = CSSLink.objects.all()[0]
        css2 = CSSLink(name=css1.name, link=css1.link)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                css2.save()

    def test_save_with_dependency(self):
        """test save method with dependency
        """
        css = CSSLink.objects.all()[0]
        dependency = CSSLink.objects.all()[1:]
        for d in dependency:
            css.dependency.add(d)
        css.save()
        self.assertListEqual(list(css.dependency.all()), list(dependency))

    def test_cyclic_dependency(self):
        """test for cycles in dependency
        """
        # d_set = dependencies
        # for d in d_set:
        #   for dependencies of d:
        #       if dependency in d_set:
        #           cyclic dependency exists
        pass


class JSLinkTest(TestCase):

    """tests for js Link
    """

    def setUp(self):
        """set up tests
        """
        self.seeder = Seed.seeder()
        self.seeder.add_entity(JSLink, 10)
        self.seeder.execute()

    def tearDown(self):
        """clean up after tests
        """
        JSLink.objects.all().delete()

    def test_save(self):
        """test save method
        """
        js = JSLink(
            name='test js link',
            link='https://example.com/',
        )
        js.save()
        self.assertIsNotNone(js.pk)

    def test_link(self):
        """test only valid links are accepted
        """
        js = JSLink.objects.all()[0]
        js.link = 'abcde'
        # TODO: test for error
        js.save()

    def test_str(self):
        """test str method
        """
        js = JSLink.objects.all()[0]
        self.assertEqual(js.__str__(), js.name)

    def test_duplicates(self):
        """test duplicates are not allowed
        """
        js1 = JSLink.objects.all()[0]
        js2 = JSLink(name=js1.name, link=js1.link)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                js2.save()

    def test_save_with_dependency(self):
        """test save method with dependency
        """
        js = JSLink.objects.all()[0]
        dependency = JSLink.objects.all()[1:]
        for d in dependency:
            js.dependency.add(d)
        js.save()
        self.assertListEqual(list(js.dependency.all()), list(dependency))

    def test_cyclic_dependency(self):
        """test for cycles in dependency
        """
        # d_set = dependencies
        # for d in d_set:
        #   for dependencies of d:
        #       if dependency in d_set:
        #           cyclic dependency exists
        pass

"""Tests for Articles

"""

from django.core.urlresolvers import NoReverseMatch
from django.test import Client
from django.test import TestCase
from django.utils import timezone

from subdomains.utils import reverse

from sitedata.models import Tag

from .models import Article

HTTP_HOST = 'articles.example.com'


class ArticlesModelTest(TestCase):

    """Tests for Article Models
    """

    def setUp(self):
        """create a test Article
        """
        self.client = Client()
        tag = Tag(tagname='test tag')
        tag.save()
        article = Article(
            title='Test Article',
            body='This is a test article',
            published=timezone.now(),
        )
        article.save()
        self.article_slug = article.slug
        article.tags.add(tag)
        article.save()
        self.assertIn(tag, article.tags.all())

    def test_add_model(self):
        """test adding Articles
        """
        article = Article.objects.get(title='Test Article')
        self.assertIsNotNone(article)

    def test_str(self):
        """test Article.__str__ returns title
        """
        article = Article.objects.get(title='Test Article')
        self.assertEqual(article.__str__(), article.title)

    def test_duplicate(self):
        """test duplicate Articles get different slugs
        """
        article1 = Article.objects.get(title='Test Article')
        article2 = Article(
            title=article1.title,
            body=article1.body,
            published=article1.published,
        )
        article2.save()
        self.assertEqual(article1.title, article2.title)
        self.assertNotEqual(article1.slug, article2.slug)

    def test_post_url(self):
        """test Article urls are generated correctly
        """
        article = Article.objects.get(title='Test Article')
        url = reverse(
            viewname='articles:post',
            subdomain='articles',
            kwargs={'article': article.slug, })
        self.assertEqual(article.get_absolute_url(), url)

    def test_valid_post_url(self):
        """test Article urls except valid keywords only
        """
        with self.assertRaises(NoReverseMatch):
            reverse(
                viewname='articles:post',
                subdomain='articles',
                kwargs={'article': 'a!FQ#^VQ$!QC', })

    def test_save(self):
        """test Article save() does not have unwanted side-effects
        """
        article = Article.objects.get(title='Test Article')
        title = article.title
        published = article.published
        slug = article.slug
        modified = article.modified
        try:
            article.save()
        except:
            self.fail('Article save method raised an Exception.')
        else:
            self.assertEqual(article.title, title)
            self.assertEqual(article.published, published)
            self.assertEqual(article.slug, slug)
            self.assertNotEqual(article.modified, modified)

    def test_post_view(self):
        """test Article view
        """
        article = Article.objects.get(slug=self.article_slug)
        self.assertIsNotNone(article)
        self.assertIsNotNone(article.slug)
        url = reverse(
            viewname='articles:post',
            subdomain='articles',
            kwargs={'article': article.slug, })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        response_article = response.context['post']
        self.assertEqual(article, response_article)
        self.assertEqual(url, response.context['page_url'])

    def test_index_view(self):
        """test Articles index view
        """
        url = reverse(
            viewname='articles:index',
            subdomain='articles')
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 200)
        response_articles = list(response.context['posts'])
        articles = list(Article.objects.order_by('-published').values())
        self.assertListEqual(articles, response_articles)
        self.assertEqual(url, response.context['page_url'])

    def test_nonexistant_article_view(self):
        """test Articles view with a non-existant article
        """
        url = reverse(
            viewname='articles:post',
            subdomain='articles',
            kwargs={'article': 'xyzrandomarticle', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

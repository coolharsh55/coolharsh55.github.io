from autofixture import AutoFixture
from django.test import TestCase

from .models import get_unique_slug

from sitebase.models import Author


class ModelsTests(TestCase):
    """tests for models utils"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_unique_slug(self):
        fixture = AutoFixture(Author)
        fixture.create(1)
        author_orig = Author.objects.all()[0]
        unique_slug = get_unique_slug(
            Author, author_orig, 'name', name=author_orig.name)
        author_new = Author(name=author_orig.name)
        author_new.save()
        self.assertNotEqual(author_new.slug, author_orig.slug)
        self.assertEqual(author_new.slug, unique_slug)
        self.assertNotEqual(
            author_new.slug, get_unique_slug(
                Author, author_orig, 'name', name=author_orig.name))

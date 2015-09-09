"""tests for dev blog
"""

from django.test import Client
from django.test import TestCase

from subdomains.utils import reverse

HTTP_HOST = 'dev.example.com'


class DevBlogUrlTest(TestCase):

    """tests for the devblog urls
    """

    def setUp(self):
        """set up tests
        """
        self.client = Client()

    def tearDown(self):
        """clean up after tests
        """
        pass

    def test_url_index(self):
        """test url for index
        """
        url = reverse(
            viewname='devblog:index',
            subdomain='dev')
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

    def test_url_blogpost(self):
        """test url for blogpost
        """
        url = reverse(
            viewname='devblog:blogpost',
            subdomain='dev',
            kwargs={'blogpost': 'randomblogpost', })
        self.assertIsNotNone(url)
        response = self.client.get(url, HTTP_HOST=HTTP_HOST)
        self.assertEqual(response.status_code, 404)

    def test_404(self):
        """test 404 on subdomain returns fancy404
        """
        pass

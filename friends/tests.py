"""tests for friends
"""

from django.test import Client
from django.test import TestCase

from subdomains.utils import reverse


class SupBdayTest(TestCase):

    """tests for sup's bday
    """

    def test_url(self):
        """test url for sup's bday 2015
        """
        url = reverse(
            viewname='friends:sup_bday_2015',
            subdomain='friends')
        self.assertIsNotNone(url)

    def test_index(self):
        """test view for sup's bday 2015'
        """
        url = reverse(
            viewname='friends:sup_bday_2015',
            subdomain='friends')
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

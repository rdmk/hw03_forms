from django.http import response
from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_author_page(self):
        response = self.guest_client.get('/about/author/')
        self.assertAlmostEqual(response.status_code, 200)

    def test_tech_page(self):
        response = self.guest_client.get('/about/tech/')
        self.assertAlmostEqual(response.status_code, 200)

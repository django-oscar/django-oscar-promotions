from django.urls import reverse
from oscar.test.testcases import WebTestCase


class PromotionViewsTests(WebTestCase):
    def test_pages_exist(self):
        urls = [reverse('oscar_promotions:home')]
        for url in urls:
            self.assertIsOk(self.get(url))

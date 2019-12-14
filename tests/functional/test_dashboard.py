from django.urls import reverse
from oscar.test.testcases import WebTestCase


class DashboardViewsTests(WebTestCase):

    is_staff = True

    def test_pages_exist(self):
        urls = [
            reverse('oscar_promotions_dashboard:promotion-list'),
            reverse('oscar_promotions_dashboard:promotion-create-rawhtml'),
            reverse('oscar_promotions_dashboard:promotion-create-singleproduct'),
            reverse('oscar_promotions_dashboard:promotion-create-image'),
        ]
        for url in urls:
            self.assertIsOk(self.get(url))

    def test_create_redirects(self):
        base_url = reverse('oscar_promotions_dashboard:promotion-create-redirect')
        p_types = ['rawhtml', 'singleproduct', 'image']
        for p_type in p_types:
            url = '{base_url}?promotion_type={p_type}'.format(
                base_url=base_url, p_type=p_type
            )
            self.assertIsRedirect(self.get(url))

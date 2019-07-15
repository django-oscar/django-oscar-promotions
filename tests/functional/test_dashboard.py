from django.urls import reverse
from oscar.test.testcases import WebTestCase


class DashboardViewsTests(WebTestCase):

    is_staff = True

    def test_pages_exist(self):
        urls = [
            reverse("dashboard:promotion-list"),
            reverse("dashboard:promotion-create-rawhtml"),
            reverse("dashboard:promotion-create-singleproduct"),
            reverse("dashboard:promotion-create-image"),
        ]
        for url in urls:
            self.assertIsOk(self.get(url))

    def test_create_redirects(self):
        base_url = reverse("dashboard:promotion-create-redirect")
        p_types = ["rawhtml", "singleproduct", "image"]
        for p_type in p_types:
            url = "{base_url}?promotion_type={p_type}".format(
                base_url=base_url, p_type=p_type
            )
            self.assertIsRedirect(self.get(url))

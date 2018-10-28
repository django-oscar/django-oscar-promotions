from django.test import TestCase
from django.urls import reverse

from oscar.core.loading import get_classes
from oscar.test.testcases import WebTestCase

from oscar_promotions import models
from oscar_promotions.dashboard import forms


RawHTML, PagePromotion = get_classes('oscar_promotions.models', ['RawHTML', 'PagePromotion'])


class ViewTests(WebTestCase):
    is_staff = True

    def test_pages_exist(self):
        urls = [
            reverse('dashboard:promotion-list'),
            reverse('dashboard:promotion-create-rawhtml'),
            reverse('dashboard:promotion-create-singleproduct'),
            reverse('dashboard:promotion-create-image'),
        ]
        for url in urls:
            self.assertIsOk(self.get(url))

    def test_create_redirects(self):
        base_url = reverse('dashboard:promotion-create-redirect')
        types = ['rawhtml', 'singleproduct', 'image']
        for p_type in types:
            url = '%s?promotion_type=%s' % (base_url, p_type)
            self.assertIsRedirect(self.get(url))


class PromotionTest(TestCase):

    def test_default_template_name(self):
        promotion = models.Image.objects.create(name="dummy banner")
        self.assertEqual('oscar_promotions/image.html', promotion.template_name())


class TestPagePromotionForm(TestCase):

    def test_page_promotion_has_fields(self):
        promotion = RawHTML()
        promotion.save()
        instance = PagePromotion(content_object=promotion)
        data = {'position': 'page', 'page_url': '/'}
        form = forms.PagePromotionForm(data=data, instance=instance)
        self.assertTrue(form.is_valid())
        page_promotion = form.save()
        self.assertEqual(page_promotion.page_url, '/')

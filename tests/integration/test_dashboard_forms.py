from django.test import TestCase
from oscar.core.loading import get_model

from oscar_promotions.dashboard import forms

RawHTML = get_model('oscar_promotions', 'RawHTML')
PagePromotion = get_model('oscar_promotions', 'PagePromotion')


class PagePromotionFormTests(TestCase):
    def test_page_promotion_has_fields(self):
        promotion = RawHTML()
        promotion.save()
        instance = PagePromotion(content_object=promotion)
        data = {'position': 'page', 'page_url': '/'}
        form = forms.PagePromotionForm(data=data, instance=instance)
        self.assertTrue(form.is_valid())
        page_promotion = form.save()
        self.assertEqual(page_promotion.page_url, '/')

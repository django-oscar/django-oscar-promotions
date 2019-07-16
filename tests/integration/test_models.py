from django.test import RequestFactory, TestCase
from oscar.core.loading import get_class

from oscar_promotions.templatetags.promotion_tags import render_promotion
from tests.factories.oscar_promotions import (
    AutomaticProductListFactory,
    HandPickedProductListFactory,
    ImageFactory,
    MultiImageFactory,
    RawHTMLFactory,
    SingleProductFactory,
    TabbedBlockFactory,
)

DefaultStrategy = get_class('partner.strategy', 'Default')


class RawHTMLPromotionsTests(TestCase):
    def test_render_promotion(self):
        promotion = RawHTMLFactory()
        render_promotion({'request': RequestFactory().get('/')}, promotion)
        self.assertEqual('oscar_promotions/rawhtml.html', promotion.template_name())


class ImagePromotionsTests(TestCase):
    def test_render_promotion(self):
        promotion = ImageFactory()
        render_promotion({'request': RequestFactory().get('/')}, promotion)
        self.assertEqual('oscar_promotions/image.html', promotion.template_name())


class MultiImagePromotionsTests(TestCase):
    def test_render_promotion(self):
        promotion = MultiImageFactory()
        render_promotion({'request': RequestFactory().get('/')}, promotion)
        self.assertEqual('oscar_promotions/multiimage.html', promotion.template_name())


class SingleProductFactoryPromotionsTests(TestCase):
    def test_render_promotion(self):
        promotion = SingleProductFactory()
        request = RequestFactory().get('/')
        request.strategy = DefaultStrategy()
        render_promotion({'request': request}, promotion)
        self.assertEqual(
            'oscar_promotions/singleproduct.html', promotion.template_name()
        )


class AutomaticProductListPromotionsTests(TestCase):
    def test_render_promotion(self):
        promotion = AutomaticProductListFactory()
        request = RequestFactory().get('/')
        request.strategy = DefaultStrategy()
        render_promotion({'request': request}, promotion)
        self.assertEqual(
            'oscar_promotions/automaticproductlist.html', promotion.template_name()
        )


class HandPickedProductListPromotionsTests(TestCase):
    def test_render_promotion(self):
        promotion = HandPickedProductListFactory()
        request = RequestFactory().get('/')
        request.strategy = DefaultStrategy()
        render_promotion({'request': request}, promotion)
        self.assertEqual(
            'oscar_promotions/handpickedproductlist.html', promotion.template_name()
        )


class TabbedBlockPromotionsTests(TestCase):
    def test_render_promotion(self):
        promotion = TabbedBlockFactory()
        render_promotion({'request': RequestFactory().get('/')}, promotion)
        self.assertEqual('oscar_promotions/tabbedblock.html', promotion.template_name())

from django.test import TestCase
from oscar.core.loading import get_model


Image = get_model("oscar_promotions", "Image")


class BasePromotionsTests(TestCase):
    def test_default_template_name(self):
        promotion = Image.objects.create(name="dummy banner")
        self.assertEqual("oscar_promotions/image.html", promotion.template_name())

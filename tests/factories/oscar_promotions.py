import factory.fuzzy
from oscar.core.loading import get_model

from tests.factories.catalogue import ProductFactory

PagePromotion = get_model('oscar_promotions', 'PagePromotion')
KeywordPromotion = get_model('oscar_promotions', 'KeywordPromotion')


class RawHTMLFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_model('oscar_promotions', 'RawHTML')

    name = factory.Faker('sentence')
    body = factory.Faker('text')


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_model('oscar_promotions', 'Image')

    name = factory.Faker('sentence')
    link_url = factory.Faker('uri_path')
    image = 'image.jpg'


class MultiImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_model('oscar_promotions', 'MultiImage')

    name = factory.Faker('sentence')

    @factory.post_generation
    def images(self, *args, **kwargs):
        for _ in range(4):
            self.images.add(ImageFactory())


class SingleProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_model('oscar_promotions', 'SingleProduct')

    name = factory.Faker('sentence')
    product = factory.SubFactory(ProductFactory)
    description = factory.Faker('text')


class AutomaticProductListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_model('oscar_promotions', 'AutomaticProductList')

    name = factory.Faker('sentence')
    description = factory.Faker('text')
    link_url = factory.Faker('uri_path')
    link_text = factory.Faker('sentence')
    method = factory.fuzzy.FuzzyChoice(
        [choice for choice, label in Meta.model.METHOD_CHOICES]
    )

    @factory.post_generation
    def products(self, *args, **kwargs):
        for _ in range(4):
            ProductFactory()


class HandPickedProductListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_model('oscar_promotions', 'HandPickedProductList')

    name = factory.Faker('sentence')
    description = factory.Faker('text')
    link_url = factory.Faker('uri_path')
    link_text = factory.Faker('sentence')

    @factory.post_generation
    def products(self, *args, **kwargs):
        for _ in range(4):
            self.products.add(ProductFactory())


class TabbedBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_model('oscar_promotions', 'TabbedBlock')

    name = factory.Faker('sentence')

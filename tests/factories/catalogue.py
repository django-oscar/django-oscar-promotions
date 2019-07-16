import factory
from oscar.core.loading import get_model

Product = get_model('catalogue', 'Product')
ProductClass = get_model('catalogue', 'ProductClass')


class ProductClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductClass

    name = factory.Faker('sentence')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    upc = factory.Faker('isbn13')
    title = factory.Faker('sentence')
    description = factory.Faker('text')
    product_class = factory.SubFactory(ProductClassFactory)

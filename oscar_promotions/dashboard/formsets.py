from django.forms.models import inlineformset_factory

from oscar.core.loading import get_class, get_classes

HandPickedProductList, OrderedProduct \
    = get_classes('oscar_promotions.models',
                  ['HandPickedProductList', 'OrderedProduct'])
ProductSelect = get_class('dashboard.catalogue.widgets', 'ProductSelect')
OrderedProductForm = get_class('oscar_promotions.dashboard.forms', 'OrderedProductForm')

OrderedProductFormSet = inlineformset_factory(
    HandPickedProductList, OrderedProduct, form=OrderedProductForm, extra=2)

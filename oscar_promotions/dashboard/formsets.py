from django.forms.models import inlineformset_factory
from oscar.core.loading import get_class, get_model

HandPickedProductList = get_model('oscar_promotions', 'HandPickedProductList')
OrderedProduct = get_model('oscar_promotions', 'OrderedProduct')
OrderedProductForm = get_class(
    'oscar_promotions.dashboard.forms', 'OrderedProductForm', module_prefix='oscar_promotions'
)

OrderedProductFormSet = inlineformset_factory(
    HandPickedProductList, OrderedProduct, form=OrderedProductForm, extra=2)

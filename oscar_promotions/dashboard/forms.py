from django import forms
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from django.forms import SelectMultiple
from oscar.core.loading import get_class, get_model
from oscar.forms.fields import ExtendedURLField

from oscar_promotions import app_settings
from oscar_promotions.conf import PROMOTION_CLASSES

HandPickedProductList = get_model('oscar_promotions', 'HandPickedProductList')
OrderedProduct = get_model('oscar_promotions', 'OrderedProduct')
PagePromotion = get_model('oscar_promotions', 'PagePromotion')
RawHTML = get_model('oscar_promotions', 'RawHTML')
SingleProduct = get_model('oscar_promotions', 'SingleProduct')

ProductSelect = get_class('dashboard.catalogue.widgets', 'ProductSelect')


class PromotionTypeSelectForm(forms.Form):
    choices = []
    for klass in PROMOTION_CLASSES:
        choices.append((klass.classname(), klass._meta.verbose_name))
    promotion_type = forms.ChoiceField(choices=tuple(choices),
                                       label=_("Promotion type"))


class RawHTMLForm(forms.ModelForm):
    class Meta:
        model = RawHTML
        fields = ['name', 'body', 'site']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs['class'] = "no-widget-init"


class SingleProductForm(forms.ModelForm):
    class Meta:
        model = SingleProduct
        fields = ['name', 'product', 'description', 'site']
        widgets = {'product': ProductSelect}


class HandPickedProductListForm(forms.ModelForm):
    class Meta:
        model = HandPickedProductList
        fields = ['name', 'description', 'link_url', 'link_text', 'site']


class OrderedProductForm(forms.ModelForm):
    class Meta:
        model = OrderedProduct
        fields = ['list', 'product', 'display_order']
        widgets = {
            'product': ProductSelect,
        }


class PagePromotionForm(forms.ModelForm):
    page_url = ExtendedURLField(label=_("URL"))
    position = forms.CharField(
        widget=forms.Select(choices=app_settings.OSCAR_PROMOTIONS_POSITIONS),
        label=_("Position"),
        help_text=_("Where in the page this content block will appear"))

    class Meta:
        model = PagePromotion
        fields = ['position', 'page_url']

    def clean_page_url(self):
        page_url = self.cleaned_data.get('page_url')
        if not page_url:
            return page_url

        if page_url.startswith('http'):
            raise forms.ValidationError(
                _("Content blocks can only be linked to internal URLs"))

        if page_url.startswith('/') and not page_url.endswith('/'):
            page_url += '/'

        return page_url


class PromotionsSearchForm(forms.Form):

    sites_choices = (('', '---------'),) + tuple([(k, v) for k, v in Site.objects.all().values_list("id", "name")])
    sites = forms.MultipleChoiceField(
        choices=sites_choices, label=_("Site"), required=False,
        widget=SelectMultiple(attrs={'data-multiple': 'true'})
    )

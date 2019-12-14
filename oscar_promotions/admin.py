from django.contrib import admin
from oscar.core.loading import get_model

AutomaticProductList = get_model('oscar_promotions', 'AutomaticProductList')
HandPickedProductList = get_model('oscar_promotions', 'HandPickedProductList')
Image = get_model('oscar_promotions', 'Image')
KeywordPromotion = get_model('oscar_promotions', 'KeywordPromotion')
MultiImage = get_model('oscar_promotions', 'MultiImage')
OrderedProduct = get_model('oscar_promotions', 'OrderedProduct')
PagePromotion = get_model('oscar_promotions', 'PagePromotion')
RawHTML = get_model('oscar_promotions', 'RawHTML')
SingleProduct = get_model('oscar_promotions', 'SingleProduct')
TabbedBlock = get_model('oscar_promotions', 'TabbedBlock')


class OrderProductInline(admin.TabularInline):
    model = OrderedProduct


class HandPickedProductListAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]


class PagePromotionAdmin(admin.ModelAdmin):
    list_display = ['page_url', 'content_object', 'position']
    exclude = ['clicks']


class KeywordPromotionAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'position', 'clicks']
    readonly_fields = ['clicks']


admin.site.register(Image)
admin.site.register(MultiImage)
admin.site.register(RawHTML)
admin.site.register(HandPickedProductList, HandPickedProductListAdmin)
admin.site.register(AutomaticProductList)
admin.site.register(TabbedBlock)
admin.site.register(PagePromotion, PagePromotionAdmin)
admin.site.register(KeywordPromotion, KeywordPromotionAdmin)
admin.site.register(SingleProduct)

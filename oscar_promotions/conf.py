from oscar.core.loading import get_model

SingleProduct = get_model('oscar_promotions', 'SingleProduct')
RawHTML = get_model('oscar_promotions', 'RawHTML')
Image = get_model('oscar_promotions', 'Image')
PagePromotion = get_model('oscar_promotions', 'PagePromotion')
AutomaticProductList = get_model('oscar_promotions', 'AutomaticProductList')
HandPickedProductList = get_model('oscar_promotions', 'HandPickedProductList')
MultiImage = get_model('oscar_promotions', 'MultiImage')


def get_promotion_classes():
    return (RawHTML, Image, SingleProduct, AutomaticProductList,
            HandPickedProductList, MultiImage)


PROMOTION_CLASSES = get_promotion_classes()

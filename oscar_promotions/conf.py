from oscar.core.loading import get_class

SingleProduct = get_class("oscar_promotions.models", "SingleProduct")
RawHTML = get_class("oscar_promotions.models", "RawHTML")
Image = get_class("oscar_promotions.models", "Image")
PagePromotion = get_class("oscar_promotions.models", "PagePromotion")
AutomaticProductList = get_class("oscar_promotions.models", "AutomaticProductList")
HandPickedProductList = get_class("oscar_promotions.models", "HandPickedProductList")
MultiImage = get_class("oscar_promotions.models", "MultiImage")


def get_promotion_classes():
    return (
        RawHTML,
        Image,
        SingleProduct,
        AutomaticProductList,
        HandPickedProductList,
        MultiImage,
    )


PROMOTION_CLASSES = get_promotion_classes()

from django.urls import reverse
from django.views.generic import RedirectView, TemplateView
import logging

from constance import config
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.cache import cache_page
from oscar.core.loading import get_model

from libs.silk_helpers.decorators import conditional_profiling

logger = logging.getLogger(__name__)


ProductReview = get_model('reviews', 'ProductReview')
Category = get_model('catalogue', 'Category')


if config.USE_ESI:
    decorators = [cache_page(3600), ]
else:
    decorators = []


class HomeView(TemplateView):
    """
    This is the home page and will typically live at /
    """
    template_name = 'oscar_promotions/home.html'


class RecordClickView(RedirectView):
    """
    Simple RedirectView that helps recording clicks made on promotions
    """
    permanent = False
    model = None

    def get_redirect_url(self, **kwargs):
        try:
            prom = self.model.objects.get(pk=kwargs['pk'])
        except self.model.DoesNotExist:
            return reverse('promotions:home')

        if prom.promotion.has_link:
            prom.record_click()
            return prom.link_url
        return reverse('promotions:home')


@method_decorator(conditional_profiling(), name='dispatch')
class VFHomeView(HomeView):
    """
    Class/View to handle home
    """

    def get_context_data(self, **kwargs):
        ctx = super(VFHomeView, self).get_context_data(**kwargs)
        ctx['review_list'] = ProductReview.objects.filter(
            status=ProductReview.APPROVED,
            product__is_public=True
        ).order_by("-date_created")[:10]

        ctx['categories'] = Category.objects.filter(more_ways_shop=True)

        return ctx


class AMPHomeView(TemplateView):
    """
    Class/View to handle AMP home
    """
    template_name = "oscar_promotions/amp_home.html"


# @method_decorator(decorators, name='dispatch')
class LandingPageFloresADomicilio(VFHomeView):
    template_name = "oscar_promotions/landing-page-flores-a-domicilio.html"


# @method_decorator(decorators, name='dispatch')
class LandingPageComuna(VFHomeView):
    template_name = "oscar_promotions/landing-page-comuna.html"
    comuna = None

    def get(self, request, *args, **kwargs):
        comuna = kwargs.get("comuna")
        if comuna:
            self.comuna = comuna

        return super(LandingPageComuna, self).get(request, *args, **kwargs)

    def get_template_names(self):
        template_list = super(LandingPageComuna, self).get_template_names()
        if len(template_list) > 0 and self.comuna:
            name = "oscar_promotions/landing-page-comuna-%s.html" % slugify(self.comuna)
            template_list.insert(0, name)

        return template_list

    def get_context_data(self, **kwargs):
        ctx = super(LandingPageComuna, self).get_context_data(**kwargs)

        comuna = kwargs.get("comuna")
        if comuna:
            ctx["comuna"] = comuna.replace("-", " ").title()

        return ctx

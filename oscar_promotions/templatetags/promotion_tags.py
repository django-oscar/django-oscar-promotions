from django.template import Library
from django.template.loader import select_template
import logging
import pytz

from django import template
from django.template.loader import select_template
from django.conf import settings
from django.utils.timezone import now
from django.db.models import Q

from oscar_promotions.models import TimeBasedPromotion, MultiImage

from dynamic_preferences.registries import global_preferences_registry

register = template.Library()
logger = logging.getLogger(__name__)
global_preferences = global_preferences_registry.manager()

register = Library()


@register.simple_tag(takes_context=True)
def render_promotion(context, promotion):
    template = select_template([
        promotion.template_name(), 'oscar_promotions/default.html'])
    request = context['request']

    ctx = {
        'request': request,
        'promotion': promotion
    }
    ctx.update(**promotion.template_context(request=request))

    return template.render(ctx, request)


@register.inclusion_tag('oscar_promotions/partials/prices_range.html', takes_context=True)
def search_facets_list(context):
    facets_list = settings.OSCAR_SEARCH_FACETS['queries'].items()[0][1]['queries']

    ctx = dict()
    ctx['facets_list'] = facets_list

    return ctx


@register.inclusion_tag('oscar_promotions/partials/category_list.html', takes_context=True)
def show_category_list(context):
    categories_list = settings.CATEGORIES_LIST

    return {'categories_list': categories_list}


@register.simple_tag()
def get_time_promotion():
    current_timezone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = now().astimezone(current_timezone)

    tpl = TimeBasedPromotion.objects.filter(enabled=True)
    tpl = tpl.filter(Q(available_since_date__lte=current_datetime) |
                     Q(available_since_date__isnull=True))
    tpl = tpl.filter(Q(available_until_date__gte=current_datetime) |
                     Q(available_until_date__isnull=True))
    tpl = tpl.filter(available_since_time__lte=current_datetime.time(),
                     available_until_time__gte=current_datetime.time())

    return tpl


@register.simple_tag()
def get_multi_images_promotion():
    try:
        multi_image = MultiImage.objects.get(name=global_preferences['PromotionalOffer__PROMOTIONAL_CAROUSEL'])
    except MultiImage.DoesNotExist as err:
        logger.exception(err)
    else:
        return multi_image.images.all() if multi_image else []


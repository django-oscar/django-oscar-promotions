from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PromotionsConfig(AppConfig):
    label = 'oscar_promotions'
    name = 'oscar_promotions'
    verbose_name = _('Promotions')

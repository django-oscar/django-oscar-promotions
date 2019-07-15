from django.apps import apps
from django.conf.urls import url

from oscar import config
from oscar.core.loading import get_class


class Shop(config.Shop):
    name = ''

    def ready(self):
        super().ready()
        self.promotions_app = apps.get_app_config('promotions')

    def get_urls(self):
        urls = super().get_urls()
        urls.append(url(r'', self.promotions_app.urls))
        return urls

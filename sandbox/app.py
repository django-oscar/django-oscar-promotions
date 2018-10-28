from django.conf.urls import url

from oscar.app import Shop as CoreShop
from oscar.core.loading import get_class


class Shop(CoreShop):
    app = get_class('oscar_promotions.app', 'application')

    def get_urls(self):
        urls = super().get_urls()
        urls.append(url(r'', self.app.urls))
        return urls


application = Shop()

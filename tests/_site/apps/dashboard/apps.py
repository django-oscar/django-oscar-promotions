from django.apps import apps
from django.conf.urls import include, url
from oscar.apps.dashboard.apps import DashboardConfig as OscarDashboardConfig


class DashboardConfig(OscarDashboardConfig):
    def ready(self):
        super().ready()
        self.promotions_app = apps.get_app_config('oscar_promotions_dashboard')

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = []
        extra_urls.append(url(r'^promotions/', include(self.promotions_app.urls[0])))
        urls.extend(self.post_process_urls(extra_urls))
        return urls

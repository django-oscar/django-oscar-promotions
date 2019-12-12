from django.apps import apps
from django.conf import settings
from django.conf.urls import i18n
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include(i18n)),
    path("", apps.get_app_config("oscar_promotions").urls),
    path("dashboard/promotions/", apps.get_app_config("oscar_promotions_dashboard").urls),
    path("", include(apps.get_app_config("oscar").urls[0])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

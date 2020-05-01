from django.conf.urls import url
from django.utils.translation import gettext_lazy as _
from oscar.core.application import OscarDashboardConfig
from oscar.core.loading import get_class


class PromotionsDashboardConfig(OscarDashboardConfig):

    label = 'oscar_promotions_dashboard'
    name = 'oscar_promotions.dashboard'
    namespace = 'oscar_promotions_dashboard'
    verbose_name = _("Promotions dashboard")
    default_permissions = ['is_staff']

    # Dynamically set the CRUD views for all promotion classes
    view_names = (
        ('create_%s_view', 'Create%sView'),
        ('update_%s_view', 'Update%sView'),
        ('delete_%s_view', 'Delete%sView'),
    )

    def get_promotion_classes(self):
        from oscar_promotions.conf import PROMOTION_CLASSES

        return PROMOTION_CLASSES

    def ready(self):
        super().ready()
        self.list_view = get_class(
            'oscar_promotions.dashboard.views', 'ListView', module_prefix='oscar_promotions'
        )
        self.page_list = get_class(
            'oscar_promotions.dashboard.views', 'PageListView', module_prefix='oscar_promotions'
        )
        self.page_detail = get_class(
            'oscar_promotions.dashboard.views', 'PageDetailView', module_prefix='oscar_promotions'
        )
        self.create_redirect_view = get_class(
            'oscar_promotions.dashboard.views', 'CreateRedirectView', module_prefix='oscar_promotions'
        )
        self.delete_page_promotion_view = get_class(
            'oscar_promotions.dashboard.views', 'DeletePagePromotionView', module_prefix='oscar_promotions'
        )
        for klass in self.get_promotion_classes():
            for attr_name, view_name in self.view_names:
                full_attr_name = attr_name % klass.classname()
                full_view_name = view_name % klass.__name__
                view = get_class(
                    'oscar_promotions.dashboard.views', full_view_name, module_prefix='oscar_promotions'
                )
                setattr(self, full_attr_name, view)

    def get_urls(self):
        urls = [
            url(r'^$', self.list_view.as_view(), name='promotion-list'),
            url(r'^pages/$', self.page_list.as_view(), name='promotion-list-by-page'),
            url(
                r'^page/-(?P<path>/([\w-]+(/[\w-]+)*/)?)$',
                self.page_detail.as_view(),
                name='promotion-list-by-url',
            ),
            url(
                r'^create/$',
                self.create_redirect_view.as_view(),
                name='promotion-create-redirect',
            ),
            url(
                r'^page-promotion/(?P<pk>\d+)/$',
                self.delete_page_promotion_view.as_view(),
                name='pagepromotion-delete',
            ),
        ]
        for klass in self.get_promotion_classes():
            code = klass.classname()
            urls.extend(
                [
                    url(
                        r'create/%s/' % code,
                        getattr(self, 'create_%s_view' % code).as_view(),
                        name='promotion-create-%s' % code,
                    ),
                    url(
                        r'^update/(?P<ptype>%s)/(?P<pk>\d+)/$' % code,
                        getattr(self, 'update_%s_view' % code).as_view(),
                        name='promotion-update',
                    ),
                    url(
                        r'^delete/(?P<ptype>%s)/(?P<pk>\d+)/$' % code,
                        getattr(self, 'delete_%s_view' % code).as_view(),
                        name='promotion-delete',
                    ),
                ]
            )
        return self.post_process_urls(urls)

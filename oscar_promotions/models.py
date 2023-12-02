import datetime

import pytz
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _, pgettext_lazy
from oscar.core.loading import get_model
from oscar.models.fields import ExtendedURLField

from oscar_promotions import app_settings

# Linking models - these link promotions to content (eg pages, or keywords)


class LinkedPromotion(models.Model):

    # We use generic foreign key to link to a promotion model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = fields.GenericForeignKey('content_type', 'object_id')

    position = models.CharField(_("Position"), max_length=100,
                                help_text=_("Position on page"))
    display_order = models.PositiveIntegerField(_("Display Order"), default=0)
    clicks = models.PositiveIntegerField(_("Clicks"), default=0)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    site = models.ForeignKey('sites.Site', on_delete=models.CASCADE, null=False, blank=False, default=1)

    class Meta:
        abstract = True
        app_label = 'oscar_promotions'
        ordering = ['-clicks']
        verbose_name = _("Linked Promotion")
        verbose_name_plural = _("Linked Promotions")

    def record_click(self):
        self.clicks += 1
        self.save()
    record_click.alters_data = True


class PagePromotion(LinkedPromotion):
    """
    A promotion embedded on a particular page.
    """
    page_url = ExtendedURLField(
        _('Page URL'), max_length=128, db_index=True)

    def __str__(self):
        return "%s on %s" % (self.content_object, self.page_url)

    def get_link(self):
        return reverse('promotions:page-click',
                       kwargs={'page_promotion_id': self.id})

    class Meta(LinkedPromotion.Meta):
        verbose_name = _("Page Promotion")
        verbose_name_plural = _("Page Promotions")


class KeywordPromotion(LinkedPromotion):
    """
    A promotion linked to a specific keyword.

    This can be used on a search results page to show promotions
    linked to a particular keyword.
    """

    keyword = models.CharField(_("Keyword"), max_length=200)

    # We allow an additional filter which will let search query matches
    # be restricted to different parts of the site.
    filter = models.CharField(_("Filter"), max_length=200, blank=True)

    def get_link(self):
        return reverse('promotions:keyword-click',
                       kwargs={'keyword_promotion_id': self.id})

    class Meta(LinkedPromotion.Meta):
        verbose_name = _("Keyword Promotion")
        verbose_name_plural = _("Keyword Promotions")

    # Different model types for each type of promotion


class AbstractPromotion(models.Model):
    """
    Abstract base promotion that defines the interface
    that subclasses must implement.
    """
    _type = 'Promotion'
    keywords = fields.GenericRelation(KeywordPromotion,
                                      verbose_name=_('Keywords'))
    pages = fields.GenericRelation(PagePromotion, verbose_name=_('Pages'))

    site = models.ForeignKey('sites.Site', on_delete=models.CASCADE, null=False, blank=False, default=1,
                             verbose_name=_('Site'))

    class Meta:
        abstract = True
        app_label = 'oscar_promotions'
        verbose_name = _("Promotion")
        verbose_name_plural = _("Promotions")

    @property
    def type(self):
        return _(self._type)

    @classmethod
    def classname(cls):
        return cls.__name__.lower()

    @property
    def code(self):
        return self.__class__.__name__.lower()

    def template_name(self):
        """
        Returns the template to use to render this promotion.
        """
        return 'oscar_promotions/%s.html' % self.code

    def template_context(self, request):
        return {}

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    @property
    def num_times_used(self):
        ctype = self.content_type
        page_count = PagePromotion.objects.filter(content_type=ctype,
                                                  object_id=self.id).count()
        keyword_count \
            = KeywordPromotion.objects.filter(content_type=ctype,
                                              object_id=self.id).count()
        return page_count + keyword_count


class RawHTML(AbstractPromotion):
    """
    Simple promotion - just raw HTML
    """
    _type = 'Raw HTML'
    name = models.CharField(_("Name"), max_length=128)


    # Used to determine how to render the promotion (eg
    # if a different width container is required).  This isn't always
    # required.
    display_type = models.CharField(
        _("Display type"), max_length=128, blank=True,
        help_text=_("This can be used to have different types of HTML blocks"
                    " (eg different widths)"))
    body = models.TextField(_("HTML"))
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta(AbstractPromotion.Meta):
        verbose_name = _('Raw HTML')
        verbose_name_plural = _('Raw HTML')

    def __str__(self):
        return self.name


class Image(AbstractPromotion):
    """
    An image promotion is simply a named image which has an optional
    link to another part of the site (or another site).

    This can be used to model both banners and pods.
    """
    _type = 'Image'
    name = models.CharField(_("Name"), max_length=128)
    cta_text = models.TextField(_('CTA Text'), blank=True, help_text=_('Call to action text'))
    link_url = ExtendedURLField(
        _('Link URL'), blank=True,
        help_text=_('This is where this promotion links to'))
    image = models.ImageField(
        _('Image'), upload_to=app_settings.OSCAR_PROMOTIONS_FOLDER,
        max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta(AbstractPromotion.Meta):
        verbose_name = _("Image")
        verbose_name_plural = _("Image")


class MultiImage(AbstractPromotion):
    """
    A multi-image promotion is simply a collection of image promotions
    that are rendered in a specific way.  This models things like
    rotating banners.
    """
    _type = 'Multi-image'
    name = models.CharField(_("Name"), max_length=128)
    images = models.ManyToManyField(
        'oscar_promotions.Image', blank=True,
        help_text=_(
            "Choose the Image content blocks that this block will use. "
            "(You may need to create some first)."))
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta(AbstractPromotion.Meta):
        verbose_name = _("Multi Image")
        verbose_name_plural = _("Multi Images")


class SingleProduct(AbstractPromotion):
    _type = 'Single product'
    name = models.CharField(_("Name"), max_length=128)
    product = models.ForeignKey('catalogue.Product', on_delete=models.CASCADE)
    description = models.TextField(_("Description"), blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def template_context(self, request):
        return {'product': self.product}

    class Meta(AbstractPromotion.Meta):
        verbose_name = _("Single product")
        verbose_name_plural = _("Single product")


class AbstractProductList(AbstractPromotion):
    """
    Abstract superclass for promotions which are essentially a list
    of products.
    """
    name = models.CharField(
        pgettext_lazy("Promotion product list title", "Title"),
        max_length=255)
    description = models.TextField(_("Description"), blank=True)
    link_url = ExtendedURLField(_('Link URL'), blank=True)
    link_text = models.CharField(_("Link text"), max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta(AbstractPromotion.Meta):
        abstract = True
        verbose_name = _("Product list")
        verbose_name_plural = _("Product lists")

    def __str__(self):
        return self.name

    def template_context(self, request):
        return {'products': self.get_products()}


class HandPickedProductList(AbstractProductList):
    """
    A hand-picked product list is a list of manually selected
    products.
    """
    _type = 'Product list'
    products = models.ManyToManyField('catalogue.Product',
                                      through='OrderedProduct', blank=True,
                                      verbose_name=_("Products"))

    def get_queryset(self):
        return self.products.base_queryset()\
            .order_by('%s.display_order' % OrderedProduct._meta.db_table)

    def get_products(self):
        return self.get_queryset()

    class Meta(AbstractProductList.Meta):
        verbose_name = _("Hand Picked Product List")
        verbose_name_plural = _("Hand Picked Product Lists")


class OrderedProduct(models.Model):

    list = models.ForeignKey(
        'oscar_promotions.HandPickedProductList',
        on_delete=models.CASCADE,
        verbose_name=_("List"))
    product = models.ForeignKey(
        'catalogue.Product',
        on_delete=models.CASCADE,
        verbose_name=_("Product"))
    display_order = models.PositiveIntegerField(_('Display Order'), default=0)

    class Meta:
        app_label = 'oscar_promotions'
        ordering = ('display_order',)
        unique_together = ('list', 'product')
        verbose_name = _("Ordered product")
        verbose_name_plural = _("Ordered product")


class AutomaticProductList(AbstractProductList):

    _type = 'Auto-product list'
    BESTSELLING, RECENTLY_ADDED = ('Bestselling', 'RecentlyAdded')
    METHOD_CHOICES = (
        (BESTSELLING, _("Bestselling products")),
        (RECENTLY_ADDED, _("Recently added products")),
    )
    method = models.CharField(_('Method'), max_length=128,
                              choices=METHOD_CHOICES)
    num_products = models.PositiveSmallIntegerField(_('Number of Products'),
                                                    default=4)

    def get_queryset(self):
        Product = get_model('catalogue', 'Product')
        qs = Product.objects.browsable().base_queryset().select_related('stats')
        if self.method == self.BESTSELLING:
            return qs.order_by('-stats__score')
        return qs.order_by('-date_created')

    def get_products(self):
        return self.get_queryset()[:self.num_products]

    class Meta(AbstractProductList.Meta):
        verbose_name = _("Automatic product list")
        verbose_name_plural = _("Automatic product lists")


class OrderedProductList(HandPickedProductList):
    tabbed_block = models.ForeignKey(
        'oscar_promotions.TabbedBlock',
        on_delete=models.CASCADE,
        related_name='tabs',
        verbose_name=_("Tabbed Block"))
    display_order = models.PositiveIntegerField(_('Display Order'), default=0)

    class Meta(HandPickedProductList.Meta):
        ordering = ('display_order',)
        verbose_name = _("Ordered Product List")
        verbose_name_plural = _("Ordered Product Lists")


class TabbedBlock(AbstractPromotion):

    _type = 'Tabbed block'
    name = models.CharField(
        pgettext_lazy("Tabbed block title", "Title"), max_length=255)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    class Meta(AbstractPromotion.Meta):
        verbose_name = _("Tabbed Block")
        verbose_name_plural = _("Tabbed Blocks")


class TimeBasedPromotion(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    available_since_date = models.DateField(blank=True, null=True)
    available_since_time = models.TimeField()
    available_until_date = models.DateField(blank=True, null=True)
    available_until_time = models.TimeField()
    promotional_code = models.CharField(max_length=50, blank=True, null=True)
    call_to_action = models.CharField(max_length=200, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    enabled = models.BooleanField(default=True)
    icon_name = models.CharField(max_length=30, null=True, blank=True)
    site = models.ForeignKey('sites.Site', on_delete=models.CASCADE, null=False, blank=False, default=1)

    def get_remaining_time(self):
        """
        :return: None if no expire time defined.
        :return: DateTime instance until which this promo should show.

        """
        until_date = self.available_until_date
        until_time = self.available_until_time

        if until_date is None and until_time is None:
            return None

        if until_date is None:
            current_timezone = pytz.timezone(settings.TIME_ZONE)
            current_datetime = now().astimezone(current_timezone)

            until_date = current_datetime.date()

        if until_time is None:
            until_time = datetime.time(hour=23, minute=59, second=59)

        until_datetime = datetime.datetime.combine(until_date, until_time)

        return until_datetime

=======================
Django Oscar Promotions
=======================

Django Oscar Promotions is an app for Dashboard-editable promotional content
in Oscar. It was formerly a part of Oscar core, but has now been separated into
a standalone app.

Installation
~~~~~~~~~~~~

Install the package with ``pip install django-oscar-promotions``.

Add the following entries to ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        ...,
        'oscar_promotions.apps.PromotionsConfig',
        'oscar_promotions.dashboard.apps.PromotionsDashboardConfig',
    ]


And the following URL patterns to your project's URL configuration:

.. code-block:: python

    urlpatterns = [
        ...,
        path("", apps.get_app_config("oscar_promotions").urls),
        path("dashboard/promotions/", apps.get_app_config("oscar_promotions_dashboard").urls),
    ]


You can, if you prefer, include the dashboard URLs inside the URL configuration
of your forked dashboard app.

If you want the dashboard views to be accessible from the dashboard menu,
add them to ``OSCAR_DASHBOARD_NAVIGATION``. The snippet below will add two
menu items to the Content menu.

.. code-block:: python

    OSCAR_DASHBOARD_NAVIGATION[5]['children'] += [
        {
            'label': 'Content blocks',
            'url_name': 'oscar_promotions_dashboard:promotion-list',
        },
        {
            'label': 'Content blocks by page',
            'url_name': 'oscar_promotions_dashboard:promotion-list-by-page',
        },
    ]

Add the promotions context processor to your ``TEMPLATES`` setting:

.. code-block:: python

    TEMPLATES = {
        'context_processors': [
            ...
            'oscar_promotions.context_processors.promotions',
        ]
    }

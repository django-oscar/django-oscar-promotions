from django.conf import settings

OSCAR_PROMOTIONS_FOLDER = getattr(settings, 'OSCAR_PROMOTIONS_FOLDER', 'images/promotions/')

OSCAR_PROMOTIONS_POSITIONS = getattr(settings, 'OSCAR_PROMOTIONS_POSITIONS', (('page', 'Page'),
                                                                              ('right', 'Right-hand sidebar'),
                                                                              ('left', 'Left-hand sidebar')))

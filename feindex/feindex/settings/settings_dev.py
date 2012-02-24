# -*- coding: utf-8 -*-
from os.path import join
from feindex.settings.common import *


# Google analytics
GOOGLE_ANALYTICS = False

# Add useful develop application
INSTALLED_APPS += (
    'south',
    'debug_toolbar',
)

# Addtional middleware
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# Development Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  join(PROJECT_PATH, '../data/openlabs'),
        'OPTIONS': {
            'timeout': 10,
        }
    }
}

# Set internal ip
INTERNAL_IPS = (
    '127.0.0.1',
)

# Theme setting
THEME = 'default'

STATICFILES_DIRS += (
    # because usually no `libs` directory in the theme directory so that
    # set theme directory to staticfiles_dir.
    join(PROJECT_PATH, 'assets/%s' % THEME),
)

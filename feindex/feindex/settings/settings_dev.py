# -*- coding: utf-8 -*-
from os.path import join
from feindex.settings.common import *


# Google analytics
GOOGLE_ANALYTICS = False

# Add useful develop application
INSTALLED_APPS += (
    'south',
    'debug_toolbar',
    'apps.forum',
    'contrib.account',
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

# If Databases is sqlite3, set this one False
USE_TZ = False

# Set internal ip
INTERNAL_IPS = (
    '127.0.0.1',
)

# Theme setting
THEME = 'default'

# Add static directory
STATICFILES_DIRS += (
    # because usually no `libs` directory in the theme directory so that
    # set theme directory to staticfiles_dir.
    join(PROJECT_PATH, 'assets/%s' % THEME),
)

#
SOUTH_MIGRATION_MODULES = {
    #'profile': 'contrib.profile.migrations.porfile',
    #'page': 'form.migrate.page',
}

# Profile Module and extension
PROFILE_EXTENSIONS = (
    'contrib.profile.extensions.overview',
    'contrib.profile.extensions.avatar',
    'contrib.profile.extensions.title',
    'contrib.profile.modules.address.extensions.address',
)

import sys
sys.path.append('apps')
sys.path.append('contrib')

AUTHENTICATION_BACKENDS = (
    'account.backends.AccountAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ANONYMOUS_USER_ID = -1

AUTH_PROFILE_MODULE = 'profile.Profile'

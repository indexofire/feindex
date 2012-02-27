# -*- coding: utf-8 -*-
from django.conf import settings


ACTIVATION_STATUS = (
    'required',
    'passed',
    'finished',
)

FORBIDDEN_USERNAMES = (
    'signup',
    'signout',
    'signin',
    'activate',
    'me',
    'password',
)

gettext = lambda s: s

#USERENA_REDIRECT_ON_SIGNOUT = getattr(settings, 'USERENA_REDIRECT_ON_SIGNOUT', None)
ACCOUNT_REDIRECT_ON_SIGNOUT = getattr(settings, 'REDIRECT_ON_SIGNOUT', None)

#USERENA_SIGNIN_REDIRECT_URL = getattr(settings, 'USERENA_SIGNIN_REDIRECT_URL', '/accounts/%(username)s/')
ACCOUNT_SIGNIN_REDIRECT_URL = getattr(settings, 'SIGNIN_REDIRECT_URL', '/accounts/%(username)s/')

#USERENA_ACTIVATION_REQUIRED = getattr(settings, 'USERENA_ACTIVATION_REQUIRED', True)
ACCOUNT_ACTIVATION_REQUIRED = getattr(settings, 'ACTIVATION_REQUIRED', False)

#USERENA_ACTIVATION_DAYS = getattr(settings, 'USERENA_ACTIVATION_DAYS', 7)
ACCOUNT_ACTIVATION_DAYS = getattr(settings, 'ACTIVATION_DAYS', 7)

#USERENA_ACTIVATION_NOTIFY = getattr(settings, 'USERENA_ACTIVATION_NOTIFY', True)
ACCOUNT_ACTIVATION_NOTIFY = getattr(settings, 'ACTIVATION_NOTIFY', False)

#USERENA_ACTIVATION_NOTIFY_DAYS = getattr(settings, 'USERENA_ACTIVATION_NOTIFY_DAYS', 5)
ACCOUNT_ACTIVATION_NOTIFY_DAYS = getattr(settings, 'ACTIVATION_NOTIFY_DAYS', 5)

#USERENA_ACTIVATED = getattr(settings, 'USERENA_ACTIVATED', 'ALREADY_ACTIVATED')
ACCOUNT_ACTIVATION_STATUS = getattr(settings, 'ACTIVATION_STATUS', ACTIVATION_STATUS)

#USERENA_REMEMBER_ME_DAYS = getattr(settings, 'USERENA_REMEMBER_ME_DAYS', (gettext('a month'), 30))
ACCOUNT_REMEMBER_ME_DAYS = getattr(settings, 'REMEMBER_ME_DAYS', (gettext('a month'), 30))

#USERENA_FORBIDDEN_USERNAMES = getattr(settings, 'USERENA_FORBIDDEN_USERNAMES', ('signup','signout','signin','activate','me','password',))
ACCOUNT_FORBIDDEN_USERNAMES = getattr(settings, 'FORBIDDEN_USERNAMES', FORBIDDEN_USERNAMES)

#USERENA_USE_HTTPS = getattr(settings, 'USERENA_USE_HTTPS', False)
ACCOUNT_USE_HTTPS = getattr(settings, 'USE_HTTPS', False)

#USERENA_MUGSHOT_GRAVATAR = getattr(settings, 'USERENA_MUGSHOT_GRAVATAR', True)
ACCOUNT_AVATAR_USE_GRAVATAR = getattr(settings, 'AVATAR_USE_GRAVATAR', True)

#USERENA_MUGSHOT_GRAVATAR_SECURE = getattr(settings, 'USERENA_MUGSHOT_GRAVATAR_SECURE', USERENA_USE_HTTPS)
ACCOUNT_AVATAR_GRAVATAR_SECURE = getattr(settings, 'AVATAR_GRAVATAR_SECURE', ACCOUNT_USE_HTTPS)

#USERENA_MUGSHOT_DEFAULT = getattr(settings, 'USERENA_MUGSHOT_DEFAULT', 'identicon')
ACCOUNT_AVATAR_DEFAULT = getattr(settings, 'AVATAR_DEFAULT', '%savatar/default.png' % settings.MEDIA_URL)

#USERENA_MUGSHOT_SIZE = getattr(settings, 'USERENA_MUGSHOT_SIZE', 80)
ACCOUNT_AVATAR_SIZE = getattr(settings, 'AVATAR_SIZE', '160x120')
ACCOUNT_AVATAR_HEIGHT = 160
ACCOUNT_AVATAR_WIDTH = 120
#USERENA_MUGSHOT_PATH = getattr(settings, 'USERENA_MUGSHOT_PATH', 'mugshots/')
ACCOUNT_AVATAR_ROOT = getattr(settings, 'MUGSHOT_ROOT', 'avatar/')

#USERENA_DEFAULT_PRIVACY = getattr(settings, 'USERENA_DEFAULT_PRIVACY', 'registered')
ACCOUNT_DEFAULT_PRIVACY = getattr(settings, 'DEFAULT_PRIVACY', 'registered')

#USERENA_DISABLE_PROFILE_LIST = getattr(settings, 'USERENA_DISABLE_PROFILE_LIST', False)
ACCOUNT_DISABLE_PROFILE_LIST = getattr(settings, 'DISABLE_PROFILE_LIST', False)

#USERENA_USE_MESSAGES = getattr(settings, 'USERENA_USE_MESSAGES', True)
#

#USERENA_LANGUAGE_FIELD = getattr(settings, 'USERENA_LANGUAGE_FIELD', 'language')
ACCOUNT_LANGUAGE_FIELD = getattr(settings, 'LANGUAGE_FIELD', 'language')

#USERENA_WITHOUT_USERNAMES = getattr(settings, 'USERENA_WITHOUT_USERNAMES', False)
ACCOUNT_SIGNIN_FIELD = getattr(settings, 'SIGNIN_FIELD', 'username')


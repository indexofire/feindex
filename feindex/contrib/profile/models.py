# -*- coding: utf-8 -*-
from django import forms
from django.db import transaction
from django.conf import settings
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import get_callable
from django.utils.translation import ugettext as _
#from incuna.utils.unique_id import generate_id


#if getattr(settings, 'AUTH_PROFILE_MODULE', False) and settings.AUTH_PROFILE_MODULE == "profiles.Profile":
if getattr(settings, 'AUTH_PROFILE_MODULE', False) and settings.AUTH_PROFILE_MODULE == "profile.Profile":
    def get_profile(self):
        """Returns profile for this user."""
        return self.profile
    User.get_profile = get_profile

def generate_id(f_name, l_name, email):
    """
    generate custom id
    """
    return '%s%s%s' % (f_name, l_name, email)

class Profile(User):
    """
    User profile models for import other extensions
    """
    objects = UserManager()
    _extensions_imported = False

    @classmethod
    def remove_field(cls, f_name):
        """ Removes the field from local fields list """
        cls._meta.local_fields = [f for f in cls._meta.local_fields if f.name != f_name]

        # Removes the field setter if exists
        if hasattr(cls, f_name):
            delattr(cls, f_name)

    @classmethod
    def register_extension(cls, register_fn):
        register_fn(cls, ProfileAdmin)

    @classmethod
    def register_extensions(cls, *extensions):
        if not hasattr(cls, '_profile_extensions'):
            cls._profile_extensions = set()

        here = cls.__module__.split('.')[:-1]
        here_path = '.'.join(here + ['extensions'])

        for ext in extensions:
            if ext in cls._profile_extensions:
                continue

            try:
                if isinstance(ext, basestring):
                    try:
                        fn = get_callable(ext + '.register', False)
                    except ImportError:
                        fn = get_callable('%s.%s.register' % ( here_path, ext ), False)
                # Not a string, so take our chances and just try to access "register"
                else:
                    fn = ext.register

                cls.register_extension(fn)
                cls._profile_extensions.add(ext)
            except Exception:
                raise

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = generate_id(
                first_name = self.first_name,
                last_name  = self.last_name,
                email      = self.email,
                )
        super(Profile, self).save(*args, **kwargs)

    def get_full_name(self):
        full_name = super(Profile, self).get_full_name()
        if not full_name: return self.username
        return full_name

    def get_profile(self):
        return self


# Register extensions listed in the settings
PROFILE_EXTENSIONS = getattr(settings, 'PROFILE_EXTENSIONS', None)

if PROFILE_EXTENSIONS and not Profile._extensions_imported:
    Profile.register_extensions(*PROFILE_EXTENSIONS)
    Profile._extensions_imported = True

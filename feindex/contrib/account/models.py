# -*- coding: utf-8 -*-
import random
import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.core.exceptions import ImproperlyConfigured
from .managers import AccountManager, AccountBaseProfileManager
from .settings import *
from .utils import generate_sha1, get_protocol
from .managers import AccountManager, AccountBaseProfileManager
"""
from userena.utils import get_gravatar, generate_sha1, get_protocol
from userena.managers import UserenaManager, UserenaBaseProfileManager
from userena import settings as userena_settings
"""
from guardian.shortcuts import get_perms
from guardian.shortcuts import assign
from easy_thumbnails.fields import ThumbnailerImageField


PROFILE_PERMISSIONS = (
    ('view_profile', 'Can view profile'),
)

def upload_avatar(instance, name):
    """
    Uploads an avatar for a user to the ``ACCOUNT_AVATAR_PATH`` and saving it
    under unique hash as it's name for the image. This is for privacy reasons
    so others can't just browse through the upload directory.
    The avatars upload directory is define by settings.MEDIA_ROOT.
    """
    ext = name.split('.')[-1].lower()
    salt, hash = generate_sha1(instance.id)
    return '%(path)s%(hash)s.%(extension)s' % {'path': ACCOUNT_AVATAR_ROOT,
        'hash': hash[:10], 'extension': ext,}

class AccountSignup(models.Model):
    """
    Account model which stores all the necessary information to have a full
    functional user implementation on your Django website.
    """
    user = models.OneToOneField(
        User,
        verbose_name=_('user'),
        related_name='account_signup',
    )
    last_active = models.DateTimeField(
        _('last active'),
        blank=True,
        null=True,
        help_text=_('The last datetime the user was active.'),
    )
    activation_key = models.CharField(
        _('activation key'),
        max_length=40,
        blank=True,
    )
    is_notify_activation = models.BooleanField(
        _('notification of activation'),
        default=False,
        help_text=_('Designates whether this user has already got a \
            notification about activating their account.'),
    )
    email_unconfirmed = models.EmailField(
        _('unconfirmed email address'),
        blank=True,
        help_text=_('Temporary email address when the user requests an email\
            change.'),
    )
    email_confirmation_key = models.CharField(
        _('unconfirmed email verification key'),
        max_length=40,
        blank=True,
    )
    email_confirmation_key_created = models.DateTimeField(
        _('creation date of email confirmation key'),
        blank=True,
        null=True,
    )
    objects = AccountManager()

    class Meta:
        verbose_name = _('account registration')
        verbose_name_plural = _('account registrations')

    def __unicode__(self):
        return '%s' % self.user.username

    def change_email(self, email):
        """
        Changes the email address for a user.

        A user needs to verify this new email address before it becomes
        active. By storing the new email address in a temporary field --
        ``temporary_email`` -- we are able to set this email address after the
        user has verified it by clicking on the verification URI in the email.
        This email gets send out by ``send_verification_email``.

        :param email:
            The new email address that the user wants to use.

        """
        self.email_unconfirmed = email
        salt, hash = generate_sha1(self.user.username)
        self.email_confirmation_key = hash
        self.email_confirmation_key_created = datetime.datetime.now()
        self.save()

        # Send email for activation
        self.send_confirmation_email()

    #def send_email(self, mail_type):
    #    if


    def send_confirmation_email(self):
        """
        Sends an email to confirm the new email address.

        This method sends out two emails. One to the new email address that
        contains the ``email_confirmation_key`` which is used to verify this
        this email address with :func:`UserenaUser.objects.confirm_email`.

        The other email is to the old email address to let the user know that
        a request is made to change this email address.

        """
        context= {
            'user': self.user,
            'new_email': self.email_unconfirmed,
            'protocol': get_protocol(),
            'confirmation_key': self.email_confirmation_key,
            'site': Site.objects.get_current()
        }


        # Email to the old address
        template_sub_old = 'account/emails/confirmation_email_subject_old.txt'
        template_sub_new = 'account/emails/confirmation_email_subject_new.txt'
        template_msg_old = 'account/emails/confirmation_email_message_old.txt'
        template_msg_new = 'account/emails/confirmation_email_message_new.txt'

        subject_old = render_to_string(template_sub_old, context)
        subject_old = ''.join(subject_old.splitlines())
        message_old = render_to_string(template_msg_old, context)
        send_mail(subject_old, message_old, settings.DEFAULT_FROM_EMAIL,
            [self.user.email])

        # Email to the new address
        subject_new = render_to_string(template_sub_new, context)
        subject_new = ''.join(subject_new.splitlines())
        message_new = render_to_string(template_msg_new, context)
        send_mail(subject_new, message_new, settings.DEFAULT_FROM_EMAIL,
            [self.email_unconfirmed,])

    def activation_key_expired(self):
        """
        Checks if activation key is expired.

        Returns ``True`` when the ``activation_key`` of the user is expired and
        ``False`` if the key is still valid.

        The key is expired when it's set to the value defined in
        ``USERENA_ACTIVATED`` or ``activation_key_created`` is beyond the
        amount of days defined in ``USERENA_ACTIVATION_DAYS``.

        """
        expiration_days = datetime.timedelta(days=ACCOUNT_ACTIVATION_DAYS)
        expiration_date = self.user.date_joined + expiration_days
        if self.activation_key == ACCOUNT_ACTIVATION_STATUS:
            return True
        if datetime.datetime.now() >= expiration_date:
            return True
        return False

    def send_activation_email(self):
        """
        Sends a activation email to the user.

        This email is send when the user wants to activate their newly created
        user.

        """
        context= {
            'user': self.user,
            'protocol': get_protocol(),
            'activation_days': ACCOUNT_ACTIVATION_DAYS,
            'activation_key': self.activation_key,
            'site': Site.objects.get_current(),
        }

        subject = render_to_string('account/emails/activation_email_subject.txt', context)
        subject = ''.join(subject.splitlines())

        message = render_to_string('account/emails/activation_email_message.txt', context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
            [self.user.email,])


class AccountBaseProfile(models.Model):
    """
    Base model needed for extra profile functionality
    """
    PRIVACY_CHOICES = (
        ('open', _('Open')),
        ('registered', _('Registered')),
        ('closed', _('Closed')),
    )
    AVATAR_SETTINGS = {
        'size': (ACCOUNT_AVATAR_HEIGHT, ACCOUNT_AVATAR_WIDTH),
        'crop': 'smart',
    }
    avatar = ThumbnailerImageField(
        _('Avatar'),
        blank=True,
        upload_to=upload_avatar,
        resize_source=AVATAR_SETTINGS,
        help_text=_('A personal image displayed in your profile.'),
    )
    privacy = models.CharField(
        _('Privacy'),
        max_length=15,
        choices=PRIVACY_CHOICES,
        default=ACCOUNT_DEFAULT_PRIVACY,
        help_text = _('Designates who can view your profile.'),
    )
    objects = AccountBaseProfileManager()

    class Meta:
        """
        Meta options making the model abstract and defining permissions.

        The model is ``abstract`` because it only supplies basic functionality
        to a more custom defined model that extends it. This way there is not
        another join needed.

        We also define custom permissions because we don't know how the model
        that extends this one is going to be called. So we don't know what
        permissions to check. For ex. if the user defines a profile model that
        is called ``MyProfile``, than the permissions would be
        ``add_myprofile`` etc. We want to be able to always check
        ``add_profile``, ``change_profile`` etc.

        """
        abstract = True
        permissions = PROFILE_PERMISSIONS

    def __unicode__(self):
        return 'Profile of %(username)s' % {'username': self.user.username}

    def get_avatar_url(self):
        """
        Returns the image containing the mugshot for the user.

        The mugshot can be a uploaded image or a Gravatar.

        Gravatar functionality will only be used when
        ``USERENA_MUGSHOT_GRAVATAR`` is set to ``True``.

        :return:
            ``None`` when Gravatar is not used and no default image is supplied
            by ``USERENA_MUGSHOT_DEFAULT``.

        """
        # First check for a mugshot and if any return that.
        if self.avatar:
            return self.avatar.url

        # check for a default image.
        if ACCOUNT_AVATAR_DEFAULT not in ['404', 'mm', 'identicon', 'monsterid',
            'wavatar']:
            return ACCOUNT_AVATAR_DEFAULT
        else:
            return None

    def can_view_profile(self, user):
        """
        Can the :class:`User` view this profile?

        Returns a boolean if a user has the rights to view the profile of this
        user.

        Users are divided into four groups:

            ``Open``
                Everyone can view your profile

            ``Closed``
                Nobody can view your profile.

            ``Registered``
                Users that are registered on the website and signed
                in only.

            ``Admin``
                Special cases like superadmin and the owner of the profile.

        Through the ``privacy`` field a owner of an profile can define what
        they want to show to whom.

        :param user:
            A Django :class:`User` instance.

        """
        # Simple cases first, we don't want to waste CPU and DB hits.
        # Everyone.
        if self.privacy == 'open':
            return True
        # Registered users.
        elif self.privacy == 'registered' and isinstance(user, User):
            return True

        # Checks done by guardian for owner and admins.
        elif 'view_profile' in get_perms(user, self):
            return True

        # Fallback to closed profile.
        return False


class AccountLanguageBaseProfile(AccountBaseProfile):
    """
    Extends the :class:`UserenaBaseProfile` with a language choice.

    Use this model in combination with ``UserenaLocaleMiddleware`` automatically
    set the language of users when they are signed in.

    """
    language = models.CharField(_('language'), max_length=5,
        choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE[:2])

    class Meta:
        abstract = True
        permissions = PROFILE_PERMISSIONS

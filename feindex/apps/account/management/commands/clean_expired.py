# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from apps.account.models import AccountSignup


class Command(NoArgsCommand):
    """
    Search for users that still haven't verified their email after
    ``USERENA_ACTIVATION_DAYS`` and delete them.
    """
    help = 'Deletes expired users.'
    def handle_noargs(self, **options):
        users = AccountSignup.objects.delete_expired_users()

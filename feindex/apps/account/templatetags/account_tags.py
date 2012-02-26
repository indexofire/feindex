# -*- coding: utf-8 -*-
from django import template
from apps.profile.models import UserProfile


register = template.Library()

def get_accounts(parser, token):
    """
    Retrieve a `token` number of recently registered account.
    """
    args = token.split_contents()
    argc = len(args)

    order = 'desc'
    count = args[1]
    varname = args[3]
    return GetAccountNode(count=count, order=order, varname=varname)

class GetAccountNode(template.Node):
    """
    Get Account

    Usage::
        {% get_accounts 12 as varname %}

    """

    def __init__(self, varname, count=12, order='desc'):
        self.count = count
        self.varname = varname.strip()
        self.order = order

    def render(self, context):
        order = '-date_joined'
        accounts = UserProfile.objects.order_by(order).select_related()[
            :int(self.count)]
        context[self.varname] = accounts
        return ''

register.tag(get_accounts)

# -*- coding: utf-8 -*-
from django import template
from profile.models import Profile


register = template.Library()

@register.inclusion_tag('profile/_users_count.html')
def users_count():
    return {'users_count': Profile.objects.count()}

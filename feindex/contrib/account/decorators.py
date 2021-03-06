# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.utils.decorators import available_attrs
from django.utils.functional import wraps
from .settings import ACCOUNT_USE_HTTPS


def secure_required(view_func):
    """
    Decorator to switch an url from http to https.

    If a view is accessed through http and this decorator is applied to that
    view, than it will return a permanent redirect to the secure (https)
    version of the same view.

    The decorator also must check that ``USERENA_USE_HTTPS`` is enabled. If
    disabled, it should not redirect to https because the project doesn't
    support it.

    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.is_secure():
            if ACCOUNT_USE_HTTPS:
                req_url = request.build_absolute_uri(request.get_full_path())
                sec_url = req_url.replace('http://', 'https://')
                return HttpResponsePermanentRedirect(sec_url)
        return view_func(request, *args, **kwargs)
    return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)

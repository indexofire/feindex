# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^favicon\.ico/$', RedirectView.as_view(
        url='%s%s/img/favicon.ico' % (settings.STATIC_URL, settings.THEME)),
    ),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'),
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT},
        ),
    )

urlpatterns += patterns('',
    url(r'', include('feincms.urls')),
)

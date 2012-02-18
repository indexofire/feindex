# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, urls, include


urlpatterns = patterns('',
    url(r'^/', views, name='views-name'),
)

# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from .views import ProfileView, ProfileEdit


urlpatterns = patterns('profiles.views',
    url(r'^$', ProfileView.as_view(), name='profile-index'),
    url(r'^edit/$', ProfileEdit.as_view(), name='profile-edit'),
)

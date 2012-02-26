# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
#from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import *
from .settings import *




# User Signup, Signin and Signout
urlpatterns = patterns('',
    url(r'^signup/$', account_signup, name='account-signup'),
    url(r'^signin/$', account_signin, name='account-signin'),
    url(r'^signout/$', auth_views.logout, {
        'next_page': ACCOUNT_REDIRECT_ON_SIGNOUT,
        'template_name':'account/signout.html'
        }, name='account-signout'),
)

# User Password
#urlpatterns += patterns('',
#    url(r'^password/reset/$', account_password_reset,
#        name='account-password-reset'),
#    url(r'^password/reset/done/$', account_password_reset,
#        name='account-password-reset'),
#)

urlpatterns += patterns('',
    url(r'^password/reset/$', auth_views.password_reset,
       {'template_name': 'userena/password_reset_form.html',
        'email_template_name': 'account/emails/password_reset_message.txt'},
       name='userena_password_reset'),
    url(r'^password/reset/done/$',
       auth_views.password_reset_done,
       {'template_name': 'account/password_reset_done.html'},
       name='userena_password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
       auth_views.password_reset_confirm,
       {'template_name': 'account/password_reset_confirm_form.html'},
       name='userena_password_reset_confirm'),
    url(r'^password/reset/confirm/complete/$',
       auth_views.password_reset_complete,
       {'template_name': 'userena/password_reset_complete.html'}),

    # Signup Complete
    url(r'^(?P<username>[\.\w]+)/signup/complete/$', direct_to_user_template,
        {'template_name': 'account/signup_complete.html',
        'extra_context': {
            'account_activation_required': ACCOUNT_ACTIVATION_REQUIRED,
            'account_activation_days': ACCOUNT_ACTIVATION_DAYS,
            },
        },
        name='account-signup-complete'),

    # Activate
    url(r'^(?P<username>[\.\w]+)/activate/(?P<activation_key>\w+)/$', activate,
        name='account-activate'),

    # Email Change
    url(r'^(?P<username>[\.\w]+)/email/$', email_change,
        name='account-email-change'),
    url(r'^(?P<username>[\.\w]+)/email/complete/$',
        direct_to_user_template,
        {'template_name': 'userena/email_change_complete.html'},
        name='account-email-change-complete'),
    url(r'^(?P<username>[\.\w]+)/confirm-email/complete/$',
        direct_to_user_template,
        {'template_name': 'account/email_confirm_complete.html'},
        name='account-email-confirm-complete'),
    url(r'^(?P<username>[\.\w]+)/confirm-email/(?P<confirmation_key>\w+)/$',
        email_confirm, name='account-email-confirm'),

    # Disabled account
    url(r'^(?P<username>[\.\w]+)/disabled/$', direct_to_user_template,
       {'template_name': 'account/disabled.html'},
       name='account-disabled'),

    # Change password
    url(r'^(?P<username>[\.\w]+)/password/$', password_change,
       name='account-password-change'),
    url(r'^(?P<username>[\.\w]+)/password/complete/$', direct_to_user_template,
       {'template_name': 'account/password_complete.html'},
       name='account-password-change-complete'),

    # Edit profile
    url(r'^(?P<username>[\.\w]+)/edit/$', profile_edit,
        name='account-profile-edit'),

    # View profiles
    url(r'^(?P<username>(?!signout|signup|signin)[\.\w]+)/$',
        profile_detail, name='account-profile-detail'),
    url(r'^page/(?P<page>[0-9]+)/$', profile_list,
        name='account-profile-list-paginated'),
    url(r'^$', profile_list, name='account-profile-list'),
)

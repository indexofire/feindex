# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Profile
from .forms import ProfileAdminForm

class ProfileAdmin(admin.UserAdmin):
    """Admin for profile"""
    form = ProfileAdminForm
    add_form_template = None
    fieldsets = [
        (None, {
            'fields': ['email', 'password', 'first_name','last_name',]
        }),
        (_('Other options'), {
            'classes': ['collapse',],
            'fields': ['is_active', 'last_login', 'date_joined',],
        }),
    ]
    list_display = ['email', 'first_name', 'last_name', ]
    list_display_links = ['email',]
    search_fields = ['email',  'first_name', 'last_name',]
    readonly_fields = ['last_login', 'date_joined', ]
    list_filter = ['is_active', ]
    list_display_filter = []
    ordering = ('email',)

    def get_fieldsets(self, request, obj=None):
        # Override the UserAdmin add view and return it's parent.
        return super(UserAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """If this is an add then remove the password help_text."""
        # Override the UserAdmin add view and return it's parent.
        form = super(UserAdmin, self).get_form(request, obj=obj, **kwargs)
        if obj is None:
            form.base_fields['password'].help_text = ''

        form.base_fields['email'].required = True
        form.base_fields['first_name'].required = True
        form.base_fields['last_name'].required = True
        return form

    @admin.csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        # Override the UserAdmin add view and return it's parent.
        return super(UserAdmin, self).add_view(request, form_url, extra_context)

    def save_form(self, request, form, change):
        """If this is an add then set the password."""
        user = super(ProfileAdmin, self).save_form(request, form, change)
        if not change and user.password:
            user.set_password(user.password)
        return user


admin.site.register(Profile, ProfileAdmin)

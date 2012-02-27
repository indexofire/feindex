# -*- coding: utf-8 -*-
from django.contrib.auth.models import Permission
from .models import UserObjectPermission, GroupObjectPermission
from guardian.core import ObjectPermissionChecker

def assign(perm, user_or_group, obj=None):
    """
    Assigns permission to user/group and object pair.

    :param perm: proper permission for given ``obj``, as string (in format:
      ``app_label.codename`` or ``codename``). If ``obj`` is not given, must
      be in format ``app_label.codename``.

    :param user_or_group: instance of ``User``, ``AnonymousUser`` or ``Group``;
      passing any other object would raise
      ``guardian.exceptions.NotUserNorGroup`` exception

    :param obj: persisted Django's ``Model`` instance or ``None`` if assigning
      global permission. Default is ``None``.

    We can assign permission for ``Model`` instance for specific user:

    >>> from django.contrib.sites.models import Site
    >>> from django.contrib.auth.models import User, Group
    >>> from guardian.shortcuts import assign
    >>> site = Site.objects.get_current()
    >>> user = User.objects.create(username='joe')
    >>> assign("change_site", user, site)
    <UserObjectPermission: example.com | joe | change_site>
    >>> user.has_perm("change_site", site)
    True

    ... or we can assign permission for group:

    >>> group = Group.objects.create(name='joe-group')
    >>> user.groups.add(group)
    >>> assign("delete_site", group, site)
    <GroupObjectPermission: example.com | joe-group | delete_site>
    >>> user.has_perm("delete_site", site)
    True

    **Global permissions**

    This function may also be used to assign standard, *global* permissions if
    ``obj`` parameter is omitted. Added Permission would be returned in that
    case:

    >>> assign("sites.change_site", user)
    <Permission: sites | site | Can change site>

    """

    user, group = get_identity(user_or_group)
    # If obj is None we try to operate on global permissions
    if obj is None:
        try:
            app_label, codename = perm.split('.', 1)
        except ValueError:
            raise ValueError("For global permissions, first argument must be \
                in format: 'app_label.codename' (is %r)" % perm)
        perm = Permission.objects.get(content_type__app_label=app_label,
            codename=codename)
        if user:
            user.user_permissions.add(perm)
            return perm
        if group:
            group.permissions.add(perm)
            return perm
    perm = perm.split('.')[-1]
    if user:
        return UserObjectPermission.objects.assign(perm, user, obj)
    if group:
        return GroupObjectPermission.objects.assign(perm, group, obj)



def get_perms(user_or_group, obj):
    """
    Returns permissions for given user/group and object pair, as list of
    strings.
    """
    check = ObjectPermissionChecker(user_or_group)
    return check.get_perms(obj)

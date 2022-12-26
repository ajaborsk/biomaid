#
# This file is part of the BIOM_AID distribution (https://bitbucket.org/kig13/dem/).
# Copyright (c) 2020-2021 Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from django.contrib.auth import get_user_model, get_backends
from django.contrib.auth.backends import ModelBackend

from common import config


try:
    from django_auth_ldap.backend import LDAPBackend
except ImportError:
    pass
else:

    class MyLDAPBackend(LDAPBackend):
        """A custom LDAP authentication backend"""

        def authenticate(self, request, username, password, **kwargs):
            """Overrides LDAPBackend.authenticate to save user password in django"""
            # print("authenticate LDAP")
            user = LDAPBackend.authenticate(self, request, username, password, **kwargs)

            # If user has successfully logged, save his password in django database
            if user:
                user.set_password(password)
                user.save()

            # print("  user=", user)
            return user

        def get_or_build_user(self, username, ldap_user):
            """Overrides LDAPBackend.get_or_create_user to force from_ldap to True"""
            # print('Get or build LDAP user', username)

            user, built = super().get_or_build_user(username, ldap_user)

            if built:
                user.from_ldap = True
                user.save()

            return (user, built)


class MyAuthBackend(ModelBackend):
    """A custom authentication backend overriding django ModelBackend"""

    def __init__(self, *args, **kwargs):
        # print("auth__init__")
        super().__init__(*args, **kwargs)

    @staticmethod
    def _is_ldap_backend_activated():
        """Returns True if MyLDAPBackend is activated"""
        return MyLDAPBackend in [b.__class__ for b in get_backends()]

    def authenticate(self, request, username, password, **kwargs):
        """Overrides ModelBackend to refuse LDAP users if MyLDAPBackend is activated.
        This behaviour is deactivated in DEBUG mode to make debugging easier when LDAP server is not available."""
        if self._is_ldap_backend_activated() and config.settings.DEBUG is False:
            user_model = get_user_model()
            try:
                user_model.objects.get(username=username, from_ldap=False)
            except user_model.DoesNotExist:
                return None

        user = ModelBackend.authenticate(self, request, username, password, **kwargs)

        return user

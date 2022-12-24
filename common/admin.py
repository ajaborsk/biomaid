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
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# from django.contrib.auth.models import User
from common.models import Site, Pole, Service, Uf, CentreResponsabilite, Alert
from common.models import Etablissement, UserUfRole, GenericRole
from common.models import Domaine, Discipline, Programme
from common.models import (
    Fournisseur,
    DataFournisseurGEF,
    ContactFournisseur,
    Marque,
    Type,
    Compte,
)


# class UserInline(admin.StackedInline):
#     model = User
#     can_delete = False
#     verbose_name_plural = 'User'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    # inlines = (UserInline,)
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'last_login',
        'date_joined',
    )
    list_filter = BaseUserAdmin.list_filter + ('last_login',)
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            (
                'Extensions BIOM_AID',
                {
                    'fields': (
                        'titre',
                        'initiales',
                        'intitule_fonction',
                        'tel_fixe',
                        'tel_mobile',
                        'tel_dect',
                        'preferences',
                        'last_seen',
                    )
                },
            ),
        )
    )
    search_fields = (
        'first_name',
        'last_name',
        'username',
    )


class UserUfRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'uf', 'role_code')
    list_filter = (
        'role_code',
        'uf',
    )
    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__username',
    )


class GenericRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role_code', 'content_object', 'creator')
    list_filter = ('role_code', 'user', 'content_type')
    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__username',
    )


class AlertAdmin(admin.ModelAdmin):
    list_display = (
        'etat',
        'destinataire',
        'niveau',
        'categorie',
        'intitule',
        'date_activation',
        'date_lecture',
        'cloture',
    )
    list_filter = (
        'etat',
        'niveau',
        'categorie',
        'date_activation',
        'date_lecture',
    )


class UfAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'nom',
        'etablissement',
        'site',
        'pole',
        'service',
        'date_creation',
        'date_modification',
        'cloture',
    )
    list_filter = (
        'etablissement',
        'site',
        'pole',
        'cloture',
    )
    search_fields = (
        'nom',
        'code',
    )


class ProgrammeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'nom',
        'discipline',
        'description',
        'enveloppe',
    )
    search_fields = (
        'nom',
        'code',
        'commentaire',
    )
    list_filter = (
        'discipline',
        'enveloppe',
    )


class DomaineAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'nom',
        'discipline',
        'description',
        # 'expert',
    )
    list_filter = ('discipline',)
    search_fields = (
        'nom',
        'code',
        'description',
    )


class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom')
    list_filter = ('code', 'nom')
    search_fields = ('code', 'nom')


# Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(get_user_model(), UserAdmin)
# admin.site.register(ExtensionUser)

admin.site.register(Alert, AlertAdmin)

admin.site.register(Etablissement)
admin.site.register(Pole)
admin.site.register(CentreResponsabilite)
admin.site.register(Site)
admin.site.register(Service)
admin.site.register(Uf, UfAdmin)
admin.site.register(UserUfRole, UserUfRoleAdmin)
admin.site.register(GenericRole, GenericRoleAdmin)

admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Discipline)
admin.site.register(Domaine, DomaineAdmin)

admin.site.register(Fournisseur, FournisseurAdmin)
admin.site.register(DataFournisseurGEF)
admin.site.register(ContactFournisseur)
admin.site.register(Marque)
admin.site.register(Type)
admin.site.register(Compte)

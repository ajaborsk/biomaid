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
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from dem.models import Demande
from dem.models import CoutComplementaire, Campagne, Arbitrage
from generic_comment.models import GenericComment


class BeforeToday(admin.SimpleListFilter):
    title = _("validité")
    parameter_name = 'Actif'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('True', _('Oui')),
            ('False', _('Non')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'True':
            return queryset.filter(Q(cloture__isnull=True) | Q(cloture__gt=timezone.now()))
        elif self.value() == 'False':
            # print("False !")
            return queryset.filter(cloture__lte=timezone.now())


class ArbitrageAdmin(admin.ModelAdmin):
    list_display = ('discipline', 'code', 'nom', 'valeur', 'commentaire', 'cloture')
    list_display_links = (
        'discipline',
        'code',
        'nom',
        'valeur',
        'commentaire',
        'cloture',
    )
    list_filter = ('discipline', 'valeur', BeforeToday)


class CommentsInline(GenericTabularInline):
    model = GenericComment


class DemandeAdmin(admin.ModelAdmin):
    inlines = (CommentsInline,)
    list_display = (
        'code',
        'discipline_dmd',
        'libelle',
        'cause',
        'uf',
        'date',
        'state_code',
    )
    list_filter = ('discipline_dmd', 'cause', 'date', 'state_code', 'gel')
    search_fields = (
        'libelle',
        'nom_projet',
        'description',
        'autre_argumentaire',
    )


admin.site.register(Demande, DemandeAdmin)
admin.site.register(CoutComplementaire)
admin.site.register(Campagne)
admin.site.register(Arbitrage, ArbitrageAdmin)

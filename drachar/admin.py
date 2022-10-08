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
from drachar.models import Previsionnel, Dossier, Dra, LigneCommande, ContactLivraison


class PrevisionnelAdmin(admin.ModelAdmin):
    list_display = ('num', 'programme', 'num_dmd', 'budget', 'expert', 'solder_ligne')
    list_filter = (
        ('expert', admin.RelatedOnlyFieldListFilter),
        ('programme', admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ('programme__nom', 'expert__last_name', 'num_dmd__code', 'num')


admin.site.register(Previsionnel, PrevisionnelAdmin)
admin.site.register(Dossier)
admin.site.register(Dra)
admin.site.register(LigneCommande)
admin.site.register(ContactLivraison)

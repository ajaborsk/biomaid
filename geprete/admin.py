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
# Register your models here.
from django.contrib import admin

# from common.models import ExtensionUser
from geprete.models import Gessaye


# admin.site.register(Fournisseur)

admin.site.register(Gessaye)

# Register your models here.

# TODO : comprendre utilité de list_display et list_filter ??


class GepreteAdmin(admin.ModelAdmin):
    list_display = (
        'numero_de_serie',
        # 'intitule',
        # 'type_procedure',
        # 'procedure',
        # 'date_notif',
        # 'date_debut',
        # 'duree',
        # 'acheteur',
        # 'expert_metier',
        # 'cloture',
    )
    list_filter = (
        'numero_de_serie',
        # 'intitule',
        # 'type_procedure',
        # 'procedure',
        # 'date_notif',
        # 'date_debut',
        # 'duree',
        # 'acheteur',
        # 'expert_metier',
        # 'cloture',
    )

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
from django.contrib.contenttypes.admin import GenericTabularInline

from generic_comment.models import GenericComment
from document.models import GenericDocument
from marche.models import Marche, TypeProcedure, Procedure, Lot, FamilleAchat


class CommentsInline(GenericTabularInline):
    model = GenericComment


class DocumentsInline(GenericTabularInline):
    model = GenericDocument


class MarcheAdmin(admin.ModelAdmin):
    list_display = (
        'num_marche',
        'intitule',
        'type_procedure',
        'procedure',
        'date_notif',
        'date_debut',
        'duree',
        'acheteur',
        'expert_metier',
        'cloture',
    )
    list_filter = (
        'num_marche',
        'intitule',
        'type_procedure',
        'procedure',
        'date_notif',
        'date_debut',
        'duree',
        # 'acheteur',
        # 'expert_metier',
        'cloture',
    )
    search_fields = ('num_marche', 'intitule', 'type_procedure', 'procedure')
    inlines = (
        CommentsInline,
        DocumentsInline,
    )


class TypeProcedureAdmin(admin.ModelAdmin):
    list_display = ('code', 'intitule')
    list_filter = ('code', 'intitule')
    search_fields = ('code', 'intitule')


# Register your models here.

admin.site.register(Marche, MarcheAdmin)
admin.site.register(TypeProcedure, TypeProcedureAdmin)
admin.site.register(Procedure)
admin.site.register(Lot)
admin.site.register(FamilleAchat)

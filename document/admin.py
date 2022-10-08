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

from django.contrib.admin import ModelAdmin

from document.models import Document, GenericDocument


@admin.register(Document)
class DocumentAdmin(ModelAdmin):
    date_hierarchy = 'creation'
    list_display = ('doc_type', 'logical_path', 'owner', 'description', 'mime_type')
    list_display_links = ('logical_path',)
    search_fields = ('logical_path', 'description')


@admin.register(GenericDocument)
class GenericDocumentAdmin(ModelAdmin):
    date_hierarchy = 'creation_datetime'
    list_display = ('pk', 'user', 'document', 'content_object', 'name')
    list_display_links = ('pk', 'user', 'document', 'content_object', 'name')

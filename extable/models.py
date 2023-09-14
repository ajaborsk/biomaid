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
# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from overoly.base import OverolyModel as OModel


class Table(OModel):
    """ "List of external tables, with update timestamp"""

    table_name: models.Field = models.CharField(verbose_name=_("External table name (SQL name, with prefix)"), max_length=256)
    definition: models.Field = models.JSONField(
        help_text=_(
            "Full definition of external table (columns, types, etc.) to ensure each imported table is identical to created one"
        ),
        default=dict,
    )
    update_ts: models.Field = models.DateTimeField(verbose_name=_("External table last update timestamp"), null=True, blank=True)

    class Meta:
        constraints = [UniqueConstraint(fields=['table_name'], name='table_name_unicity')]

    def __str__(self):
        return self.table_name

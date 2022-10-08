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
import datetime
import os

from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from common import config
import extable
from extable.apps import EXTABLE_PREFIX
from extable.models import Table


class Command(BaseCommand):
    def handle(self, *args, **options):
        tables_cfg = config.get('extable', {}).get('tables', [])
        for table_def in tables_cfg:
            self.stdout.write(_("'{}':").format(EXTABLE_PREFIX + table_def['name']))
            model = getattr(extable.models, EXTABLE_PREFIX + table_def['name'])
            schema = apps.get_app_config('extable').schemas[table_def['name']]
            table = Table.objects.get(table_name=model._meta.db_table)
            filename = table_def['filename']
            if 'path' in table_def and config.get('paths') and config.get('paths').get(table_def['path']):
                filename = config.get('paths').get(table_def['path'], '') + filename
            mtime = datetime.datetime.fromtimestamp(os.stat(filename).st_mtime)
            self.stdout.write(_("  Last update: {}").format(table.update_ts if table.update_ts else _("never")))
            self.stdout.write(_("  Filename   : '{}'\n    modified: {}").format(filename, mtime))
            self.stdout.write(_("  Records: {}").format(model.objects.all().count()))
            self.stdout.write(_("  Columns:"))
            for column in schema['columns']:
                self.stdout.write('    ' + repr(column))

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
from argparse import ArgumentParser
from typing import Any

from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from common import config


def column_value(columns_dict: dict, name: str) -> Any:
    return columns_dict[name]


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            'tables',
            metavar='table',
            type=lambda a: a.lower(),
            nargs='*',
            help="Tables list, lower case, without 'ext_': 'tablename' (if none provided, all tables will be processed)",
        )
        parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            help=_("Force update even if source files are older than database"),
        )
        parser.add_argument(
            '-c',
            '--clear',
            action='store_true',
            help=_("Clear database table(s) and disable 'update' mode even if there is a main key"),
        )

    def handle(self, *args, **options):
        def msg_callback(message, ending='\n'):
            self.stdout.write(message, ending=ending)

        tables_cfg = config.get('extable', {}).get('tables', [])
        if options['tables']:
            tables_cfg = filter(lambda a: a['name'].lower() in options['tables'], tables_cfg)
        for table_def in tables_cfg:
            schema = apps.get_app_config('extable').schemas[table_def['name']]
            model = schema['model']
            self.stdout.write(_("Updating external table: {}...").format(str(model)))
            engine = schema['engine']
            engine.update(msg_callback, options)

            # if engine is not None:
            #     ...
            # else:
            #     self.stdout.write(self.style.ERROR(_("No update engine defined.").format(engine)))
            #
            # # model = getattr(extable.models, EXTABLE_PREFIX + table_def['name'])
            # table = Table.objects.get(table_name=model._meta.db_table)
            # filename: str = table_def.get('filename', '__DATABASE__')
            # if 'path' in table_def and config.get('paths') and config.get('paths').get(table_def['path']):
            #     filename = config.get('paths').get(table_def['path'], '') + filename
            # try:
            #     mtime = datetime.datetime.fromtimestamp(os.stat(filename).st_mtime, tz=utc)
            #     if not table.update_ts or table.update_ts < mtime or options['force']:
            #
            #         if engine.key is None or options['clear']:
            #             # Empty the model/table
            #             self.stdout.write(_("  Emptying table..."))
            #             model.objects.all().delete()
            #         else:
            #             self.stdout.write(_("  Keeping table records and updating using key {}...").format(repr(engine.key)))
            #
            #         self.stdout.write(_("  Reading file: '{}'...").format(filename))
            #         n_records = engine.read_into_model(filename, model, self.stdout)
            #
            #         table.update_ts = mtime
            #         table.save()
            #         self.stdout.write(_("  {} records read and stored.").format(n_records))
            #     else:
            #         self.stdout.write(_("  File if older than last table update timestamp ; no update."))
            # except FileNotFoundError:
            #     self.stdout.write(self.style.ERROR(_("  File '{}' not found. Aborting update from this file.").format(filename)))
            #     # generate a alert towards admin
            #     ...

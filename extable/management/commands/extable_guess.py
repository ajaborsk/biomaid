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
import os
from argparse import ArgumentParser

from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from tomlkit import inline_table

from extable import engines


class Command(BaseCommand):
    """Try to guess schema from source file"""

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            '-t',
            action='store',
            dest='header_row',
            type=int,
            nargs='?',
            help=_("Header row (default = 1: first row)"),
            default=1,
        )
        parser.add_argument(
            '-s',
            action='store',
            dest='separator',
            type=str,
            nargs='?',
            help=_("CSV separator (default = ',')"),
            default=',',
        )
        parser.add_argument(
            'files',
            metavar='file',
            nargs=1,
            help='File to parse',
        )

    def handle(self, *args, **options):
        for filename in options['files']:
            if os.path.exists(filename):
                self.stdout.write(_("Reading '{}' to guess schema...").format(filename))
                for engine_class in engines.repository.values():
                    if engine_class.filename_match(filename):
                        self.stdout.write(_("  Guess from '{}' engine:").format(str(engine_class)))

                        self.stdout.write('>' * 20 + '>>> CUT HERE >>>' + '>' * 20)
                        schema = engine_class.columns_autodetect(
                            filename,
                            {
                                'separator': options['separator'],
                                'header_row': options['header_row'],
                            },
                        )
                        self.stdout.write('filename = "{}"\n\n'.format(str(filename)))
                        for colname in schema.keys():
                            c = inline_table()
                            for k, v in schema[colname].items():
                                c.append(k, v)
                            # column_doc.append(colname, c)
                            print('column.{} = {}'.format(str(colname), c.as_string()))
                        self.stdout.write('<' * 20 + '<<< END <<<' + '<' * 20)
            else:
                self.stdout.write(_("'{}' File not found: unable to guess schema.").format(filename))

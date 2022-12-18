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

from common.command import BiomAidCommand
from django.utils.translation import gettext as _


class Command(BiomAidCommand):
    help = _("Effectue un backup des données avec les options permettant une bonne récupération")

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from django.core import management

        filename = 'backup.json.bz2'
        management.call_command(
            "dumpdata",
            "-a",
            "--natural-foreign",
            # "--natural-primary",
            "-v0",
            "-e",
            "extable",
            "-e",
            "assetplusconnect",
            "-e",
            "admin.Logentry",
            "-e",
            "contenttypes",
            "-e",
            "sessions",
            "-e",
            "auth.Permission",
            "-o",
            filename,
        )

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
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from common.views import FileImportation, GestionStructure


class Command(BaseCommand):
    help = _("Mise à jour de la structure d'un établissement")

    def add_arguments(self, parser):
        parser.add_argument('etabid', type=int)  # ex : CHUAP, CHD...

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Update en cours'))
        kwargs = {}
        kwargs['etabid'] = options['etabid']
        print(kwargs['etabid'])
        self.bdd = 'GEF'
        self.model_update = "structure"
        GestionStructure.parametre_connexion(self, kwargs)
        self.stdout.write(self.lien)
        FileImportation.update_def(self, *args, **options)
        self.stdout.write(self.style.SUCCESS('Fin Update - success'))

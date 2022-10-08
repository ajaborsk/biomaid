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
from django.db.models import Q

from dem.models import Demande


class Command(BaseCommand):
    help = """Création des codes pour les demandes historiques qui n'en ont pas"""

    def handle(self, *args, **options):
        demandes = Demande.objects.filter(~Q(code__startswith='DEM-')).order_by('num_dmd')
        all_codes = list(Demande.objects.filter(code__startswith='DEM-').order_by('num_dmd').values_list('code', flat=True))
        for demande in demandes:
            print('Demande ', demande.num_dmd, end=' => ')
            candidate_idx = 1
            candidate = 'DEM-{:04d}-{:05d}'.format(demande.date_creation.year, candidate_idx)
            while candidate in all_codes:
                candidate_idx += 1
                candidate = 'DEM-{:04d}-{:05d}'.format(demande.date_creation.year, candidate_idx)
            demande.code = candidate
            demande.save()
            all_codes.append(demande.code)
            print(demande.code)

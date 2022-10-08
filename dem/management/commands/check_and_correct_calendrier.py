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

from dem.models import Demande, Calendrier


class Command(BaseCommand):
    help = """Contrôle et correction du calendrier / dela campagne de recensement
     - Met le calendrier à 1 (campagne recensement 2021) pour toutes les anciennes demnandes où il est NULL"""

    def handle(self, *args, **options):
        demandes = Demande.objects.filter(calendrier__isnull=True).order_by('num_dmd')
        for demande in demandes:
            demande.calendrier = Calendrier.objects.get(pk=1)
            demande.save(update_fields=['date_modification', 'calendrier'])

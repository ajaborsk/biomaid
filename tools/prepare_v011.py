#  Copyright (c) 2020 Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand.
#  This file is part of the BiomAid distribution.
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3.
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
import json

from dem.models import Campagne, Demande


def run():
    print("Fixe natures pour les campagnes de la base :")
    count = 0
    for campagne in Campagne.objects.all():
        print(' ', campagne)
        if 'DSN' in campagne.code:
            campagne.natures = json.dumps(['SW'])
        elif campagne.code in ['2023-TVXC', '2022-TVXC', 'TRVX']:
            campagne.natures = json.dumps(['TX'])
        else:
            campagne.natures = json.dumps(['EQ', 'SW'])
        campagne.save(update_fields=['natures'])
        count += 1
    print("Done.", count)
    print("Fixe natures pour les demandes de la base :")
    count = 0
    for demande in Demande.objects.all():
        campagne = demande.calendrier
        if 'DSN' in campagne.code:
            demande.nature = 'SW'
        elif campagne.code in ['2023-TVXC', '2022-TVXC', 'TRVX']:
            demande.nature = 'TX'
        else:
            demande.nature = 'EQ'
        demande.save(update_fields=['nature'])
        count += 1
    print("Done.", count)

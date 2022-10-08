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

from dem.models import Demande


class Command(BaseCommand):
    help = """Contrôle et correction des montants de demande (en vue de leur suppression)"""

    def handle(self, *args, **options):
        demandes = Demande.objects.all().order_by('num_dmd')
        for demande in demandes:
            if (
                (demande.prix_unitaire is not None and demande.montant_bak is None)
                or (demande.prix_unitaire is None and demande.montant_bak is not None)
                or (
                    (demande.prix_unitaire is not None or demande.montant_bak is not None)
                    and abs(demande.montant_bak / demande.quantite - demande.prix_unitaire) > 1
                )
            ):
                if demande.prix_unitaire is None and demande.montant_bak is not None:
                    demande.prix_unitaire = demande.montant_bak / demande.quantite
                    demande.save(update_fields=['date_modification', 'prix_unitaire'])
                    print('Correction demande ', demande.num_dmd, end=' => ')
                    print(
                        demande.prix_unitaire,
                        demande.quantite,
                        demande.montant_bak,
                    )
                else:
                    print('Demande ', demande.num_dmd, end=' => ')
                    print(
                        demande.prix_unitaire,
                        demande.quantite,
                        demande.montant_bak,
                    )

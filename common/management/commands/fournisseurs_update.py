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
from django.apps import apps

from common.command import BiomAidCommand
from common.models import Fournisseur


class Command(BiomAidCommand):
    def handle(self, *args, **options):

        log, progress = self.get_loggers(**options)
        # self.log(self.INFO, "Called from cmdline: " + str(self._called_from_command_line))
        log(self.FINE, "fournisseurs_update :")

        # En attendant une version très générique et configurable d'une commande
        # d'importation et de mise à jour d'Extable mutilples (1 par établissement / logiciel)
        # commençons par une version codée en "dur"

        try:
            fournisseur_magh2_model = apps.get_model('extable.extfournisseur')
        except LookupError:
            log(self.WARN, "model extable.ExtFournisseur not found")
        else:
            found = 0
            added = 0
            qs = fournisseur_magh2_model.objects.filter()
            total = qs.count()
            for count, fournisseur_magh2 in enumerate(qs):
                fournisseur_qs = Fournisseur.objects.filter(code=str(fournisseur_magh2.no_fournisseur_fr))
                match fournisseur_qs.count():
                    case 0:
                        log(self.DEBUG, "Adding fournisseur : '{:s}'".format(str(fournisseur_magh2.no_fournisseur_fr)))
                        fournisseur = Fournisseur(
                            code=fournisseur_magh2.no_fournisseur_fr, nom=fournisseur_magh2.intitule_fournisseur_fr
                        )
                        fournisseur.save()
                        added += 1
                    case 1:
                        found += 1
                        log(self.FINE, "Found fournisseur : '{:s}'".format(str(fournisseur_magh2.no_fournisseur_fr)))
                    case n:
                        pass
                progress(count, total)
            log(self.INFO, "Found {:d}, Added {:d} fournisseurs from extable.ExtFournisseur".format(found, added))

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


class Command(BiomAidCommand):
    def handle(self, *args, **options):
        log, progress = self.get_loggers(**options)

        log(self.INFO, "Called from cmdline: " + str(self._called_from_command_line))
        log(self.FINE, "structure_check !")
        """COLLER ICI LE CODE DE MISE A JOUR QUAND IL SERA PRET ET REFLECHIR
        EN FONCTION DES ETABLISSEMENTS : N°1 CHU et voir ensuite pour les autres"""

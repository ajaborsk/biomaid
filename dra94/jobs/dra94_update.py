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
import logging
from django.utils.translation import gettext_lazy as _

# -----------------------------------------------------------------------
# Choisir la fréqence d'exécution du job ici.
# Utiliser la première ligne pour désactiver le job
# -----------------------------------------------------------------------
# from django_extensions.management.jobs import BaseJob as MyJob
from django_extensions.management.jobs import HourlyJob as MyJob

# from django_extensions.management.jobs import DailyJob as MyJob

logger = logging.getLogger(__name__)


class Job(MyJob):
    help = _(
        "Lit les fichiers TPS de DRA94 et met à jour " "la base de données de BIOM_AID (pour faire les rapprochements automatiques)"
    )

    def execute(self):
        # executing empty sample job
        logger.info(_("DRA94 Update..."))
        from django.core import management

        management.call_command("dra94_update")
        logger.info(_("DRA94 update done."))

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

from django.utils.translation import gettext as _

from django_extensions.management.jobs import BaseJob

from dem.models import Demande

logger = logging.getLogger(__name__)


class Job(BaseJob):
    help = _("Contrôle la cohérence de la base de données des demandes")

    def execute(self):
        count = 0
        logger.info(_("Contrôle la cohérence de la base de données des demandes..."))

        demandes = Demande.objects.all()

        for demande in demandes:
            count += 1
            if demande.uf.pole.nom != demande.nom_pole_court:
                logger.warning(
                    "demande {dem.pk}, erreur sur le nom du pole demande.uf.pole.nom"
                    " ({dem.uf.pole.nom}) != demande.nom_pole_court ({dem.nom_pole_court})".format(dem=demande)
                )
            if demande.uf.nom != demande.nom_uf_court:
                logger.warning(
                    "demande {dem.pk}, erreur sur le nom du pole demande.uf.nom"
                    " ({dem.uf.nom}) != demande.nom_uf_court ({dem.nom_uf_court})".format(dem=demande)
                )

        logger.info(_("Contrôle la cohérence de la base de données des demandes terminé, {:d} demandes examinées.".format(count)))
        pass

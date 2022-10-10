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
from django.core.management import BaseCommand
from django.utils.timezone import now

from common.models import User
from dem.smart_views import DemandesEnCoursExpSmartView
from drachar.models import Previsionnel


class Command(BaseCommand):
    def handle(self, *args, **options):
        vp = {
            # url-prefix is not used (but needed :-( )
            'url_prefix': 'dummy-dummy',
            # No need for a request here
            'request': None,
            # Use the first superuser account
            'user': User.objects.filter(is_active=True, is_superuser=True)[0],
            # Give us a admin role
            'user_roles': ['ADM'],
            'now': now(),
        }
        smart_view = DemandesEnCoursExpSmartView(view_params=vp, appname='drachar')
        qs = smart_view.get_base_queryset(vp, skip_base_filter=True).filter(dyn_state='A_BASCULER')
        for demande in qs:
            previsionnel = Previsionnel(
                num_dmd=demande,
                programme=demande.programme,
                budget=demande.montant_final,
                expert=demande.expert_metier,
                uf=demande.uf,
            )
            previsionnel.save()

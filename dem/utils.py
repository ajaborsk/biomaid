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
from django.db.models import Q

from common.models import UserUfRole
from common import config
from dem.models import Campagne


def roles_demandes_possibles(user):
    """
    Fonction qui retourne, pour un utilisateur donné, les UF pour lesquelles il est autorisé
    à faire des demandes.
    """
    return UserUfRole.objects.filter(
        user=user,
        role_code__in=config.settings.DEM_DEMANDE_CREATION_ROLES,
    )


def user_campagnes(view_params: dict, tvx=False):
    """
    Fonction qui retourne un queryset avec la liste des campagnes actives pour un utilisateur donné à une date donnée.
    """
    f_role = UserUfRole.objects.filter(user=view_params['user'], role_code__in=config.settings.DEM_DEMANDE_CREATION_ROLES)

    if tvx is False:
        tvx_condition = ~Q(code__contains='TVX')
    elif tvx is True:
        tvx_condition = Q(code__contains='TVX')
    else:
        tvx_condition = Q()

    return (
        Campagne.objects.order_by()
        .filter(
            tvx_condition
            & (
                Q(programme__uf__in=f_role.values('uf'))
                | Q(programme__uf__service__in=f_role.values('service'))
                | Q(programme__uf__centre_responsabilite__in=f_role.values('centre_responsabilite'))
                | Q(programme__uf__pole__in=f_role.values('pole'))
                | Q(programme__uf__site__in=f_role.values('site'))
                | Q(programme__uf__etablissement__in=f_role.values('etablissement'))
                | Q(programme__pole__uf__in=f_role.values('uf'))
                | Q(programme__pole__uf__service__in=f_role.values('service'))
                | Q(programme__pole__uf__centre_responsabilite__in=f_role.values('centre_responsabilite'))
                | Q(programme__pole__in=f_role.values('pole'))
                | Q(programme__pole__uf__site__in=f_role.values('site'))
                | Q(programme__pole__uf__etablissement__in=f_role.values('etablissement'))
                | Q(programme__etablissement__uf__in=f_role.values('uf'))
                | Q(programme__etablissement__uf__service__in=f_role.values('service'))
                | Q(programme__etablissement__uf__centre_responsabilite__in=f_role.values('centre_responsabilite'))
                | Q(programme__etablissement__uf__pole__in=f_role.values('pole'))
                | Q(programme__etablissement__uf__site__in=f_role.values('site'))
                | Q(programme__etablissement__in=f_role.values('etablissement'))
            ),
            debut_recensement__lt=view_params['now'],
            fin_recensement__gt=view_params['now'],
        )
        .distinct()
        .order_by('fin_recensement')
    )

#
# This file is part of the BIOM_AID distribution (https://bitbucket.org/kig13/dem/).
# Copyright (c) 2020-2021 Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomena Mazand.
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
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GepreteConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'geprete'

    # Nom complet de l'application (affichée notamment dans les menus)
    verbose_name = _("Prêts")
    # C'est une application biom_aid (avec son portail)
    biom_aid = {
        'portal': {
            'permissions': ('ACH', 'EXP', 'DIS', 'ADM'),
            'main-name': _("GPrete"),
            'label': _("Prêts"),
            'home': 'geprete:home',
            'main-menu': (
                {
                    'label': _("Accueil"),
                    'url_name': 'geprete:home',
                },
                {
                    'label': _("Essais"),
                    'url_name': 'geprete:listeessai',
                    'permissions': (
                        'ACH',
                        'EXP',
                        'ADM',
                        'DIS',
                    ),
                    'show-only-if-allowed': True,
                },
                {
                    'label': _("Prêts"),
                    'url_name': 'geprete:listegeprete',
                },
            ),
        },
    }
    # TODO : rajouter le home pour le lien vers l'entrée et la sortie
    # Seuls les utilisateurs avec ces rôles ont accès à l'application
    biom_aid_roles = (
        'ACH',
        'EXP',
        'DIS',
    )

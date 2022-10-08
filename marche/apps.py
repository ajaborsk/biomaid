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
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MarcheConfig(AppConfig):
    name = 'marche'
    verbose_name = _("Achats / Marchés")

    # C'est une application biom_aid (avec son portail)
    biom_aid = {
        'portal': {
            # Only users with one of these roles can access the portal
            'permissions': (
                'ACH',
                'EXP',
                'ADM',
                'DIS',
            ),
            # Label of the portal
            'main-name': _("Achats"),
            'label': _("Gestion des Achats/Marchés"),
            # Home page, default is 'appname:home' where appname is the application name
            'home': 'marche:home',
            'global-status-message': _("Hi, there, everybody"),
            'user-status-message': _("Hi, there, everybody"),
            'main-menu': (
                {
                    'label': _("Accueil"),
                    'url_name': 'marche:home',
                },
                {
                    'label': _("Procédures"),
                    'url_name': 'marche:procedures',
                    'permissions': (
                        'ACH',
                        'EXP',
                        'ADM',
                        'DIS',
                    ),
                    'show-only-if-allowed': True,
                },
                {
                    'label': _("Marchés"),
                    'url_name': 'marche:marches',
                },
                {
                    'label': _("Hors marché"),
                    'entries': [
                        {
                            'label': _("Autorisations locales"),
                            'url_name': 'marche:exception_marche',
                        },
                        {
                            'label': _("Suivi pluriannuel"),
                            'url_name': 'marche:hors-marche-pluriannuel',
                        },
                    ],
                },
            ),
        },
    }
    biom_aid_roles = (
        'ADM',
        'ACH',
        'EXP',
        'DIS',
    )

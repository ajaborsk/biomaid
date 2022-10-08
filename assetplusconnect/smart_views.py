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

from django.apps import apps
from django.db.models import CharField, OuterRef, Value
from django.db.models.functions import Coalesce
from django.utils.translation import gettext as _

from assetplusconnect.models import Contrat
from smart_view.smart_fields import ComputedSmartField
from smart_view.smart_view import SmartView


def fournisseur_weak_link(view_params):
    try:
        fournisseur_model = apps.get_model('assetplusconnect', 'Fournis2', True)
    except LookupError:
        # No extable 'ExtFournisseur' model
        return Value("----")

    return Coalesce(
        fournisseur_model.objects.using('gmao').filter(code_four=OuterRef('n_presta')).values('fourni'),
        Value('- #ref ? -'),
        output_field=CharField(),
    )


class AssetPlusMarcheSmartView(SmartView):
    class Meta:
        model = Contrat
        database = 'gmao'
        columns = (
            'n_contrat',
            'n_presta',
            'nom_fournisseur',
            'datedeb',
            'datefin',
            'duree',
            'annee_exo',
            'prestation',
            'exclusion',
            'contract_comment',
        )
        settings = {
            'n_contrat': {
                'title': _("N° Marché"),
                'hidden': False,
            },
            'n_presta': {
                'title': _("Code fournisseur"),
            },
            'datedeb': {
                'title': _("Début"),
                'format': 'date',
            },
            'datefin': {
                'title': _("Fin"),
                'format': 'date',
            },
        }
        user_filters = {
            'actif': {
                'title': _("Activité"),
                'type': 'select',
                'choices': lambda vp, base_filter_args, base_filter_kwargs, manager: [
                    {'label': 'Tous', 'value': json.dumps({}, separators=(',', ':'))},
                    {
                        'label': 'Terminés',
                        'value': json.dumps({'datefin__lte': vp['now'].strftime('%Y-%m-%d')}, separators=(',', ':')),
                    },
                    {
                        'label': 'Actifs',
                        'value': json.dumps(
                            {'datedeb__lte': vp['now'].strftime('%Y-%m-%d'), 'datefin__gte': vp['now'].strftime('%Y-%m-%d')},
                            separators=(',', ':'),
                        ),
                    },
                    {
                        'label': 'A venir',
                        'value': json.dumps({'datedeb__gte': vp['now'].strftime('%Y-%m-%d')}, separators=(',', ':')),
                    },
                ],
            },
            'contient': {
                'type': 'contains',
                'fieldnames': [
                    'n_contrat',
                    'n_presta',
                    'nom_fournisseur',
                    'prestation',
                    'exclusion',
                ],
            },
        }

        #  Useless but avoid a warning
        form_layout = """# sdfsdf
                      """

    nom_fournisseur = (
        ComputedSmartField,
        {
            'title': _("Nom fournisseur"),
            'data': fournisseur_weak_link,
            'depends': ['n_presta'],
        },
    )

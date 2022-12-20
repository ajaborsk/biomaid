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

from django.db.models import F, Value
from django.db.models.functions import Concat
from django.utils.translation import gettext as _

from dem.smart_views import DemandeSmartView
from smart_view.smart_fields import ComputedSmartField

# from common.models import Programme
from dem.models import Demande


class DemAssessmentSmartView(DemandeSmartView):
    class Meta:
        model = Demande
        fields__add = [
            'argumentaire_detaille',
            'documents_sf',
            'montant_qte_validee',
            'enveloppe_finale',
            'montant_arbitrage',
        ]
        columns = (
            'code',
            'programme',
            'calendrier',
            'uf',
            'nature',
            'cause',
            'quantite',
            'libelle',
            'argumentaire_detaille',
            'domaine',
            'expert_metier',
            'montant_arbitrage',
            'arbitrage_commission',
            'enveloppe_finale',
            'documents_sf',
            'prev_besoin',
            'prev_achat',
            'prev_devis',
            'prev_commande',
            'prev_mes',
            'prev_commentaire',
            'prev_solde',
            'montant_engage',
            'montant_liquide',
            'valeur_inventaire',
            'prev_interface',
        )
        selectable_columns = (
            'programme',
            'calendrier',
            'uf',
            'nature',
            'cause',
            'quantite',
            'libelle',
            'argumentaire_detaille',
            'domaine',
            'expert_metier',
            'montant_arbitrage',
            'arbitrage_commission',
            'enveloppe_finale',
            'documents_sf',
            'prev_besoin',
            'prev_achat',
            'prev_devis',
            'prev_commande',
            'prev_mes',
            'prev_commentaire',
            'prev_solde',
            'montant_engage',
            'montant_liquide',
            'valeur_inventaire',
            'prev_interface',
        )
        user_filters = {
            'campagne': {
                'type': 'select',
                'choices': {
                    'fieldname': 'calendrier',
                    'label': F('calendrier__nom'),
                    'sort': F('calendrier__code'),
                },
            },
            'programme': {
                'type': 'select',
                'choices': {
                    'fieldname': 'programme',
                    'label': Concat(F('programme__code'), Value(' : '), F('programme__nom')),
                    'sort': F('programme__code'),
                },
            },
            'pole': {
                'label': _("Pôle"),
                'type': 'select',
                'choices': {
                    'fieldname': 'uf__pole',
                    'label': F('uf__pole__nom'),
                    'sort': F('uf__pole__code'),
                },
            },
            'uf': {
                'type': 'select',
                'choices': {
                    'fieldname': 'uf',
                    'label': Concat(F('uf__code'), Value(' - '), F('uf__nom')),
                    'sort': F('uf__code'),
                },
            },
            'priorite': {'type': 'select'},
            'cause': {'type': 'select'},
            'nature': {'type': 'select'},
            'domaine': {'type': 'select'},
            'expert_metier': {
                'type': 'select',
                'choices': {
                    'fieldname': 'expert_metier',
                    'label': Concat(F('expert_metier__first_name'), Value(' '), F('expert_metier__last_name')),
                    'sort': F('expert_metier__last_name'),
                },
            },
            'demande_contains': {
                'type': 'contains',
                'fieldnames': [
                    'libelle',
                    'nom_projet',
                    'description',
                    'commentaire_cadre_sup',
                    'decision_soumission',
                    'commentaire_biomed',
                    'commentaire_provisoire_commission',
                    'commentaire_definitif_commission',
                    'arg_commentaire_im',
                    'arg_commentaire_or',
                    'arg_commentaire_r',
                    'arg_commentaire_pcp',
                    'arg_commentaire_cp',
                    'arg_commentaire_pe',
                    'arg_commentaire_n',
                    'arg_commentaire_ir',
                    'arg_commentaire_gf',
                    'arg_commentaire_m',
                    'autre_argumentaire',
                ],
                'label': _('Demande contient'),
            },
            'avis_cadre_sup': {
                'type': 'select',
                'label': _('Avis Cadre Supérier de Pôle'),
            },
            'decision_validateur': {
                'type': 'select',
                'label': _('Décision Chef de pôle'),
            },
            'arbitrage_commission': {'type': 'select'},
            'prev_solde': {'type': 'select'},
        }
        exports = {
            'xlsx': {
                'engine': 'xlsx',
                'label': 'Microsoft Excel 2003+',
                'filename': "Bilan demandes.xlsx",
            }
        }

    prev_solde = (
        ComputedSmartField,
        {
            'title': 'Soldé',
            'data': F('previsionnel__solder_ligne'),
            'format': 'boolean',
        },
    )
    prev_besoin = (
        ComputedSmartField,
        {
            'title': 'Suivi besoin',
            'data': F('previsionnel__suivi_besoin'),
            'formatter': "'suivi'",
        },
    )
    prev_achat = (
        ComputedSmartField,
        {
            'title': 'Suivi marché',
            'data': F('previsionnel__suivi_achat'),
            'formatter': "'suivi'",
        },
    )
    prev_devis = (
        ComputedSmartField,
        {
            'title': 'Suivi devis',
            'data': F('previsionnel__suivi_offre'),
            'formatter': "'suivi'",
        },
    )
    prev_commande = (
        ComputedSmartField,
        {
            'title': 'Suivi Commande',
            'data': F('previsionnel__suivi_appro'),
            'formatter': "'suivi'",
        },
    )
    prev_mes = (
        ComputedSmartField,
        {
            'title': 'Suivi mise en service',
            'data': F('previsionnel__suivi_mes'),
            'formatter': "'suivi'",
        },
    )
    prev_commentaire = (
        ComputedSmartField,
        {
            'title': 'Commentaire exécution',
            'data': F('previsionnel__commentaire_public'),
        },
    )
    prev_interface = (
        ComputedSmartField,
        {
            'title': 'Interfaces',
            'data': F('previsionnel__interface'),
            'format': 'html',
        },
    )
    montant_engage = (
        ComputedSmartField,
        {
            'data': F('previsionnel__montant_engage'),
            'title': _("Montant engagé"),
            'format': 'money',
            'decimal_symbol': ",",
            'thousands_separator': " ",
            'currency_symbol': " €",
            'symbol_is_after': True,
            'precision': 0,
            'max_width': 95,
            'footer_data': "sum",
        },
    )
    montant_liquide = (
        ComputedSmartField,
        {
            'data': F('previsionnel__montant_liquide'),
            'title': _("Montant liquidé"),
            'format': 'money',
            'decimal_symbol': ",",
            'thousands_separator': " ",
            'currency_symbol': " €",
            'symbol_is_after': True,
            'precision': 0,
            'max_width': 95,
            'footer_data': "sum",
        },
    )
    valeur_inventaire = (
        ComputedSmartField,
        {
            'data': F('previsionnel__valeur_inventaire'),
            'title': _("Valeur dans l'inventaire"),
            'format': 'money',
            'decimal_symbol': ",",
            'thousands_separator': " ",
            'currency_symbol': " €",
            'symbol_is_after': True,
            'precision': 0,
            'max_width': 95,
            'footer_data': "sum",
        },
    )

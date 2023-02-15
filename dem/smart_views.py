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
import datetime
import json
import logging
from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import (
    Case,
    CharField,
    DecimalField,
    ExpressionWrapper,
    F,
    OuterRef,
    Q,
    TextField,
    Value,
    When,
)
from django.db.models.functions import Cast, Coalesce, Concat
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext as _

from common import config
from common.db_utils import StringAgg, class_roles_expression, user_choices, user_lookup
from common.models import Discipline, Programme, Uf, UserUfRole
from dem.apps import DRACHAR_DELAI_DEMANDE_TERMINEE
from dem.models import Arbitrage, Campagne, Demande, NATURE_CHOICES
from dem.utils import roles_demandes_possibles, user_campagnes
from document.smart_fields import DocumentsSmartField
from document.views import all_documents_json_partial
from smart_view.smart_fields import ComputedSmartField, ConditionnalSmartField, SmartField, ToolsSmartField
from smart_view.smart_table import SmartTable
from smart_view.smart_view import SmartView

logger = logging.getLogger(__name__)


def debug(*args):
    logger.debug(" ".join(map(str, args)))


class CampagneSmartView(SmartView):
    class Meta:
        model = Campagne
        permissions = {
            'create': ('ADM', 'MAN'),
            'write': {
                None: {
                    'ADM': {
                        'code': True,
                        'nom': True,
                        'natures': True,
                        'description': True,
                        'message': True,
                        'debut_recensement': True,
                        'fin_recensement': True,
                        'discipline': True,
                        'dispatcher': True,
                    },
                },
                'EDITABLE': {
                    'ADM': {
                        'code': True,
                        'nom': True,
                        'natures': True,
                        'description': True,
                        'message': True,
                        'debut_recensement': True,
                        'fin_recensement': True,
                        'discipline': True,
                        'dispatcher': True,
                    },
                },
            },
            'delete': {
                'EDITABLE': ('ADM',),
            },
        }
        columns = (
            'id',
            'code',
            'nom',
            'natures',
            'description',
            'message',
            'debut_recensement',
            'fin_recensement',
            'discipline',
            'dispatcher',
            'instance_roles',
            'state_code',
            'tools',
        )
        settings = {
            'id': {
                'special': 'id',
                'hidden': True,
            },
            'dispatcher': {
                'editor': 'autocomplete',
                'lookup': user_lookup,
                'choices': user_choices,
            },
            'debut_recensement': {
                'editor': 'dateEditor',
            },
        }
        form_layout = """
        #
            # Campagne
                <code>  <nom--+-->
                <description-+--+->
                <message-+-+-->
                <discipline> <natures>  <dispatcher>
                <debut_recensement> <fin_recensement>
        """
        user_filters = {
            'discipline': {'type': 'select'},
        }
        menu_left = ({'label': 'Ajouter une campagne', 'url_name': 'common:calendrier-create'},)

    state_code = (
        ComputedSmartField,
        {
            'special': 'state',
            'data': lambda params: ExpressionWrapper(Value('EDITABLE'), output_field=TextField()),
        },
    )

    instance_roles = (
        ComputedSmartField,
        {
            'special': 'roles',
            'data': class_roles_expression(Campagne),
        },
    )

    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'common:calendrier-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir la campagne"),
                },
                {
                    'tool': 'copy',
                    'url_name': 'common:calendrier-copy',
                    'url_args': ('${id}',),
                    'tooltip': _("Copier la campagne"),
                },
                {
                    'tool': 'delete',
                    'url_name': 'common:calendrier-ask-delete',
                    'url_args': ('${id}',),
                    'tooltip': _("Supprimer la campagne"),
                },
            ],
        },
    )


# Table complète, avec tous les champs et les formats adaptés à un affichage en tableau
class DemandeSmartView(SmartView):
    class Meta:
        # this is intentionally NOT a method (but only a function)
        def uf_demandes_possibles(view_params: dict):  # noqa
            api_filter = Q()
            load = view_params.get('load', [''])[0]
            if load:
                api_filter = Q(pk=load)
            else:
                # Liste des rôles pour lesquels je peux faire une demande sur une UF
                keyword = view_params.get('keyword', '')
                if keyword:
                    api_filter = Q(nom_complet__icontains=keyword)
            # if keyword:
            #     print('Looking for {}'.format(repr(keyword)))
            tmp_scope = roles_demandes_possibles(view_params['user'])
            return (
                Uf.objects.filter(
                    Q(pk__in=tmp_scope.values('uf'))
                    | Q(service__in=tmp_scope.values('service'))
                    | Q(centre_responsabilite__in=tmp_scope.values('centre_responsabilite'))
                    | Q(pole__in=tmp_scope.values('pole'))
                    | Q(site__in=tmp_scope.values('site'))
                    | Q(etablissement__in=tmp_scope.values('etablissement')),
                    cloture__isnull=True,
                )
                # .filter(nom__icontains=keyword)
                .annotate(
                    str_pk=Cast('pk', output_field=CharField()),
                    nom_complet=Concat('code', Value(' - '), 'nom'),
                )
                .filter(api_filter)
                .values_list('str_pk', 'nom_complet')
            )

        # Ceci va entraîner la création d'une colonne par champ du modêle, avec des 'settings' par défaut,
        #  issus du modèle
        model = Demande

        # Gestion des droits d'accès :
        #    C'est un arbre de dict. A terme, cela pourrait sûrement être mis dans le modèle car c'est lié aux données et pas à
        #  leur présentation. Il faudrait alors traduire les droits sur les champs du modèle en droits sur les champs de la
        #  smartview (ce qui est assez facile et même souvent direct car ils sont identiques...)
        #    Ou alors, mettre ces droits (avec tous les autres sur tous les modèles) dans une "politique" à côté ?...
        # Niveaux :
        #  - action ('create', 'delete' et 'write' seulement pour l'instant)
        #   - état (la valeur de la colonne de type StateSmartField)
        #    - rôle (un des élements de la colonne de type RoleSmartField)
        #     - champs concerné : si présent et True => éditable. A terme on pourrait imaginer d'autres valeurs (comme une liste de
        #                          choix en fonction du rôle et/ou de l'état ==> workflow !)
        permissions = {
            "create": config.settings.DEM_DEMANDE_CREATION_ROLES,
            'read': {
                'DIR': {},
                'CHP': {},
                'ACHP': {},
                'CSP': {},
                'CAP': {},
                'AMAR': {},
                'RUN': {},
                'DRP': {},
                'CHS': {},
                'CAD': {},
                'RMA': {},
                'DIS': {},
                'EXP': {},
                'ARB': {},
                'TECH': {},
                'P-EXP': {},
            },
            "delete": {  # 3 niveaux (en tout) pour l'action 'delete' ; la notion de champ n'a pas de sens ici
                None: ('OWN',),  # Seul le demandeur peut supprimer sa demande
                "NOUVELLE": (  # Seules les demandes non encore validées peuvent être supprimées
                    'OWN',
                ),  # Seul le demandeur peut supprimer sa demande
                'TVX_NEW': (  # Seules les demandes non encore traitées peuvent être supprimées
                    'OWN',
                ),  # Seul le demandeur peut supprimer sa demande
            },
            "write": {
                None: {  # L'Etat 'None' correspond à un enregistrement en cours de création
                    'ADM': {
                        'state_code': True,
                        'calendrier': True,
                        'nature': True,
                        "discipline_dmd": True,
                        "redacteur": True,
                        "referent": True,
                        "uf": True,
                        "priorite": True,
                        "cause": True,
                        'libelle': True,
                        'tvx_batiment': True,
                        'tvx_etage': True,
                        'localisation': True,
                        'description': True,
                        'nom_projet': True,
                        'contact': True,
                        'dect_contact': True,
                        'date_premiere_demande': True,
                        'materiel_existant': True,
                        'it_caracteristiques_minimales': True,
                        'it_a_installer': True,
                        'consommables_eventuels': True,
                        "impact_travaux": True,
                        "impact_informatique": True,
                        'quantite': True,
                        'prix_unitaire': True,
                        'montant': True,
                        'tmp_int_year': True,
                        'tmp_int_remain': True,
                        'arg_interet_medical': True,
                        'arg_commentaire_im': True,
                        'arg_oblig_reglementaire': True,
                        'arg_commentaire_or': True,
                        'arg_recommandations': True,
                        'arg_commentaire_r': True,
                        'arg_projet_chu_pole': True,
                        'arg_commentaire_pcp': True,
                        'arg_confort_patient': True,
                        'arg_commentaire_cp': True,
                        'arg_confort_perso_ergo': True,
                        'arg_commentaire_pe': True,
                        'arg_notoriete': True,
                        'arg_commentaire_n': True,
                        'arg_innovation_recherche': True,
                        'arg_commentaire_ir': True,
                        'arg_gain_financier': True,
                        'arg_commentaire_gf': True,
                        'arg_mutualisation': True,
                        'arg_commentaire_m': True,
                        'tvx_contrainte_alib': True,
                        'tvx_contrainte_autre': True,
                        'tvx_contrainte_lib': True,
                        'tvx_contrainte_lar': True,
                        'tvx_contrainte': True,
                        'tvx_priorite': True,
                        'tvx_arg_normes': True,
                        'tvx_arg_normes_comment': True,
                        'tvx_arg_reorg': True,
                        'tvx_arg_reorg_comment': True,
                        'tvx_arg_devact': True,
                        'tvx_arg_devact_comment': True,
                        'tvx_arg_eqpt': True,
                        'tvx_arg_eqpt_comment': True,
                        'tvx_arg_qvt': True,
                        'tvx_arg_qvt_comment': True,
                        'tvx_arg_vetustes': True,
                        'tvx_arg_vetustes_comment': True,
                        'tvx_arg_securite': True,
                        'tvx_arg_securite_comment': True,
                        "autre_argumentaire": True,
                        'workflow_alert': True,
                    },
                    'CAP': {
                        'state_code': True,
                        'calendrier': True,
                        'nature': True,
                        "discipline_dmd": True,
                        "redacteur": True,
                        "referent": True,
                        "uf": True,
                        "priorite": True,
                        "cause": True,
                        "libelle": True,
                        'tvx_batiment': True,
                        'tvx_etage': True,
                        "localisation": True,
                        "description": True,
                        "nom_projet": True,
                        "contact": True,
                        "dect_contact": True,
                        "date_premiere_demande": True,
                        "materiel_existant": True,
                        'it_caracteristiques_minimales': True,
                        'it_a_installer': True,
                        'consommables_eventuels': True,
                        "impact_travaux": True,
                        "impact_informatique": True,
                        "quantite": True,
                        "prix_unitaire": True,
                        'montant': True,
                        'tmp_int_year': True,
                        'tmp_int_remain': True,
                        'arg_interet_medical': True,
                        'arg_commentaire_im': True,
                        'arg_oblig_reglementaire': True,
                        'arg_commentaire_or': True,
                        'arg_recommandations': True,
                        'arg_commentaire_r': True,
                        'arg_projet_chu_pole': True,
                        'arg_commentaire_pcp': True,
                        'arg_confort_patient': True,
                        'arg_commentaire_cp': True,
                        'arg_confort_perso_ergo': True,
                        'arg_commentaire_pe': True,
                        'arg_notoriete': True,
                        'arg_commentaire_n': True,
                        'arg_innovation_recherche': True,
                        'arg_commentaire_ir': True,
                        'arg_gain_financier': True,
                        'arg_commentaire_gf': True,
                        'arg_mutualisation': True,
                        'arg_commentaire_m': True,
                        'tvx_contrainte_alib': True,
                        'tvx_contrainte_autre': True,
                        'tvx_contrainte_lib': True,
                        'tvx_contrainte_lar': True,
                        'tvx_contrainte': True,
                        'tvx_priorite': True,
                        'tvx_arg_normes': True,
                        'tvx_arg_normes_comment': True,
                        'tvx_arg_reorg': True,
                        'tvx_arg_reorg_comment': True,
                        'tvx_arg_devact': True,
                        'tvx_arg_devact_comment': True,
                        'tvx_arg_eqpt': True,
                        'tvx_arg_eqpt_comment': True,
                        'tvx_arg_qvt': True,
                        'tvx_arg_qvt_comment': True,
                        'tvx_arg_vetustes': True,
                        'tvx_arg_vetustes_comment': True,
                        'tvx_arg_securite': True,
                        'tvx_arg_securite_comment': True,
                        "autre_argumentaire": True,
                    },
                    'AMAR': {
                        'state_code': True,
                        'calendrier': True,
                        'nature': True,
                        "discipline_dmd": True,
                        "redacteur": True,
                        "referent": True,
                        "uf": True,
                        "priorite": True,
                        "cause": True,
                        "libelle": True,
                        'tvx_batiment': True,
                        'tvx_etage': True,
                        "localisation": True,
                        "description": True,
                        "nom_projet": True,
                        "contact": True,
                        "dect_contact": True,
                        "date_premiere_demande": True,
                        "materiel_existant": True,
                        'consommables_eventuels': True,
                        'it_caracteristiques_minimales': True,
                        'it_a_installer': True,
                        "impact_travaux": True,
                        "impact_informatique": True,
                        "quantite": True,
                        "prix_unitaire": True,
                        'montant': True,
                        'tmp_int_year': True,
                        'tmp_int_remain': True,
                        'arg_interet_medical': True,
                        'arg_commentaire_im': True,
                        'arg_oblig_reglementaire': True,
                        'arg_commentaire_or': True,
                        'arg_recommandations': True,
                        'arg_commentaire_r': True,
                        'arg_projet_chu_pole': True,
                        'arg_commentaire_pcp': True,
                        'arg_confort_patient': True,
                        'arg_commentaire_cp': True,
                        'arg_confort_perso_ergo': True,
                        'arg_commentaire_pe': True,
                        'arg_notoriete': True,
                        'arg_commentaire_n': True,
                        'arg_innovation_recherche': True,
                        'arg_commentaire_ir': True,
                        'arg_gain_financier': True,
                        'arg_commentaire_gf': True,
                        'arg_mutualisation': True,
                        'arg_commentaire_m': True,
                        'tvx_contrainte_alib': True,
                        'tvx_contrainte_autre': True,
                        'tvx_contrainte_lib': True,
                        'tvx_contrainte_lar': True,
                        'tvx_contrainte': True,
                        'tvx_priorite': True,
                        'tvx_arg_normes': True,
                        'tvx_arg_normes_comment': True,
                        'tvx_arg_reorg': True,
                        'tvx_arg_reorg_comment': True,
                        'tvx_arg_devact': True,
                        'tvx_arg_devact_comment': True,
                        'tvx_arg_eqpt': True,
                        'tvx_arg_eqpt_comment': True,
                        'tvx_arg_qvt': True,
                        'tvx_arg_qvt_comment': True,
                        'tvx_arg_vetustes': True,
                        'tvx_arg_vetustes_comment': True,
                        'tvx_arg_securite': True,
                        'tvx_arg_securite_comment': True,
                        'autre_argumentaire': True,
                    },
                    'RMA': {
                        'state_code': True,
                        'calendrier': True,
                        'nature': True,
                        'discipline_dmd': True,
                        'redacteur': True,
                        'referent': True,
                        'uf': True,
                        'priorite': True,
                        'cause': True,
                        'libelle': True,
                        'localisation': True,
                        'description': True,
                        'nom_projet': True,
                        'contact': True,
                        'dect_contact': True,
                        'date_premiere_demande': True,
                        'materiel_existant': True,
                        'it_caracteristiques_minimales': True,
                        'it_a_installer': True,
                        'consommables_eventuels': True,
                        'impact_travaux': True,
                        'impact_informatique': True,
                        'quantite': True,
                        'prix_unitaire': True,
                        'montant': True,
                        'tmp_int_year': True,
                        'tmp_int_remain': True,
                        'arg_interet_medical': True,
                        'arg_commentaire_im': True,
                        'arg_oblig_reglementaire': True,
                        'arg_commentaire_or': True,
                        'arg_recommandations': True,
                        'arg_commentaire_r': True,
                        'arg_projet_chu_pole': True,
                        'arg_commentaire_pcp': True,
                        'arg_confort_patient': True,
                        'arg_commentaire_cp': True,
                        'arg_confort_perso_ergo': True,
                        'arg_commentaire_pe': True,
                        'arg_notoriete': True,
                        'arg_commentaire_n': True,
                        'arg_innovation_recherche': True,
                        'arg_commentaire_ir': True,
                        'arg_gain_financier': True,
                        'arg_commentaire_gf': True,
                        'arg_mutualisation': True,
                        'arg_commentaire_m': True,
                        'autre_argumentaire': True,
                    },
                    'CAD': {
                        'state_code': True,
                        'calendrier': True,
                        'nature': True,
                        'discipline_dmd': True,
                        'redacteur': True,
                        'referent': True,
                        'uf': True,
                        'priorite': True,
                        'cause': True,
                        'libelle': True,
                        'tvx_batiment': True,
                        'tvx_etage': True,
                        'tvx_priorite': True,
                        'tvx_contrainte_alib': True,
                        'tvx_contrainte_autre': True,
                        'tvx_contrainte_lib': True,
                        'tvx_contrainte_lar': True,
                        'tvx_contrainte': True,
                        'localisation': True,
                        'description': True,
                        'nom_projet': True,
                        'contact': True,
                        'dect_contact': True,
                        'date_premiere_demande': True,
                        'materiel_existant': True,
                        'it_caracteristiques_minimales': True,
                        'it_a_installer': True,
                        'consommables_eventuels': True,
                        'impact_travaux': True,
                        'impact_informatique': True,
                        'quantite': True,
                        'prix_unitaire': True,
                        'montant': True,
                        'tmp_int_year': True,
                        'tmp_int_remain': True,
                        'arg_interet_medical': True,
                        'arg_commentaire_im': True,
                        'arg_oblig_reglementaire': True,
                        'arg_commentaire_or': True,
                        'arg_recommandations': True,
                        'arg_commentaire_r': True,
                        'arg_projet_chu_pole': True,
                        'arg_commentaire_pcp': True,
                        'arg_confort_patient': True,
                        'arg_commentaire_cp': True,
                        'arg_confort_perso_ergo': True,
                        'arg_commentaire_pe': True,
                        'arg_notoriete': True,
                        'arg_commentaire_n': True,
                        'arg_innovation_recherche': True,
                        'arg_commentaire_ir': True,
                        'arg_gain_financier': True,
                        'arg_commentaire_gf': True,
                        'arg_mutualisation': True,
                        'arg_commentaire_m': True,
                        'tvx_arg_normes': True,
                        'tvx_arg_normes_comment': True,
                        'tvx_arg_reorg': True,
                        'tvx_arg_reorg_comment': True,
                        'tvx_arg_devact': True,
                        'tvx_arg_devact_comment': True,
                        'tvx_arg_eqpt': True,
                        'tvx_arg_eqpt_comment': True,
                        'tvx_arg_qvt': True,
                        'tvx_arg_qvt_comment': True,
                        'tvx_arg_vetustes': True,
                        'tvx_arg_vetustes_comment': True,
                        'tvx_arg_securite': True,
                        'tvx_arg_securite_comment': True,
                        'autre_argumentaire': True,
                    },
                    'CSP': {
                        'state_code': True,
                        'calendrier': True,
                        'nature': True,
                        'discipline_dmd': True,
                        'redacteur': True,
                        'referent': True,
                        'uf': True,
                        'priorite': True,
                        'cause': True,
                        'libelle': True,
                        'tvx_batiment': True,
                        'tvx_etage': True,
                        'localisation': True,
                        'description': True,
                        "nom_projet": True,
                        'contact': True,
                        'dect_contact': True,
                        'date_premiere_demande': True,
                        'materiel_existant': True,
                        'consommables_eventuels': True,
                        'it_caracteristiques_minimales': True,
                        'it_a_installer': True,
                        'impact_travaux': True,
                        'impact_informatique': True,
                        'quantite': True,
                        'prix_unitaire': True,
                        'montant': True,
                        'avis_cadre_sup': True,
                        'commentaire_cadre_sup': True,
                        'tmp_int_year': True,
                        'tmp_int_remain': True,
                        'arg_interet_medical': True,
                        'arg_commentaire_im': True,
                        'arg_oblig_reglementaire': True,
                        'arg_commentaire_or': True,
                        'arg_recommandations': True,
                        'arg_commentaire_r': True,
                        'arg_projet_chu_pole': True,
                        'arg_commentaire_pcp': True,
                        'arg_confort_patient': True,
                        'arg_commentaire_cp': True,
                        'arg_confort_perso_ergo': True,
                        'arg_commentaire_pe': True,
                        'arg_notoriete': True,
                        'arg_commentaire_n': True,
                        'arg_innovation_recherche': True,
                        'arg_commentaire_ir': True,
                        'arg_gain_financier': True,
                        'arg_commentaire_gf': True,
                        'arg_mutualisation': True,
                        'arg_commentaire_m': True,
                        'tvx_contrainte_alib': True,
                        'tvx_contrainte_autre': True,
                        'tvx_contrainte_lib': True,
                        'tvx_contrainte_lar': True,
                        'tvx_contrainte': True,
                        'tvx_priorite': True,
                        'tvx_arg_normes': True,
                        'tvx_arg_normes_comment': True,
                        'tvx_arg_reorg': True,
                        'tvx_arg_reorg_comment': True,
                        'tvx_arg_devact': True,
                        'tvx_arg_devact_comment': True,
                        'tvx_arg_eqpt': True,
                        'tvx_arg_eqpt_comment': True,
                        'tvx_arg_qvt': True,
                        'tvx_arg_qvt_comment': True,
                        'tvx_arg_vetustes': True,
                        'tvx_arg_vetustes_comment': True,
                        'tvx_arg_securite': True,
                        'tvx_arg_securite_comment': True,
                        "autre_argumentaire": True,
                    },
                    'CHP': {
                        'state_code': True,
                        'calendrier': True,
                        'nature': True,
                        "discipline_dmd": True,
                        "redacteur": True,
                        "referent": True,
                        "uf": True,
                        "priorite": True,
                        "cause": True,
                        "libelle": True,
                        'tvx_batiment': True,
                        'tvx_etage': True,
                        "localisation": True,
                        "description": True,
                        "nom_projet": True,
                        "contact": True,
                        "dect_contact": True,
                        "date_premiere_demande": True,
                        "materiel_existant": True,
                        'it_caracteristiques_minimales': True,
                        'it_a_installer': True,
                        'consommables_eventuels': True,
                        "impact_travaux": True,
                        "impact_informatique": True,
                        "quantite": True,
                        "prix_unitaire": True,
                        'montant': True,
                        'tmp_int_year': True,
                        'tmp_int_remain': True,
                        'arg_interet_medical': True,
                        'arg_commentaire_im': True,
                        'arg_oblig_reglementaire': True,
                        'arg_commentaire_or': True,
                        'arg_recommandations': True,
                        'arg_commentaire_r': True,
                        'arg_projet_chu_pole': True,
                        'arg_commentaire_pcp': True,
                        'arg_confort_patient': True,
                        'arg_commentaire_cp': True,
                        'arg_confort_perso_ergo': True,
                        'arg_commentaire_pe': True,
                        'arg_notoriete': True,
                        'arg_commentaire_n': True,
                        'arg_innovation_recherche': True,
                        'arg_commentaire_ir': True,
                        'arg_gain_financier': True,
                        'arg_commentaire_gf': True,
                        'arg_mutualisation': True,
                        'arg_commentaire_m': True,
                        'tvx_contrainte_alib': True,
                        'tvx_contrainte_autre': True,
                        'tvx_contrainte_lib': True,
                        'tvx_contrainte_lar': True,
                        'tvx_contrainte': True,
                        'tvx_priorite': True,
                        'tvx_arg_normes': True,
                        'tvx_arg_normes_comment': True,
                        'tvx_arg_reorg': True,
                        'tvx_arg_reorg_comment': True,
                        'tvx_arg_devact': True,
                        'tvx_arg_devact_comment': True,
                        'tvx_arg_eqpt': True,
                        'tvx_arg_eqpt_comment': True,
                        'tvx_arg_qvt': True,
                        'tvx_arg_qvt_comment': True,
                        'tvx_arg_vetustes': True,
                        'tvx_arg_vetustes_comment': True,
                        'tvx_arg_securite': True,
                        'tvx_arg_securite_comment': True,
                        "autre_argumentaire": True,
                    },
                    'DIR': {
                        'state_code': True,
                        'calendrier': True,
                        'nature': True,
                        "discipline_dmd": True,
                        "redacteur": True,
                        "referent": True,
                        "uf": True,
                        "priorite": True,
                        "cause": True,
                        "libelle": True,
                        'tvx_batiment': True,
                        'tvx_etage': True,
                        "localisation": True,
                        "description": True,
                        "nom_projet": True,
                        "contact": True,
                        "dect_contact": True,
                        "date_premiere_demande": True,
                        "materiel_existant": True,
                        'it_caracteristiques_minimales': True,
                        'it_a_installer': True,
                        'consommables_eventuels': True,
                        "impact_travaux": True,
                        "impact_informatique": True,
                        "quantite": True,
                        "prix_unitaire": True,
                        'montant': True,
                        'arg_interet_medical': True,
                        'arg_commentaire_im': True,
                        'arg_oblig_reglementaire': True,
                        'arg_commentaire_or': True,
                        'arg_recommandations': True,
                        'arg_commentaire_r': True,
                        'arg_projet_chu_pole': True,
                        'arg_commentaire_pcp': True,
                        'arg_confort_patient': True,
                        'arg_commentaire_cp': True,
                        'arg_confort_perso_ergo': True,
                        'arg_commentaire_pe': True,
                        'arg_notoriete': True,
                        'arg_commentaire_n': True,
                        'arg_innovation_recherche': True,
                        'arg_commentaire_ir': True,
                        'arg_gain_financier': True,
                        'arg_commentaire_gf': True,
                        'arg_mutualisation': True,
                        'arg_commentaire_m': True,
                        'tvx_contrainte_alib': True,
                        'tvx_contrainte_autre': True,
                        'tvx_contrainte_lib': True,
                        'tvx_contrainte_lar': True,
                        'tvx_contrainte': True,
                        'tvx_priorite': True,
                        'tvx_arg_normes': True,
                        'tvx_arg_normes_comment': True,
                        'tvx_arg_reorg': True,
                        'tvx_arg_reorg_comment': True,
                        'tvx_arg_devact': True,
                        'tvx_arg_devact_comment': True,
                        'tvx_arg_eqpt': True,
                        'tvx_arg_eqpt_comment': True,
                        'tvx_arg_qvt': True,
                        'tvx_arg_qvt_comment': True,
                        'tvx_arg_vetustes': True,
                        'tvx_arg_vetustes_comment': True,
                        'tvx_arg_securite': True,
                        'tvx_arg_securite_comment': True,
                        "autre_argumentaire": True,
                    },
                    'EXP': {
                        'state_code': True,
                        'calendrier': True,
                        'nature': True,
                        "discipline_dmd": True,
                        "redacteur": True,
                        "referent": True,
                        "uf": True,
                        "priorite": True,
                        "cause": True,
                        "libelle": True,
                        'tvx_batiment': True,
                        'tvx_etage': True,
                        "localisation": True,
                        "description": True,
                        "nom_projet": True,
                        "contact": True,
                        "dect_contact": True,
                        "date_premiere_demande": True,
                        "materiel_existant": True,
                        'it_caracteristiques_minimales': True,
                        'it_a_installer': True,
                        'consommables_eventuels': True,
                        "impact_travaux": True,
                        "impact_informatique": True,
                        "quantite": True,
                        "prix_unitaire": True,
                        'montant': True,
                        'tmp_int_year': True,
                        'tmp_int_remain': True,
                        'arg_interet_medical': True,
                        'arg_commentaire_im': True,
                        'arg_oblig_reglementaire': True,
                        'arg_commentaire_or': True,
                        'arg_recommandations': True,
                        'arg_commentaire_r': True,
                        'arg_projet_chu_pole': True,
                        'arg_commentaire_pcp': True,
                        'arg_confort_patient': True,
                        'arg_commentaire_cp': True,
                        'arg_confort_perso_ergo': True,
                        'arg_commentaire_pe': True,
                        'arg_notoriete': True,
                        'arg_commentaire_n': True,
                        'arg_innovation_recherche': True,
                        'arg_commentaire_ir': True,
                        'arg_gain_financier': True,
                        'arg_commentaire_gf': True,
                        'arg_mutualisation': True,
                        'arg_commentaire_m': True,
                        'tvx_contrainte_alib': True,
                        'tvx_contrainte_autre': True,
                        'tvx_contrainte_lib': True,
                        'tvx_contrainte_lar': True,
                        'tvx_contrainte': True,
                        'tvx_priorite': True,
                        'tvx_arg_normes': True,
                        'tvx_arg_normes_comment': True,
                        'tvx_arg_reorg': True,
                        'tvx_arg_reorg_comment': True,
                        'tvx_arg_devact': True,
                        'tvx_arg_devact_comment': True,
                        'tvx_arg_eqpt': True,
                        'tvx_arg_eqpt_comment': True,
                        'tvx_arg_qvt': True,
                        'tvx_arg_qvt_comment': True,
                        'tvx_arg_vetustes': True,
                        'tvx_arg_vetustes_comment': True,
                        'tvx_arg_securite': True,
                        'tvx_arg_securite_comment': True,
                        "autre_argumentaire": True,
                        'montant_unitaire_expert_metier': True,
                        'montant_total_expert_metier': False,
                        'commentaire_biomed': True,
                        'avis_biomed': True,
                        'workflow_alert': True,
                    },
                    'CHS': {
                        'state_code': True,
                        'calendrier': True,
                        'nature': True,
                        'discipline_dmd': True,
                        'redacteur': True,
                        'referent': True,
                        'uf': True,
                        'priorite': True,
                        'cause': True,
                        'libelle': True,
                        'localisation': True,
                        'description': True,
                        'nom_projet': True,
                        'contact': True,
                        'dect_contact': True,
                        'date_premiere_demande': True,
                        'tvx_batiment': True,
                        'tvx_etage': True,
                        'materiel_existant': True,
                        'it_caracteristiques_minimales': True,
                        'it_a_installer': True,
                        'consommables_eventuels': True,
                        'impact_travaux': True,
                        'impact_informatique': True,
                        'quantite': True,
                        'prix_unitaire': True,
                        'tmp_int_year': True,
                        'tmp_int_remain': True,
                        'arg_interet_medical': True,
                        'arg_commentaire_im': True,
                        'arg_oblig_reglementaire': True,
                        'arg_commentaire_or': True,
                        'arg_recommandations': True,
                        'arg_commentaire_r': True,
                        'arg_projet_chu_pole': True,
                        'arg_commentaire_pcp': True,
                        'arg_confort_patient': True,
                        'arg_commentaire_cp': True,
                        'arg_confort_perso_ergo': True,
                        'arg_commentaire_pe': True,
                        'arg_notoriete': True,
                        'arg_commentaire_n': True,
                        'arg_innovation_recherche': True,
                        'arg_commentaire_ir': True,
                        'arg_gain_financier': True,
                        'arg_commentaire_gf': True,
                        'arg_mutualisation': True,
                        'arg_commentaire_m': True,
                        "autre_argumentaire": True,
                        'tvx_priorite': True,
                        'tvx_contrainte_alib': True,
                        'tvx_contrainte_autre': True,
                        'tvx_contrainte_lib': True,
                        'tvx_contrainte_lar': True,
                        'tvx_contrainte': True,
                        'tvx_arg_normes': True,
                        'tvx_arg_normes_comment': True,
                        'tvx_arg_reorg': True,
                        'tvx_arg_reorg_comment': True,
                        'tvx_arg_devact': True,
                        'tvx_arg_devact_comment': True,
                        'tvx_arg_eqpt': True,
                        'tvx_arg_eqpt_comment': True,
                        'tvx_arg_qvt': True,
                        'tvx_arg_qvt_comment': True,
                        'tvx_arg_vetustes': True,
                        'tvx_arg_vetustes_comment': True,
                        'tvx_arg_securite': True,
                        'tvx_arg_securite_comment': True,
                    },
                },
                "NOUVELLE": {
                    "OWN": {
                        'state_code': True,
                        "referent": True,
                        "uf": True,
                        "priorite": True,
                        "cause": True,
                        "libelle": True,
                        "nom_projet": True,
                        "contact": True,
                        "dect_contact": True,
                        "date_premiere_demande": True,
                        "materiel_existant": True,
                        'it_caracteristiques_minimales': True,
                        'it_a_installer': True,
                        'tmp_int_year': True,
                        'tmp_int_remain': True,
                        'arg_interet_medical': True,
                        'arg_commentaire_im': True,
                        'arg_oblig_reglementaire': True,
                        'arg_commentaire_or': True,
                        'arg_recommandations': True,
                        'arg_commentaire_r': True,
                        'arg_projet_chu_pole': True,
                        'arg_commentaire_pcp': True,
                        'arg_confort_patient': True,
                        'arg_commentaire_cp': True,
                        'arg_confort_perso_ergo': True,
                        'arg_commentaire_pe': True,
                        'arg_notoriete': True,
                        'arg_commentaire_n': True,
                        'arg_innovation_recherche': True,
                        'arg_commentaire_ir': True,
                        'arg_gain_financier': True,
                        'arg_commentaire_gf': True,
                        'arg_mutualisation': True,
                        'arg_commentaire_m': True,
                        "autre_argumentaire": True,
                        "consommables_eventuel": True,
                        "impact_travaux": True,
                        "impact_informatique": True,
                        "quantite": True,
                        "prix_unitaire": True,
                        'montant': True,
                        "description": True,
                        "localisation": True,
                    },
                    "DIR": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    "CHP": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    "CSP": {
                        'state_code': True,
                        "avis_cadre_sup": True,
                        "commentaire_cadre_sup": True,
                    },
                    'DIS': {
                        'state_code': True,
                        'campagne_redirect': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                        'workflow_alert': True,
                    },
                    'EXP': {
                        'state_code': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'montant_unitaire_expert_metier': True,
                        'montant_total_expert_metier': False,
                        'commentaire_biomed': True,
                        'avis_biomed': True,
                        'workflow_alert': True,
                    },
                    'ARB': {
                        'state_code': True,
                        'workflow_alert': True,
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                },
                "AVFAV_CSP": {
                    "DIR": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    "CHP": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    "CSP": {
                        'state_code': True,
                        "avis_cadre_sup": True,
                        "commentaire_cadre_sup": True,
                    },
                    'DIS': {
                        'state_code': True,
                        'campagne_redirect': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                        'workflow_alert': True,
                    },
                    'EXP': {
                        'state_code': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'montant_unitaire_expert_metier': True,
                        'montant_total_expert_metier': False,
                        'commentaire_biomed': True,
                        'avis_biomed': True,
                        'workflow_alert': True,
                    },
                    'ARB': {
                        'state_code': True,
                        'workflow_alert': True,
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                },
                "AVDEF_CSP": {
                    "DIR": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    "CHP": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    "CSP": {
                        'state_code': True,
                        "avis_cadre_sup": True,
                        "commentaire_cadre_sup": True,
                    },
                    'DIS': {
                        'state_code': True,
                        'campagne_redirect': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                        'workflow_alert': True,
                    },
                    'EXP': {
                        'state_code': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'montant_unitaire_expert_metier': True,
                        'montant_total_expert_metier': False,
                        'commentaire_biomed': True,
                        'avis_biomed': True,
                        'workflow_alert': True,
                    },
                    'ARB': {
                        'state_code': True,
                        'workflow_alert': True,
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                },
                "VALIDE_CP": {
                    "DIR": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    "CHP": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    'DIS': {
                        'state_code': True,
                        'campagne_redirect': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                        'workflow_alert': True,
                    },
                    "ARB": {
                        'state_code': True,
                        'workflow_alert': True,
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                    'EXP': {
                        'state_code': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'montant_unitaire_expert_metier': True,
                        'montant_total_expert_metier': False,
                        'commentaire_biomed': True,
                        'avis_biomed': True,
                        'workflow_alert': True,
                    },
                },
                "NONVAL_CP": {
                    "DIR": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    "CHP": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    'DIS': {
                        'state_code': True,
                        'campagne_redirect': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                        'workflow_alert': True,
                    },
                    'ARB': {
                        'state_code': True,
                        'workflow_alert': True,
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                },
                "NONVAL_CP_DEF": {
                    'DIS': {
                        'state_code': True,
                        'campagne_redirect': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                        'workflow_alert': True,
                    },
                    'ARB': {
                        'state_code': True,
                        'workflow_alert': True,
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                },
                "INSTRUCTION": {
                    "DIR": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    "CHP": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    'DIS': {
                        'state_code': True,
                        'campagne_redirect': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                        'workflow_alert': True,
                    },
                    'ARB': {
                        'state_code': True,
                        'workflow_alert': True,
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                    'EXP': {
                        'state_code': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'montant_unitaire_expert_metier': True,
                        'montant_total_expert_metier': False,
                        'commentaire_biomed': True,
                        'avis_biomed': True,
                        'workflow_alert': True,
                    },
                },
                "INSTR_OK": {
                    "DIR": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    "CHP": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    "ARB": {
                        'state_code': True,
                        'workflow_alert': True,
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                    'DIS': {
                        'state_code': True,
                        'campagne_redirect': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                        'workflow_alert': True,
                    },
                    'EXP': {
                        'state_code': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'montant_unitaire_expert_metier': True,
                        'montant_total_expert_metier': False,
                        'commentaire_biomed': True,
                        'avis_biomed': True,
                        'workflow_alert': True,
                    },
                },
                'ERR_VAL_EXP': {
                    'DIS': {
                        'state_code': True,
                        'campagne_redirect': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                        'workflow_alert': True,
                    },
                    "ARB": {
                        'state_code': True,
                        'workflow_alert': True,
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                    'EXP': {
                        'state_code': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'montant_unitaire_expert_metier': True,
                        'montant_total_expert_metier': False,
                        'commentaire_biomed': True,
                        'avis_biomed': True,
                        'workflow_alert': True,
                    },
                },
                "AVFAV_EXP": {
                    "DIR": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    "CHP": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    'DIS': {
                        'state_code': True,
                        'campagne_redirect': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                        'workflow_alert': True,
                    },
                    "ARB": {
                        'state_code': True,
                        'workflow_alert': True,
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                    'EXP': {
                        'state_code': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'montant_unitaire_expert_metier': True,
                        'montant_total_expert_metier': False,
                        'commentaire_biomed': True,
                        'avis_biomed': True,
                        'workflow_alert': True,
                    },
                },
                "AVDEF_EXP": {
                    "DIR": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    "CHP": {
                        'state_code': True,
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    'DIS': {
                        'state_code': True,
                        'campagne_redirect': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                        'workflow_alert': True,
                    },
                    "ARB": {
                        'state_code': True,
                        'workflow_alert': True,
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                    'EXP': {
                        'state_code': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'montant_unitaire_expert_metier': True,
                        'montant_total_expert_metier': False,
                        'commentaire_biomed': True,
                        'avis_biomed': True,
                        'workflow_alert': True,
                    },
                },
                "VALIDE_ARB": {
                    'DIS': {
                        'state_code': True,
                        'campagne_redirect': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                        'workflow_alert': True,
                    },
                    "ARB": {
                        'state_code': True,
                        'workflow_alert': True,
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                },
                "NONVAL_ARB": {
                    'DIS': {
                        'state_code': True,
                        'campagne_redirect': True,
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                        'workflow_alert': True,
                    },
                    "ARB": {
                        'state_code': True,
                        'workflow_alert': True,
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                },
                "VALIDE_DEF": {
                    "ARB": {
                        'state_code': True,
                        'workflow_alert': True,
                        'gel': True,
                    },
                },
                "NONVAL_DEF": {
                    "ARB": {
                        'state_code': True,
                        'workflow_alert': True,
                        'gel': True,
                    },
                },
                'TVX_NEW': {
                    'ADM': {
                        'programme': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                        'libelle': True,
                        'uf': True,
                        'tvx_batiment': True,
                        'tvx_etage': True,
                        "localisation": True,
                        "description": True,
                        "nom_projet": True,
                        "contact": True,
                        "referent": True,
                        "dect_contact": True,
                        'tvx_contrainte_alib': True,
                        'tvx_contrainte_autre': True,
                        'tvx_contrainte_lib': True,
                        'tvx_contrainte_lar': True,
                        'tvx_contrainte': True,
                        'tvx_priorite': True,
                        'tvx_arg_normes': True,
                        'tvx_arg_normes_comment': True,
                        'tvx_arg_reorg': True,
                        'tvx_arg_reorg_comment': True,
                        'tvx_arg_devact': True,
                        'tvx_arg_devact_comment': True,
                        'tvx_arg_eqpt': True,
                        'tvx_arg_eqpt_comment': True,
                        'tvx_arg_qvt': True,
                        'tvx_arg_qvt_comment': True,
                        'tvx_arg_vetustes': True,
                        'tvx_arg_vetustes_comment': True,
                        'tvx_arg_securite': True,
                        'tvx_arg_securite_comment': True,
                        "autre_argumentaire": True,
                    },
                    'OWN': {
                        'libelle': True,
                        'uf': True,
                        'tvx_batiment': True,
                        'tvx_etage': True,
                        "localisation": True,
                        "description": True,
                        "nom_projet": True,
                        "contact": True,
                        "referent": True,
                        "dect_contact": True,
                        'tvx_contrainte_alib': True,
                        'tvx_contrainte_autre': True,
                        'tvx_contrainte_lib': True,
                        'tvx_contrainte_lar': True,
                        'tvx_contrainte': True,
                        'tvx_priorite': True,
                        'tvx_arg_normes': True,
                        'tvx_arg_normes_comment': True,
                        'tvx_arg_reorg': True,
                        'tvx_arg_reorg_comment': True,
                        'tvx_arg_devact': True,
                        'tvx_arg_devact_comment': True,
                        'tvx_arg_eqpt': True,
                        'tvx_arg_eqpt_comment': True,
                        'tvx_arg_qvt': True,
                        'tvx_arg_qvt_comment': True,
                        'tvx_arg_vetustes': True,
                        'tvx_arg_vetustes_comment': True,
                        'tvx_arg_securite': True,
                        'tvx_arg_securite_comment': True,
                        "autre_argumentaire": True,
                    },
                    'DIS': {
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                    },
                    'ARB': {
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                },
                'TVX_APPROB': {
                    'ADM': {
                        'tvx_eval_devact': True,
                        'tvx_eval_contin': True,
                        'tvx_eval_confort': True,
                        'tvx_eval_securite': True,
                        'tvx_eval_qvt': True,
                        'commentaire_biomed': True,
                        'montant_unitaire_expert_metier': True,
                        'avis_biomed': True,
                        'dispatcher_note': True,
                    },
                    'CHP': {
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    'DIR': {
                        "decision_validateur": True,
                        "decision_soumission": True,
                    },
                    'EXP': {
                        'tvx_eval_devact': True,
                        'tvx_eval_contin': True,
                        'tvx_eval_confort': True,
                        'tvx_eval_securite': True,
                        'tvx_eval_qvt': True,
                        'commentaire_biomed': True,
                        'montant_unitaire_expert_metier': True,
                        'avis_biomed': True,
                    },
                    'DIS': {
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                    },
                    'ARB': {
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                },
                'TVX_ANA': {
                    'ADM': {
                        'tvx_eval_devact': True,
                        'tvx_eval_contin': True,
                        'tvx_eval_confort': True,
                        'tvx_eval_securite': True,
                        'tvx_eval_qvt': True,
                        'commentaire_biomed': True,
                        'montant_unitaire_expert_metier': True,
                        'avis_biomed': True,
                        'dispatcher_note': True,
                    },
                    'EXP': {
                        'tvx_eval_devact': True,
                        'tvx_eval_contin': True,
                        'tvx_eval_confort': True,
                        'tvx_eval_securite': True,
                        'tvx_eval_qvt': True,
                        'commentaire_biomed': True,
                        'montant_unitaire_expert_metier': True,
                        'avis_biomed': True,
                    },
                    'DIS': {
                        'programme': True,
                        'domaine': True,
                        'expert_metier': True,
                        'dispatcher_note': True,
                    },
                    'ARB': {
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                },
                'TVX_ARB': {
                    'ADM': {
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                    'ARB': {
                        "arbitrage_commission": True,
                        "commentaire_provisoire_commission": True,
                        "commentaire_definitif_commission": True,
                        "quantite_validee": True,
                        "enveloppe_allouee": True,
                        'gel': True,
                    },
                    'EXP': {
                        'avis_biomed': True,
                    },
                },
                'TVX_VAL': {
                    'ADM': {
                        'gel': True,
                    },
                    'ARB': {
                        'gel': True,
                    },
                },
                'TVX_NVAL': {
                    'ADM': {
                        'gel': True,
                    },
                    'ARB': {
                        'gel': True,
                    },
                },
            },
        }

        # C'est le nom du champs qui donne le code à afficher à l'utilisateur (par défaut, c'est la clef primaire de la table)
        code_for_user = 'code'
        current_row_manager = True

        # Ici, on peut modifier les réglages des colonnes générées automatiquement
        #  Un 'setting' peut être :
        #    - Une classe (qui sera utilisée pour forcer le type de colonne, tout en gardant un maximum d'attributs
        #    - Un dictionnaire d'arguments qui seront utilisés pour créer la colonne automatiquement
        #       (prioritaire sur les attributs générés automatiquement)
        #    - Un tuple composé d'une classe et d'un dictionnaire. Les deux viennent en priorité sur les arguments automatiques
        #       (mais ceux-ci existent encore)
        settings = {
            'roles': {
                # For debug only
                'title': _("Rôles (debug)"),
                'hidden': not (hasattr(config.settings, 'SMARTVIEW_DEBUG') and config.settings.SMARTVIEW_DEBUG),
            },
            'num_dmd': {
                'special': 'id',
                'max_width': 50,
                'hidden': True,
            },
            'calendrier': {
                'title': 'Campagne de recensement (H)',
                'table.hidden': True,
                'lookup': lambda view_params: [(campagne.pk, campagne.nom) for campagne in Campagne.objects.all()],
                'choices': lambda view_params: [(campagne.pk, campagne.nom) for campagne in user_campagnes(view_params)],
            },
            'campagne_redirect': {
                'title': 'Campagne',
                'format': 'coalesce_choice',
                'fields': ['calendrier'],
                'lookup': lambda view_params: [(campagne.pk, campagne.nom) for campagne in Campagne.objects.all()],
                'choices': lambda view_params: [(campagne.pk, campagne.nom) for campagne in user_campagnes(view_params)]
                + [(campagne.pk, '>> ' + campagne.nom) for campagne in Campagne.objects.filter(programme__isnull=True)],
            },
            'code': {
                'title': _("N°"),
            },
            'contact': {'table.hidden': True},
            'dect_contact': {'table.hidden': True},
            'redacteur': {
                'lookup': user_lookup,
                'choices': lambda view_params: (
                    (
                        view_params['user'].pk,
                        get_user_model()
                        .objects.filter(pk=view_params['user'].pk)
                        .annotate(full_name=Concat('first_name', Value(" "), 'last_name'))
                        .order_by('full_name')
                        .get()
                        .full_name,
                    ),
                ),
                'help_text': _("Le rédacteur est toujours la personne connectée qui rédige la fiche."),
            },
            'date_premiere_demande': {
                'form.title': _("Année de première demande"),
                'format': 'choice',
                'choices': lambda view_params: [(date(y, 1, 1).strftime('%Y-%m-%d'), str(y)) for y in range(2017, now().year + 1)],
                'datetime_format': "%Y",
                'width': 50,
                'default': '2018',
                'form.html.show-if': 'if ((args[0]!=6)&&(args[0]!=17)) {return true;} else {return false;}',
                'form.html.show-depends': ['calendrier'],
            },
            'state_code': {
                'title': _("Etat (debug)"),
                'hidden': not (hasattr(config.settings, 'SMARTVIEW_DEBUG') and config.settings.SMARTVIEW_DEBUG),
                'special': 'state',
                'depends': [
                    'avis_cadre_sup',
                    'decision_validateur',
                    'expert_metier',
                    'avis_biomed',
                    # "montant",
                    'quantite',
                    'prix_unitaire',
                    'montant_unitaire_expert_metier',
                    # "montant_total_expert_metier",
                    'arbitrage_commission',
                    'gel',
                ],
            },
            'quantite': {
                'table.title': _("Qté"),
                'form.title': _("Quantité"),
                'min_width': 20,
                'width_grow': 0,
                'max_width': 40,
                'xlsx.title': _("Quantité"),
            },
            'uf': {
                "title": _("Unité Fonctionnelle"),
                'help_text': _("Commencez à saisir un code ou un nom et choisissez l'UF dans la liste proposée."),
                'width': 100,
                'lookup': lambda view_params: Uf.objects.values_list('pk', 'nom'),
                'choices': uf_demandes_possibles,
                'autocomplete': True,
                'table.hidden': True,
            },
            'priorite': {
                'hoz_align': 'center',
                'max_width': 80,
                'width': 80,
                'form.html.show-if': 'if ((args[0]!=6)&&(args[0]!=17)) {return true;} else {return false;}',
                'form.html.show-depends': ['calendrier'],
            },
            'nom_projet': {
                'format': 'string',
                'width': 250,
            },
            'libelle': {
                'form.title': _("Matériel demandé"),
                'format': 'string',
                'footer_data': 'count',
                'width': 250,
            },
            'description': {
                'format': 'text',
                'width': 250,
            },
            'referent': {
                'format': 'string',
                'width': 150,
                'initial': lambda view_params: view_params['user'].first_name + " " + view_params['user'].last_name,
            },
            'cause': {
                'hoz_align': 'center',
                'width': 110,
                'form.html.show-if': "return args[0].includes('EQ');",
                'form.show-depends': ['nature'],
            },
            'materiel_existant': {
                'hoz_align': 'center',
                'width': 110,
                'form.html.show-if': "return (args[0].includes('EQ') &&"
                " (args[1].includes('RE') || args[1].includes('EV') || args[1].includes('RA')));",
                'form.show-depends': ['nature', 'cause'],
            },
            'tmp_int_year': {
                'format': 'choice',
                'choices': lambda view_params: [(None, 'Sans objet')]
                + [(y, str(y)) for y in range(view_params['now'].year - 3, view_params['now'].year)],
                'table.hidden': True,
                'default': lambda view_params: view_params['now'].year - 2,
            },
            'tmp_int_remain': (
                SmartField,
                {
                    'title': _("Montant restant de l'enveloppe d'intéressement"),
                    'help_text': _(
                        "Saisissez le montant restant de l'enveloppe d'intéressement APRES " "la déduction de cette demande."
                    ),
                    'format': 'money',
                    'decimal_symbol': ",",
                    'thousands_separator': " ",
                    'currency_symbol': " €",
                    'symbol_is_after': True,
                    'precision': 0,
                    'max_width': 100,
                    'table.hidden': True,
                },
            ),
            'arg_interet_medical': {
                'table.hidden': True,
            },
            'arg_commentaire_im': {
                'show-if': 'arg_interet_medical',
                'table.hidden': True,
            },
            'arg_oblig_reglementaire': {
                'table.hidden': True,
            },
            'arg_commentaire_or': {
                'show-if': 'arg_oblig_reglementaire',
                'table.hidden': True,
            },
            'arg_recommandations': {
                'table.hidden': True,
            },
            'arg_commentaire_r': {
                'show-if': 'arg_recommandations',
                'table.hidden': True,
            },
            'arg_projet_chu_pole': {
                'table.hidden': True,
            },
            'arg_commentaire_pcp': {
                'show-if': 'arg_projet_chu_pole',
                'table.hidden': True,
            },
            'arg_confort_patient': {
                'table.hidden': True,
            },
            'arg_commentaire_cp': {
                'show-if': 'arg_confort_patient',
                'table.hidden': True,
            },
            'arg_confort_perso_ergo': {
                'table.hidden': True,
            },
            'arg_commentaire_pe': {
                'show-if': 'arg_confort_perso_ergo',
                'table.hidden': True,
            },
            'arg_notoriete': {
                'table.hidden': True,
            },
            'arg_commentaire_n': {
                'show-if': 'arg_notoriete',
                'table.hidden': True,
            },
            'arg_innovation_recherche': {
                'table.hidden': True,
            },
            'arg_commentaire_ir': {
                'show-if': 'arg_innovation_recherche',
                'table.hidden': True,
            },
            'arg_gain_financier': {
                'table.hidden': True,
            },
            'arg_commentaire_gf': {
                'show-if': 'arg_gain_financier',
                'table.hidden': True,
            },
            'arg_mutualisation': {
                'table.hidden': True,
            },
            'arg_commentaire_m': {
                'show-if': 'arg_mutualisation',
                'table.hidden': True,
            },
            'autre_argumentaire': {
                'table.hidden': True,
                'format': 'text',
            },
            'prix_unitaire': (
                SmartField,
                {
                    'title': _("Prix unitaire (TTC)"),
                    'help_text': _(
                        "Saisissez le prix unitaire en euros TTC de l'objet de votre demande, si vous le connaissez. "
                        "Si vous savez qu'un équipement ou logiciel identique existe déjà dans l'établissement, "
                        "il est inutile de remplir ce champ : L'expert en charge de l'analyse de la demande le fera."
                    ),
                    'format': 'money',
                    'decimal_symbol': ",",
                    'thousands_separator': " ",
                    'currency_symbol': " €",
                    'symbol_is_after': True,
                    'precision': 0,
                    'max_width': 100,
                },
            ),
            'it_cout_formation': (
                SmartField,
                {
                    'format': 'money',
                    'decimal_symbol': ",",
                    'thousands_separator': " ",
                    'currency_symbol': " €",
                    'symbol_is_after': True,
                    'precision': 0,
                    'max_width': 100,
                },
            ),
            # "montant": {
            #     "format": "money",
            #     "decimal_symbol": ",",
            #     "thousands_separator": " ",
            #     "currency_symbol": " €",
            #     "symbol_is_after": True,
            #     "precision": 0,
            #     "max_width": 110,
            #     "footer_data": "sum",
            # },
            'impact_travaux': {
                'width': 40,
                'form.html.show-if': "return args[0].includes('EQ');",
                'form.show-depends': ['nature'],
            },
            'impact_informatique': {
                'width': 40,
                'form.html.show-if': "return args[0].includes('EQ');",
                'form.show-depends': ['nature'],
            },
            'consommables_eventuels': {
                'width': 40,
                'format': 'text',
                'form.html.show-if': "return args[0].includes('EQ');",
                'form.show-depends': ['nature'],
            },
            'it_caracteristiques_minimales': {
                'form.html.show-if': "return args[0].includes('SW');",
                'form.show-depends': ['nature'],
            },
            'it_a_installer': {
                'form.html.show-if': "return args[0].includes('SW');",
                'form.show-depends': ['nature'],
            },
            'avis_cadre_sup': {
                'title': _("Avis favorable cadre supérieur de pôle"),
                'width': 40,
            },
            'commentaire_cadre_sup': {
                'title': _("Commentaire du cadre supérieur de pôle"),
                'width': 200,
            },
            "decision_validateur": (
                SmartField,
                {
                    "title": _("Approbation chef de pôle ou directeur"),
                    'max_width': 40,
                },
            ),
            "decision_soumission": {
                "title": _("Commentaire chef de pôle ou directeur"),
                "format": "text",
                "width": 200,
            },
            'programme': {
                'autocomplete': True,
                'lookup': lambda view_params: list(Programme.objects.all().values_list('id', 'nom')) + [(None, '-- Indéfini --')],
                'choices': lambda view_params: tuple(Programme.active_objects.all().values_list('id', 'nom').order_by('code')),
                "width": 150,
            },
            'domaine': {
                'autocomplete': True,
                "width": 150,
            },
            # Limitons le choix pour l'expert métier aux personnes qui ont au moins un rôle d'expert
            # L'utilisation d'une fonction (ici une fonction lambda) permet de faire cette évaluation à chaque instanciation
            # (ouverture de la page) et non pas seulement au lancement de Django
            'expert_metier': {
                'format': 'choice',
                'autocomplete': True,
                'lookup': user_lookup,
                'choices': lambda view_params=None: tuple(
                    UserUfRole.objects.order_by()
                    .filter(role_code='EXP', user__is_active=True)
                    .annotate(
                        libelle=ExpressionWrapper(
                            Concat(F('user__first_name'), Value(' '), F('user__last_name')),
                            output_field=TextField(),
                        )
                    )
                    .values_list('user', 'libelle')
                    .distinct()
                ),
            },
            'avis_biomed': {
                'width': 40,
            },
            'commentaire_biomed': {
                'title': _("Commentaire expert"),
                'width': 200,
            },
            'montant_unitaire_expert_metier': {
                'title': _("Montant expert TMP TMP"),
                'table.hidden': True,
            },
            'arbitrage_commission': {
                'title': _("Arbitrage"),
                'width': 100,
                'choices': lambda view_params: Arbitrage.objects.filter(
                    Q(cloture__isnull=True) | Q(cloture__gt=timezone.now()),
                    discipline__code='EQ',
                )
                .annotate(label=Concat(F('code'), Value(' - '), F('nom')))
                .values_list('pk', 'label'),
            },
            # "montant_total_expert_metier": {
            #     "format": "money",
            #     "decimal_symbol": ",",
            #     "thousands_separator": " ",
            #     "currency_symbol": " €",
            #     "symbol_is_after": True,
            #     "precision": 0,
            #     "max_width": 110,
            #     "footer_data": "sum",
            # },
            'commentaire_provisoire_commission': {
                'width': 200,
            },
            'commentaire_definitif_commission': {
                'width': 200,
            },
            'quantite_validee': {
                'title': _("Qté validée"),
                'width': 40,
                'data_if_null': 'quantite',
                'depends': [
                    'quantite',
                ],
            },
            'enveloppe_allouee': {
                'hidden': True,
                'title': _("XX Mt validé"),  # Use 'montant_valide_conditional' for display
                "format": "money",
                "decimal_symbol": ",",
                "thousands_separator": " ",
                "currency_symbol": " €",
                "symbol_is_after": True,
                "precision": 0,
                "max_width": 120,
                # "footer_data": "sum_if_ext",
                # "calc_data_test": 'valide_flag',
                # 'data_if_null': 'montant_arbitrage',
                # 'depends': [
                #     'montant_arbitrage',
                # ],
            },
            'gel': {
                'title': _("Définitif"),
                'width': 40,
            },
        }

        fields_to_copy = (
            'nature',
            'contact',
            'dect_contact',
            'date_premiere_demande',
            'nom_projet',
            'libelle',
            'description',
            'localisation',
            'cause',
            'it_caracteristiques_minimales',
            'it_a_installer',
            'referent',
            'materiel_existant',
            'quantite',
            'prix_unitaire',
            'it_cout_formation',
            'impact_travaux',
            'impact_informatique',
            'consommables_eventuels',
            'argumentaire_detaille',
            # 'montant_unitaire_expert_metier',
            # 'montant_total_expert_metier',
            'arg_interet_medical',
            'arg_commentaire_im',
            'arg_oblig_reglementaire',
            'arg_commentaire_or',
            'arg_recommandations',
            'arg_commentaire_r',
            'arg_confort_patient',
            'arg_commentaire_cp',
            'arg_confort_perso_ergo',
            'arg_commentaire_pe',
            'arg_notoriete',
            'arg_commentaire_n',
            'arg_projet_chu_pole',
            'arg_commentaire_pcp',
            'arg_gain_financier',
            'arg_commentaire_gf',
            'arg_mutualisation',
            'arg_commentaire_m',
            'arg_innovation_recherche',
            'arg_commentaire_ir',
            'autre_argumentaire',
        )

        initial_on_copy = {
            'avis_cadre_sup': None,
            'commentaire_cadre_sup': None,
            'decision_soumission': None,
            'decision_validateur': None,
            'programme': None,
            'domaine': None,
            'expert_metier': None,
            'commentaire_biomed': None,
            'montant_unitaire_expert_metier': None,
            'avis_biomed': None,
            'commentaire_provisoire_commission': None,
            'commentaire_definitif_commission': None,
            'arbitrage_commission': None,
            'enveloppe_allouee': None,
            'quantite_validee': None,
            'documents_sf': None,
            'gel': False,
        }

        form_layout = """
        # Titre de la page
        """

        def form_message(view_params):
            choices = view_params['request_get'].get('choices')
            if choices:
                choices = json.loads(choices)
                if 'calendrier' in choices and len(choices['calendrier']) == 1:
                    qs = Campagne.objects.filter(pk=int(choices['calendrier'][0]))
                    if len(qs) == 1:
                        return qs[0].message
            return None

    # Champs calculé qui détermine les campagnes vers lesquelles une demande peut être copiée
    # Le calcul se base sur la nature de la demande (il faut que les campagnes destinations soient compatibles)
    # et les dates de début et fin des campagnes destination (doivent être ouvertes).
    # La colonne est une chaîne de caractère qui peut être interprétées en JSON comme une liste des pk des campagnes, sous forme de
    # chaînes de caractères.
    can_copy_to_campagnes = (
        ComputedSmartField,
        {
            'hidden': True,
            'data': lambda view_params: Concat(
                Value('['),
                Coalesce(
                    Campagne.objects.annotate(natures_str=Cast('natures', output_field=CharField()), reff=Value('o'))
                    .filter(
                        natures_str__contains=OuterRef('nature'),
                        debut_recensement__lt=view_params['now'],
                        fin_recensement__gt=view_params['now'],
                    )
                    .order_by()
                    .values('reff')
                    # .annotate(pk_str=Cast('pk', output_field=CharField()))
                    # .values('pk_str')
                    .annotate(
                        whole_text=StringAgg(
                            Concat(
                                Value('"'),
                                Cast(F('pk'), output_field=CharField()),
                                Value('"'),
                            ),
                            ',',
                            output_field=CharField(),
                        )
                    ).values('whole_text'),
                    Value(''),
                    output_field=CharField(),
                ),
                Value(']'),
                output_field=CharField(),
            ),
        },
    )

    # Maintenant les colonnes créées 'manuellement' (déclarées)
    redacteur_view = (
        ComputedSmartField,
        {
            'title': 'Rédacteur',
            'help_text': _(
                "Le rédacteur de la fiche est déterminé à partir "
                "du nom de la personne connectée au moment de la création de la demande."
            ),
            'initial': lambda view_params: view_params['user'].first_name + ' ' + view_params['user'].last_name,
            'data': Concat('redacteur__first_name', Value(' '), 'redacteur__last_name'),
            'depends': ['redacteur'],
        },
    )

    service_view = (
        ComputedSmartField,
        {
            'title': 'Service',
            'form.help_text': _("Le service est déterminé automatiquement à partir de l'UF"),
            'initial': lambda view_params: _("Automatique"),
            'data': Concat('uf__service__code', Value(' - '), 'uf__service__nom'),
            'form.data': {
                'source': 'uf',
                'choices': lambda view_params: {id: name for id, name in Uf.objects.all().values_list('pk', 'service__nom')},
            },
            'depends': ['uf'],
        },
    )

    pole_view = (
        ComputedSmartField,
        {
            'title': 'Pôle',
            'form.help_text': _("Le pôle est déterminé automatiquement à partir de l'UF"),
            'initial': lambda view_params: _("- Automatique -"),
            'data': Concat('uf__pole__code', Value(' - '), 'uf__pole__nom'),
            'form.data': {
                'source': 'uf',
                'choices': lambda view_params: {id: name for id, name in Uf.objects.all().values_list('pk', 'pole__nom')},
            },
            'depends': ['uf'],
        },
    )

    etablissement_view = (
        ComputedSmartField,
        {
            'title': 'Etablissement',
            'form.help_text': _("L'établissement est déterminé automatiquement à partir de l'UF"),
            'initial': lambda view_params: _("- Automatique -"),
            'data': Concat('uf__etablissement__code', Value(' - '), 'uf__etablissement__nom'),
            'form.data': {
                'source': 'uf',
                'choices': lambda view_params: {id: name for id, name in Uf.objects.all().values_list('pk', 'etablissement__nom')},
            },
            'depends': ['uf'],
        },
    )

    redacteur_nom = (
        ComputedSmartField,
        {
            "format": "text",
            "title": _("Rédacteur"),
            'width': 100,
            "data": Concat(F("redacteur__first_name"), Value(" "), F("redacteur__last_name")),
            "depends": ["redacteur"],
        },
    )
    uf_nom = (
        ComputedSmartField,
        {
            "format": "text",
            'width': 125,
            "title": _("Nom UF"),
            "data": F("uf__nom"),
            "depends": [],  # Trick as a workaround
        },
    )
    uf_code = (
        ComputedSmartField,
        {
            "format": "string",
            'width': 50,
            "title": _("Code UF"),
            "data": F("uf__code"),
            "depends": [],  # Trick as a workaround
        },
    )
    pole_code = (
        ComputedSmartField,
        {
            "title": _("Code Pôle"),
            'width': 50,
            "format": 'string',
            "data": F('uf__pole__code'),
            "depends": [],  # Trick as a workaround
        },
    )
    pole_nom = (
        ComputedSmartField,
        {
            'title': _("Pôle"),
            'format': 'text',
            'width': 125,
            'data': F('uf__pole__nom'),
            "depends": [],  # Trick as a workaround
        },
    )
    argumentaire_detaille = (
        ComputedSmartField,
        {
            'title': _("Argumentaire"),
            'format': 'html',
            'width': 500,
            'min_width': 100,
            "data": ExpressionWrapper(
                Concat(
                    Value("<p>"),
                    Case(
                        When(
                            arg_interet_medical=True,
                            then=Concat(
                                Value("<b>Intérêt médical : </b>"),
                                F("arg_commentaire_im"),
                                Value("<br>"),
                                output_field=TextField(),
                            ),
                        ),
                    ),
                    Case(
                        When(
                            arg_oblig_reglementaire=True,
                            then=Concat(
                                Value("<b>Obligation Règlementaire : </b>"),
                                F("arg_commentaire_or"),
                                Value("<br>"),
                                output_field=TextField(),
                            ),
                        ),
                    ),
                    Case(
                        When(
                            arg_recommandations=True,
                            then=Concat(
                                Value("<b>Recommandations : </b>"),
                                F("arg_commentaire_r"),
                                Value("<br>"),
                                output_field=TextField(),
                            ),
                        ),
                    ),
                    Case(
                        When(
                            arg_projet_chu_pole=True,
                            then=Concat(
                                Value("<b>Projet institutionnel : </b>"),
                                F("arg_commentaire_pcp"),
                                Value("<br>"),
                                output_field=TextField(),
                            ),
                        ),
                    ),
                    Case(
                        When(
                            arg_confort_patient=True,
                            then=Concat(
                                Value("<b>Confort patient : </b>"),
                                F("arg_commentaire_cp"),
                                Value("<br>"),
                                output_field=TextField(),
                            ),
                        ),
                    ),
                    Case(
                        When(
                            arg_confort_perso_ergo=True,
                            then=Concat(
                                Value("<b>Ergonomie du travail : </b>"),
                                F("arg_commentaire_pe"),
                                Value("<br>"),
                                output_field=TextField(),
                            ),
                        ),
                    ),
                    Case(
                        When(
                            arg_notoriete=True,
                            then=Concat(
                                Value("<b>Notoriété : </b>"),
                                F("arg_commentaire_n"),
                                Value("<br>"),
                                output_field=TextField(),
                            ),
                        ),
                    ),
                    Case(
                        When(
                            arg_innovation_recherche=True,
                            then=Concat(
                                Value("<b>Innovation, recherche : </b>"),
                                F("arg_commentaire_ir"),
                                Value("<br>"),
                                output_field=TextField(),
                            ),
                        ),
                    ),
                    Case(
                        When(
                            arg_mutualisation=True,
                            then=Concat(
                                Value("<b>Mutualisation : </b>"),
                                F("arg_commentaire_m"),
                                Value("<br>"),
                                output_field=TextField(),
                            ),
                        ),
                    ),
                    Case(
                        When(
                            arg_gain_financier=True,
                            then=Concat(
                                Value("<b>Gain financier : </b>"),
                                F("arg_commentaire_gf"),
                                Value("<br>"),
                                output_field=TextField(),
                            ),
                        ),
                    ),
                    Case(
                        When(
                            autre_argumentaire__gt=" ",
                            then=Concat(
                                Value("<b>Autre : </b>"),
                                F("autre_argumentaire"),
                                output_field=TextField(),
                            ),
                        ),
                    ),
                    Value("</p>"),
                ),
                output_field=TextField(),
            ),
        },
    )
    montant_initial = (
        ComputedSmartField,
        {
            'title': _("Montant initial"),
            'format': 'money',
            'decimal_symbol': ',',
            'thousands_separator': " ",
            'currency_symbol': " €",
            'symbol_is_after': True,
            'precision': 0,
            'max_width': 120,
            'data': ExpressionWrapper(
                Case(
                    When(
                        prix_unitaire__isnull=False,
                        then=F("quantite") * F("prix_unitaire"),
                    ),
                ),
                output_field=DecimalField(),
            ),
            'form.data': 'prix_unitaire * quantite',
            'depends': [
                'prix_unitaire',
                'quantite',
            ],
        },
    )
    prix_unitaire_conditional = (
        ConditionnalSmartField,
        {
            'title': 'PU Corrigé',
            "format": "conditional_money",
            "decimal_symbol": ",",
            "thousands_separator": " ",
            "currency_symbol": " €",
            "symbol_is_after": True,
            "precision": 0,
            "max_width": 120,
            'fields': (
                'montant_unitaire_expert_metier',
                'prix_unitaire',
            ),
        },
    )
    montant_arbitrage = (
        ComputedSmartField,
        {
            'title': _("Montant arbitrage"),
            'help_text': _(
                "Montant calculé en vue de l'arbitrage qui est la meilleure estimation à partir des montants indiqués sur la "
                "demande et amendés par l'expert métier"
            ),
            "format": "money",
            "decimal_symbol": ",",
            "thousands_separator": " ",
            "currency_symbol": " €",
            "symbol_is_after": True,
            "precision": 0,
            "max_width": 120,
            "footer_data": "sum",
            'data': ExpressionWrapper(
                Case(
                    # When(
                    #     montant_total_expert_metier__isnull=False,
                    #     then=F("montant_total_expert_metier"),
                    # ),
                    When(
                        montant_unitaire_expert_metier__isnull=False,
                        then=F("quantite") * F("montant_unitaire_expert_metier"),
                    ),
                    # When(montant__isnull=False, then=F("montant")),
                    When(
                        prix_unitaire__isnull=False,
                        then=F("quantite") * F("prix_unitaire"),
                    ),
                ),
                output_field=DecimalField(),
            ),
            'depends': [
                'montant_unitaire_expert_metier',
                'prix_unitaire',
                # 'montant_total_expert_metier',
                'quantite',
                # 'montant',
            ],
        },
    )
    quantite_validee_conditional = (
        ConditionnalSmartField,
        {
            'title': _("Quantité validée"),
            'format': "conditional_integer",
            'fields': (
                'quantite_validee',
                'quantite',
            ),
            'flag_field': 'arbitrage_commission__valeur',
        },
    )

    # Montant calculé à partir du meilleur prix unitaire et de la meilleure quantité...
    montant_qte_validee = (
        ComputedSmartField,
        {
            'title': _("Montant qté validée"),
            'hidden': True,
            'depends': (
                'quantite',
                'prix_unitaire',
                'quantite_validee',
                'montant_unitaire_expert_metier',
            ),
            'data': Coalesce(F('quantite_validee'), F('quantite'))
            * Coalesce(F('montant_unitaire_expert_metier'), F('prix_unitaire')),
        },
    )
    montant_valide_conditional = (
        ConditionnalSmartField,
        {
            'title': _("Montant validé"),
            'format': "conditional_money",
            "decimal_symbol": ",",
            "thousands_separator": " ",
            "currency_symbol": " €",
            "symbol_is_after": True,
            "precision": 0,
            "max_width": 120,
            'fields': (
                'enveloppe_allouee',
                'montant_qte_validee',
            ),
            'flag_field': 'arbitrage_commission__valeur',
            'footer_data': 'sum_conditional',
        },
    )
    # Ce montant 'final' n'a pas vocation à être affiché directement car il est peu significatif pour l'utilisateur ;
    # En effet, il ne représente ni ce qui est validé (il n'est pas nul si la demande est refusée) ni ce qui doit
    # être validé (c'est 'montant_arbitrage' qui joue ce rôle).
    # Cela sert juste à calculer le TCD de répartition
    # L'algorithme complet est à revoir car il y a des cas sans solution claire (quand il n'y a un montant global défini par
    #   l'utilisateur ou l'expert et pas de montant global mais seulement une quantité validée par l'arbitre...)
    montant_final = (
        ComputedSmartField,
        {
            'title': _("Montant final"),
            'help_text': _(
                "Montant final, qui est le montant en vue de l'arbitrage éventuellement modifié par l'arbitre (si enveloppe "
                "finalement allouée)"
            ),
            'hidden': True,
            "format": "money",
            "decimal_symbol": ",",
            "thousands_separator": " ",
            "currency_symbol": " €",
            "symbol_is_after": True,
            "precision": 0,
            "max_width": 120,
            "footer_data": "sum",
            # 'data': ExpressionWrapper(
            #     Case(
            #         When(
            #             arbitrage_commission__valeur=True,
            #             then=Case(
            #                 When(
            #                     enveloppe_allouee__isnull=False,
            #                     then=F("enveloppe_allouee"),
            #                 ),
            #                 When(
            #                     montant_unitaire_expert_metier__isnull=False,
            #                     then=F("quantite_validee") * F("montant_unitaire_expert_metier"),
            #                 ),
            #                 When(
            #                     prix_unitaire__isnull=False,
            #                     then=F("quantite_validee") * F("prix_unitaire"),
            #                 ),
            #                 default=Value(math.nan),  # Pour indiquer que ce n'est pas un cas 'valide'
            #                 output_field=DecimalField(),
            #             ),
            #         ),
            #         # When(
            #         #     montant_total_expert_metier__isnull=False,
            #         #     then=F("montant_total_expert_metier"),
            #         # ),
            #         When(
            #             montant_unitaire_expert_metier__isnull=False,
            #             then=F("quantite") * F("montant_unitaire_expert_metier"),
            #         ),
            #         # When(montant__isnull=False, then=F("montant")),
            #         When(
            #             prix_unitaire__isnull=False,
            #             then=F("quantite") * F("prix_unitaire"),
            #         ),
            #     ),
            #     output_field=DecimalField(),
            # ),
            'data': Coalesce(F('enveloppe_allouee'), F('montant_qte_validee'), Value(Decimal(0.0))),
            'depends': [
                # 'arbitrage_commission',
                'enveloppe_allouee',
                'montant_qte_validee',
                # 'montant_unitaire_expert_metier',
                # 'prix_unitaire',
                # 'montant_total_expert_metier',
                # 'quantite',
                # 'montant',
            ],
        },
    )
    enveloppe_finale = (
        ComputedSmartField,
        {
            'title': _("Enveloppe"),
            'help_text': _("Montant de l'enveloppe finale"),
            "format": "money",
            "decimal_symbol": ",",
            "thousands_separator": " ",
            "currency_symbol": " €",
            "symbol_is_after": True,
            "precision": 0,
            "max_width": 120,
            "footer_data": "sum",
            'data': Case(
                When(
                    arbitrage_commission__valeur=True,
                    then=Coalesce(F('enveloppe_allouee'), F('montant_qte_validee'), Value(Decimal(0.0))),
                ),
            ),
            'depends': [
                'arbitrage_commission',
                'enveloppe_allouee',
                'montant_qte_validee',
            ],
        },
    )
    montant_consomme = (
        ComputedSmartField,
        {
            'title': _("Montant consommé"),
            'hidden': True,
            'data': ExpressionWrapper(
                Concat(
                    Value('{'),
                    F('montant_arbitrage'),
                    Value(' ,'),
                    Coalesce(
                        Cast(F('enveloppe_allouee'), output_field=CharField()),
                        Value('null'),
                    ),
                    Value('}'),
                ),
                output_field=CharField(),
            ),
            'depends': (
                'montant_arbitrage',
                'enveloppe_allouee',
            ),
        },
    )
    documents_sf = (
        DocumentsSmartField,
        {
            'title': 'Documents joints',
            'data': all_documents_json_partial(Demande),  # Hum... Sans doute possible de le configurer par défaut...
        },
    )
    # Ce drapeau peut désormais être remplacé par artitrage__valeur, qui donne le même résultat, mais sans dépendre de
    # l'interprétation d'un code...
    # valide_flag = (
    #     ComputedSmartField,
    #     {
    #         'hidden': True,
    #         'data': ExpressionWrapper(
    #             Q(arbitrage_commission__code=1) | Q(arbitrage_commission__code=2),
    #             output_field=BooleanField(),
    #         ),
    #     },
    # )
    arbitrage = (
        ComputedSmartField,
        {
            'title': _("Validé"),
            'format': 'boolean',
            'hidden': True,
            'data': F('arbitrage_commission__valeur'),
        },
    )
    roles = (
        ComputedSmartField,
        {
            'special': 'roles',
            'hidden': True,
            'data': class_roles_expression(
                Demande,
                owner_field='redacteur',
                uf_field='uf',
                programme_field='programme',
                domaine_field='domaine',
                campagne_field='calendrier',
                expert_field='expert_metier',
            ),
            'depends': [
                'uf',
                'redacteur',
                'programme',
                'domaine',
                'calendrier',
                'expert_metier',
            ],
        },
    )
    # Calcul de l'état d'une demande suivant le workflow décrit dans la documentation (dem/internals/dem_states.dot)
    dyn_state = (
        ComputedSmartField,
        {
            'hidden': not config.settings.DEBUG,
            'title': _("Etat dyn."),
            'help_text': _("Etat calculé dynamiquement à partir des valuers des champs de chaque demande."),
            'data': lambda view_params: Case(
                When(
                    gel=True,
                    then=Case(
                        When(
                            arbitrage_commission__valeur=True,
                            then=Case(
                                When(
                                    previsionnel__isnull=False,
                                    then=Case(
                                        When(
                                            previsionnel__solder_ligne=True,
                                            previsionnel__date_modification__lt=view_params['now'] - datetime.timedelta(days=90),
                                            then=Value("TRAITE"),
                                        ),
                                        default=Value("VALIDE"),
                                    ),
                                ),
                                default=Value("A_BASCULER"),
                            ),
                        ),
                        When(
                            arbitrage_commission__valeur=False,
                            then=Value("REFUSE"),
                        ),
                        default=Value("ANNULE"),
                    ),
                ),
                default=Case(
                    When(
                        montant_arbitrage__isnull=False,
                        avis_biomed__isnull=False,
                        programme__isnull=False,
                        then=Case(
                            When(
                                decision_validateur__isnull=True,
                                then=Case(
                                    When(
                                        expert_metier__isnull=True,
                                        then=Value("AAP_AREP"),
                                    ),
                                    default=Case(
                                        When(
                                            programme__arbitre__isnull=True,
                                            then=Value("AAP"),
                                        ),
                                        default=Value("AAP_AARB"),
                                    ),
                                ),
                            ),
                            default=Case(
                                When(
                                    expert_metier__isnull=True,
                                    then=Value("AREP"),
                                ),
                                default=Case(
                                    When(
                                        programme__arbitre__isnull=True,
                                        then=Value("WAIT"),
                                    ),
                                    default=Value("AARB"),
                                ),
                            ),
                        ),
                    ),
                    default=Case(
                        When(
                            expert_metier__isnull=True,
                            then=Case(
                                When(
                                    decision_validateur__isnull=True,
                                    then=Value("AAP_AREP"),
                                ),
                                default=Value("AREP"),
                            ),
                        ),
                        default=Case(
                            When(
                                decision_validateur__isnull=True,
                                then=Case(
                                    When(programme__isnull=True, then=Value("AAP_AREP_AEXP")),
                                    default=Value("AAP_AEXP"),
                                ),
                            ),
                            default=Case(
                                When(programme__isnull=True, then=Value("AREP_AEXP")),
                                default=Value("AEXP"),
                            ),
                        ),
                    ),
                ),
            ),
            'depends': [
                'gel',
                'programme',
                'decision_validateur',
                'expert_metier',
                'avis_biomed',
                'montant_arbitrage',
                'arbitrage_commission',
            ],
        },
    )


class DemandeEqptSmartView(DemandeSmartView):
    class Meta:
        columns = (
            'code',
            'num_dmd',
            'nature',
            'calendrier',
            'campagne_redirect',
            'can_copy_to_campagnes',
            'roles',
            'state_code',
            'redacteur',
            'redacteur_view',
            'contact',
            'dect_contact',
            'discipline_dmd',
            'date_premiere_demande',
            'uf',
            'pole_nom',
            'uf_code',
            'uf_nom',
            'priorite',
            'nom_projet',
            'libelle',
            'description',
            'localisation',
            'cause',
            'it_caracteristiques_minimales',
            'it_a_installer',
            'referent',
            'materiel_existant',
            'quantite',
            'prix_unitaire',
            'montant_initial',
            'it_cout_formation',
            'impact_travaux',
            'impact_informatique',
            'consommables_eventuels',
            'argumentaire_detaille',
            'tmp_int_year',
            'tmp_int_remain',
            # 'documents_joints',
            'documents_sf',
            'avis_cadre_sup',
            'commentaire_cadre_sup',
            'decision_validateur',
            'decision_soumission',
            'programme',
            'domaine',
            'expert_metier',
            'prix_unitaire_conditional',
            # 'montant_unitaire_expert_metier',
            # 'montant_total_expert_metier',
            'arg_interet_medical',
            'arg_commentaire_im',
            'arg_oblig_reglementaire',
            'arg_commentaire_or',
            'arg_recommandations',
            'arg_commentaire_r',
            'arg_confort_patient',
            'arg_commentaire_cp',
            'arg_confort_perso_ergo',
            'arg_commentaire_pe',
            'arg_notoriete',
            'arg_commentaire_n',
            'arg_projet_chu_pole',
            'arg_commentaire_pcp',
            'arg_gain_financier',
            'arg_commentaire_gf',
            'arg_mutualisation',
            'arg_commentaire_m',
            'arg_innovation_recherche',
            'arg_commentaire_ir',
            'autre_argumentaire',
            'commentaire_biomed',
            'montant_unitaire_expert_metier',
            'avis_biomed',
            'montant_arbitrage',
            'arbitrage_commission',
            'arbitrage',
            'commentaire_provisoire_commission',
            'commentaire_definitif_commission',
            'quantite_validee',
            'quantite_validee_conditional',
            'montant_qte_validee',
            'enveloppe_allouee',
            'montant_valide_conditional',
            'montant_final',
            'montant_consomme',
            'dyn_state',
            'gel',
            'tools',
        )
        selectable_columns = (
            # 'num_dmd',
            'campagne_redirect',
            'date_premiere_demande',
            'pole_nom',
            'uf_code',
            'uf_nom',
            'redacteur_view',
            'priorite',
            'nom_projet',
            'libelle',
            'description',
            'cause',
            'referent',
            'materiel_existant',
            'quantite',
            'prix_unitaire',
            # 'montant',
            'impact_travaux',
            'impact_informatique',
            'it_caracteristiques_minimales',
            'it_a_installer',
            'argumentaire_detaille',
            'documents_sf',
            'avis_cadre_sup',
            'commentaire_cadre_sup',
            'decision_validateur',
            'decision_soumission',
            'programme',
            'domaine',
            'expert_metier',
            # 'montant_unitaire_expert_metier',
            'prix_unitaire_conditional',
            'it_cout_formation',
            # 'montant_unitaire_expert_metier',
            # 'montant_total_expert_metier',
            'commentaire_biomed',
            'avis_biomed',
            'arbitrage_commission',
            'commentaire_provisoire_commission',
            'commentaire_definitif_commission',
            'quantite_validee_conditional',
            'montant_valide_conditional',
            'arbitrage',
            # 'quantite_validee',
            # 'enveloppe_allouee',
            'gel',
        )
        settings = {
            'code': {
                # 'frozen': True,
            },
            'redacteur': {
                'hidden': True,
                'initial': lambda params: params['user'].pk,
            },
            'referent': {
                'form.title': _("Nom du demandeur"),
            },
            'num_dmd': {
                'title': 'N°',
                'hidden': True,
            },
            'nom_projet': {
                'smart-copy': 'libelle',
            },
            'discipline_dmd': {
                'hidden': True,
                'initial': lambda params: Discipline.objects.filter(code='EQ')[0],
            },
            'quantite': {
                'title': 'Qté',
                'header_sort': False,
            },  # on peut aussi ne changer que quelques propriétés
            'montant_expert_metier': {
                'hidden': True,  # Use prix_unitaire_conditional instead
            },
            'quantite_validee': {
                'hidden': True,  # Use quantite_validee_conditional instead
            },
            'enveloppe_allouee': {
                'hidden': True,  # Use montant_valide_conditional instead
            },
        }
        # Exclusion des demandes de travaux (kind of hack...)
        base_filter = Q(discipline_dmd__isnull=True) | ~Q(discipline_dmd__code='TX')
        user_filters = {
            'campagne': {
                'type': 'select',
                'choices': {
                    'fieldname': 'calendrier',
                    'label': F('calendrier__nom'),
                    'sort': F('calendrier__code'),
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
        }
        form_layout = """
        # d'équipement ou de logiciel {{ instance.code }}
            <redacteur> <discipline_dmd>
            <calendrier> <nature>
            # Le demandeur
                <referent> <redacteur_view>
                <uf> <pole_view>
                <service_view> <etablissement_view>
            # Description du projet
                <--libelle----> <-cause->
                <--contact----> <-dect_contact-->
                <--priorite---> <date_premiere_demande>
                <--nom_projet-> <materiel_existant>
                <description---+--------->
                <description---+--------->
                <localisation--+--------->
                <it_caracteristiques_minimales-+-->
                <it_a_installer-+-->
                #arg Argumentaire
                    <arg_interet_medical>      <arg_commentaire_im-+--+->
                    <arg_oblig_reglementaire>  <arg_commentaire_or--+-+->
                    <arg_recommandations>      <arg_commentaire_r-+---+->
                    <arg_projet_chu_pole>      <arg_commentaire_pcp-+-+->
                    <arg_confort_patient>      <arg_commentaire_cp-+--+->
                    <arg_confort_perso_ergo>   <arg_commentaire_pe--+-+->
                    <arg_notoriete>            <arg_commentaire_n---+-+->
                    <arg_innovation_recherche> <arg_commentaire_ir--+-+->
                    <arg_gain_financier>       <arg_commentaire_gf-+--+->
                    <arg_mutualisation>        <arg_commentaire_m---+-+->
                    <autre_argumentaire--------+--------+-------+------->
                #int Intéressement
                    <tmp_int_year> <tmp_int_remain>
            # Coûts
                <quantite> <prix_unitaire>
                <montant_initial>
                <impact_travaux> <impact_informatique>
                <consommables_eventuels--+-->
            # Avis encadrement
                <avis_cadre_sup> <commentaire_cadre_sup>
            # Approbation
                <decision_validateur> <decision_soumission>
            # Répartition
                <programme> <domaine> <expert_metier>
            # Expertise
                <commentaire_biomed---+--->
                <montant_unitaire_expert_metier> <avis_biomed>
            # Arbitrage
                <commentaire_provisoire_commission-+--+--+-->
                <commentaire_definitif_commission--+--+--+-->
                <arbitrage_commission> <quantite_validee> <enveloppe_allouee> <gel>
            # Documents joints
                <--documents_sf-+--+--+->
        """
        form_rules = {
            'interessement': {
                'depends': ['calendrier'],
                'func': 'show-if-expr',
                'expr': 'if (args[0]==6) {return true;} else {return false;}',
                'targets': ['fieldset-int'],
            },
            'argumentaire': {
                'depends': ['calendrier'],
                'func': 'show-if-expr',
                'expr': 'if ((args[0]!=6)&&(args[0]!=17)) {return true;} else {return false;}',
                'targets': ['fieldset-arg'],
            },
        }

    documents_sf = (
        DocumentsSmartField,
        {
            'title': 'Documents joints',
            'data': all_documents_json_partial(Demande),  # Hum... Sans doute possible de le configurer par défaut...
        },
    )

    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'dem:request-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir la demande"),
                },
                {
                    'tool': 'copy',
                    'url_name': 'dem:request-copy',
                    'url_args': ('${id}',),
                    'choices': {
                        'nature': {
                            'column': 'nature',
                            'title': _("Nature :"),
                            'lookup': lambda view_params: dict(NATURE_CHOICES),
                        },
                        'calendrier': {
                            'json_column': 'can_copy_to_campagnes',
                            'title': _("Demande à copier pour :"),
                            'lookup': lambda view_params: dict(user_campagnes(view_params).values_list('pk', 'nom')),
                        },
                    },
                    "tooltip": "Copier la demande",
                },
                {
                    'tool': 'delete',
                    'url_name': 'dem:request-ask-delete',
                    'url_args': ('${id}',),
                    "tooltip": "Supprimer la demande",
                },
            ],
        },
    )


class MesDemandesSmartView(DemandeEqptSmartView):
    class Meta:
        # Filtre de base : Uniquement les demandes sur les UF pour lesquelles je peux faire une demande...
        def base_filter(self, view_params: dict):  # NOQA
            # Liste des rôles pour lesquels je peux faire une demande sur une UF
            tmp_scope = roles_demandes_possibles(view_params['user'])
            return (
                (
                    Q(uf__in=tmp_scope.values('uf'))
                    | Q(uf__service__in=tmp_scope.values('service'))
                    | Q(uf__centre_responsabilite__in=tmp_scope.values('centre_responsabilite'))
                    | Q(uf__pole__in=tmp_scope.values('pole'))
                    | Q(uf__site__in=tmp_scope.values('site'))
                    | Q(uf__etablissement__in=tmp_scope.values('etablissement')),
                ),
                # Hack pour ne pas voir les demandes de travaux
                Q(discipline_dmd__isnull=True) | ~Q(discipline_dmd__code='TX'),
            )


class DemandesEnCoursSmartView(DemandeEqptSmartView):
    class Meta:
        help_text = _(
            "Toutes les demandes qui n'ont pas encore été arbitrées définitivement se trouvent dans ce tableau."
            " Après validation par le chef de pôle, chaque demande sera instruite par un spécialiste"
            " puis arbitrée soit par une commission (pour la matériel des services de soin) soit par un responsable."
        )
        settings = {
            'quantite_validee_conditional': {
                'hidden': True,
            },
            'montant_valide_conditional': {
                'hidden': True,
            },
        }
        columns__remove = (
            # 'arbitrage_commission',
            'commentaire_definitif_commission',
            'gel',
        )
        selectable_columns__remove = ('arbitrage_commission', 'commentaire_definitif_commission', 'gel')

        exports = {
            'xlsx': {
                'engine': 'xlsx',
                'label': 'Microsoft Excel 2003+',
                'filename': "Demandes en cours.xlsx",
            }
        }
        table_row_tooltip = {
            "columns": [
                'num_dmd',
                'uf_code',
                'uf_nom',
                'priorite',
                'libelle',
                'quantite',
                # 'montant',
                'argumentaire_detaille',
                'commentaire_cadre_sup',
                'decision_soumission',
            ]
        }

        def base_filter(self, view_params: dict):  # NOQA
            # Liste des rôles pour lesquels je peux faire une demande sur une UF
            tmp_scope = roles_demandes_possibles(view_params['user'])
            return (
                Q(gel__isnull=True) | Q(gel=False),
                Q(uf__in=tmp_scope.values('uf'))
                | Q(uf__service__in=tmp_scope.values('service'))
                | Q(uf__centre_responsabilite__in=tmp_scope.values('centre_responsabilite'))
                | Q(uf__pole__in=tmp_scope.values('pole'))
                | Q(uf__site__in=tmp_scope.values('site'))
                | Q(uf__etablissement__in=tmp_scope.values('etablissement')),
                ~Q(discipline_dmd__code='TX'),  # Exclut les demandes de travaux
            )


class DemandesAApprouverSmartView(DemandesEnCoursSmartView):
    class Meta:
        help_text = _(
            "Toutes les demandes qui n'ont pas encore été approuvées se trouvent dans ce tableau."
            " Après <b>approbation par le chef de pôle</b> (ou le directeur fonctionnel pour"
            " les services non médicaux), chaque demande sera instruite par un spécialiste"
            " puis arbitrée soit par une commission (pour le matériel des services de soin) soit par un responsable."
            " L'approbation par le chef de pôle (ou le directeur fonctionnel) se fait en modifiant les"
            " deux dernières colonnes du tableau. Il est également possible pour le chef de pôle de définir des montants"
            " pour approuver automatiquement les demandes (dans ses préférences)."
        )
        columns__remove = (
            'expert_metier',
            'programme',
            'domaine',
            'commentaire_biomed',
            'avis_biomed',
            'montant_arbitrage',
            'montant_unitaire_expert_metier',
            'quantite_validee_conditional',  # hidden
            'prix_unitaire_conditional',
            'montant_qte_validee',
            'montant_valide_conditional',
            'montant_final',
            'montant_consomme',
            'arbitrage',
            'arbitrage_commission',
            'commentaire_provisoire_commission',
            # 'commentaire_definitif_commission',
            'quantite_validee',
            'enveloppe_allouee',
            # 'gel',
        )
        selectable_columns__remove = (
            'expert_metier',
            'programme',
            'domaine',
            'commentaire_biomed',
            'avis_biomed',
            # 'montant_arbitrage',
            # 'montant_unitaire_expert_metier',
            'prix_unitaire_conditional',
            'quantite_validee_conditional',  # hidden
            # 'montant_qte_validee',
            'montant_valide_conditional',
            'commentaire_provisoire_commission',
            # 'commentaire_definitif_commission',
            # 'montant_final',
            # 'montant_consomme',
            'arbitrage',
            # 'arbitrage_commission',
            # 'quantite_validee',
            # 'enveloppe_allouee',
            # 'gel',
        )

        def base_filter(self, view_params: dict):  # NOQA
            # Liste des rôles pour lesquels je peux faire une demande sur une UF
            tmp_scope = roles_demandes_possibles(view_params['user'])
            return (
                Q(gel__isnull=True) | Q(gel=False),
                Q(decision_validateur__isnull=True),
                Q(uf__in=tmp_scope.values('uf'))
                | Q(uf__service__in=tmp_scope.values('service'))
                | Q(uf__centre_responsabilite__in=tmp_scope.values('centre_responsabilite'))
                | Q(uf__pole__in=tmp_scope.values('pole'))
                | Q(uf__site__in=tmp_scope.values('site'))
                | Q(uf__etablissement__in=tmp_scope.values('etablissement')),
                ~Q(discipline_dmd__code='TX'),  # Exclut les demandes de travaux
            )


class DemandesEtudeSmartView(DemandeEqptSmartView):
    class Meta:
        help_text = _("Ce tableau regroupe les demandes qui ont été approuvées (ou non) par le chef de pôle et qui sont à l'étude.")
        user_filters__update = {
            'state_code': {
                'type': 'select',
                'label': _('Validation chef de pôle / directeur'),
                'choices': '__STYLES__',
                'position': 'bar',
            },
        }
        row_styler = {
            'fieldname': 'state_code',
            'styles': {
                ('VALIDE_CP', 'INSTR_OK', 'ERR_VAL_EXP', 'AVFAV_EXP'): (
                    "background-color:#efe",
                    _("Demande approuvée par le chef de pôle<br>son instruction va pouvoir continuer"),
                ),
                'NONVAL_CP': (
                    "background-color:#fdd",
                    _("Demande non approuvée par le chef de pôle<br>elle ne sera pas arbitrée"),
                ),
            },
        }
        columns__remove = (
            'arbitrage',
            'quantite_validee',
            'quantite_validee_conditional',  # hidden
            'montant_qte_validee',
            'enveloppe_allouee',
            'montant_valide_conditional',
            'montant_final',
            'montant_consomme',
            'arbitrage_commission',
            'commentaire_definitif_commission',
            'gel',
        )
        selectable_columns__remove = (
            'quantite_validee_conditional',  # hidden
            'montant_valide_conditional',
            'arbitrage',
            'arbitrage_commission',
            'commentaire_definitif_commission',
        )

        def base_filter(self, view_params: dict):  # NOQA
            # Liste des rôles pour lesquels je peux faire une demande sur une UF
            tmp_scope = roles_demandes_possibles(view_params['user'])
            return (
                Q(gel__isnull=True) | Q(gel=False),
                Q(decision_validateur__isnull=False),
                Q(uf__in=tmp_scope.values('uf'))
                | Q(uf__service__in=tmp_scope.values('service'))
                | Q(uf__centre_responsabilite__in=tmp_scope.values('centre_responsabilite'))
                | Q(uf__pole__in=tmp_scope.values('pole'))
                | Q(uf__site__in=tmp_scope.values('site'))
                | Q(uf__etablissement__in=tmp_scope.values('etablissement')),
                ~Q(discipline_dmd__code='TX'),  # Exclut les demandes de travaux
            )


class DemandesArbitrageSmartView(DemandeEqptSmartView):
    class Meta:
        help_text = _("Toutes les demandes qui **peuvent** être arbitrées par moi")
        columns__remove = ('arbitrage',)
        columns__add = (
            'workflow_alert',
            # 'valide_flag',
            # 'montant_final', # test
        )
        selectable_columns__remove = ('arbitrage',)

        def base_filter(self, view_params):
            return (
                # Demandes non validées
                Q(gel=False),
                Q(programme__arbitre=view_params['user'].pk),
                ~Q(discipline_dmd__code='TX'),  # Exclut les demandes de travaux
            )

        user_filters__update = {
            'expert_metier': {'label': _("Expert métier"), 'type': 'select'},
            'avis_biomed': {'label': _("Avis favorable expert"), 'type': 'select'},
            'domaine': {'type': 'select'},
            'arbitrage_commission': {'label': _("Arbitrage"), 'type': 'select'},
        }
        row_styler = {
            'fieldname': 'state_code',
            'styles': {
                'NONVAL_CP': (
                    "background:#fdd",
                    "Demande non validée par le Chef de pôle (provisoire)",
                ),
                'INSTRUCTION': ("background:#eef", "Demande prête pour l'instruction"),
                'INSTR_OK': ("background:#eee", "Demande instruite (mais sans avis)"),
                'AVFAV_EXP': ("background:#efe", "Avis favorable de l'expert-métier"),
                'AVDEF_EXP': ("background:#fee", "Avis défavorable de l'expert-métier"),
                'ERR_VAL_EXP': ("background:#fed", "Erreur (pas de prix/montant)"),
                'VALIDE_ARB': ("background:#cfc", "Demande validée par l'arbitre"),
                'NONVAL_ARB': ("background:#fcc", "Demande non validée par l'arbitre"),
                'VALIDE_DEF': (
                    "color:#888;background:#cfc",
                    "Demande validée définitvement",
                ),
                'NONVAL_CP_DEF': (
                    "color:#888;background:#fcc",
                    "Demande non validée par le Chef de pôle (définitif)",
                ),
                'NONVAL_DEF': (
                    "color:#888;background:#fcc",
                    "Demande non validée définitivement",
                ),
            },
        }
        exports = {
            'xlsx': {
                'engine': 'xlsx',
                'label': 'Microsoft Excel 2003+',
                'filename': "Demandes en cours.xlsx",
            }
        }


class DemandesArchiveesSmartView(MesDemandesSmartView):
    class Meta:
        help_text = _(
            "Ce tableau reprend toutes les demandes archivées : Les demandes refusées <b>et</b>"
            " les demandes acceptées et traitées (terminées depuis plus de 3 mois)."
            " Vous pouvez renouveler une demande refusée en cliquant sur l'icône &laquo;&nbsp;copier&nbsp;&raquo;"
            " dans la dernière colonne du tableau"
        )
        columns__remove = (
            'commentaire_provisoire_commission',
            'arbitrage',
            'quantite_validee',
            'enveloppe_allouee',
        )
        selectable_columns__remove = (
            'commentaire_provisoire_commission',
            'arbitrage',
        )

        def base_filter(self, view_params: dict):  # NOQA : Method could be static
            tmp_scope = roles_demandes_possibles(view_params['user'])
            return (
                Q(uf__in=tmp_scope.values('uf'))
                | Q(uf__service__in=tmp_scope.values('service'))
                | Q(uf__centre_responsabilite__in=tmp_scope.values('centre_responsabilite'))
                | Q(uf__pole__in=tmp_scope.values('pole'))
                | Q(uf__site__in=tmp_scope.values('site'))
                | Q(uf__etablissement__in=tmp_scope.values('etablissement')),
                Q(state_code__in=['NONVAL_DEF', 'NONVAL_CP_DEF'])
                | Q(
                    state_code__in=['VALIDE_DEF'],
                    previsionnel__suivi_mes__startswith='1-',
                    previsionnel__date_modification__lt=timezone.now() - DRACHAR_DELAI_DEMANDE_TERMINEE,
                ),
                # {
                #     ':or': [
                #         {'state_code__in': ['NONVAL_DEF', 'NONVAL_CP_DEF']},
                #         {
                #             'state_code__in': ['VALIDE_DEF'],
                #             'previsionnel__suivi_mes__startswith': '1-',
                #             'previsionnel__date_modification__lt': timezone.now() - DRACHAR_DELAI_DEMANDE_TERMINEE,
                #         },
                #     ]
                # },
            )
            # return {
            #     ':or': [
            #         {'state_code__in': ['NONVAL_DEF', 'NONVAL_CP_DEF']},
            #         {
            #             'state_code__in': ['VALIDE_DEF'],
            #             'previsionnel__suivi_mes__startswith': '1-',
            #             'previsionnel__date_modification__lt': timezone.now() - DRACHAR_DELAI_DEMANDE_TERMINEE,
            #         },
            #     ]
            # }

        settings = {
            'state_code': {
                'title': _("Filtre type de demande"),
            },
        }

        row_styler = {
            'fieldname': 'state_code',
            'styles': {
                ('NONVAL_DEF', 'NONVAL_CP_DEF'): (
                    "background:#fcc",
                    "Demande non validée",
                ),
                'VALIDE_DEF': ("background:#cfc", "Demande validée et traitée"),
            },
        }
        exports = {
            'xlsx': {
                'engine': 'xlsx',
                'label': 'Microsoft Excel 2003+',
                'filename': "Demandes en cours.xlsx",
            }
        }
        user_filters__update = {
            'state_code': {
                'type': 'select',
                'choices': '__STYLES__',
                'position': 'bar',
            },
        }

    # Maintenant les colonnes créées 'manuellement' (déclarées)
    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'dem:request-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir la demande"),
                },
                {
                    'tool': 'copy',
                    'url_name': 'dem:request-copy',
                    'url_args': ('${id}',),
                    'choices': {
                        'nature': {
                            'column': 'nature',
                            'title': _("Nature :"),
                            'lookup': lambda view_params: dict(NATURE_CHOICES),
                        },
                        'calendrier': {
                            'json_column': 'can_copy_to_campagnes',
                            'title': _("Demande à copier pour :"),
                            'lookup': lambda view_params: dict(user_campagnes(view_params).values_list('pk', 'nom')),
                        },
                    },
                    "tooltip": "Copier la demande",
                },
            ],
        },
    )


class DemandesRepartitionSmartView(DemandeEqptSmartView):
    class Meta:
        help_text = _(
            "On retrouve dans ce tableau toutes les demandes dont la répartition n'est pas encore faite."
            " La répartition consiste à affecter à chaque demande un programme, un domaine et un expert."
        )

        def base_filter(self, view_params):  # noqa
            return (
                [
                    (Q(programme__isnull=True) | Q(domaine__isnull=True) | Q(expert_metier__isnull=True))
                    & (Q(gel__isnull=True) | Q(gel=False))
                ],
                # Il faut (juste) que l'utilisateur soit dispatcheur...
                {'calendrier__dispatcher': view_params['user']},
            )

        columns = (
            'num_dmd',
            'code',
            'state_code',
            'roles',
            'calendrier',
            'campagne_redirect',
            'redacteur_nom',
            'pole_nom',
            'uf_code',
            'uf_nom',
            'quantite',
            'libelle',
            'cause',
            'materiel_existant',
            'nom_projet',
            'priorite',
            'referent',
            'prix_unitaire',
            'argumentaire_detaille',
            'avis_cadre_sup',
            'commentaire_cadre_sup',
            'decision_validateur',
            'decision_soumission',
            'documents_sf',
            'dispatcher_note',
            'programme',
            'domaine',
            'expert_metier',
            'commentaire_biomed',
            'avis_biomed',
            'tools',
        )

        # columns__remove = (
        #     'commentaire_biomed',
        #     'avis_biomed',
        #     'soumis_a_avis',
        #     'prix_unitaire_conditional',
        #     'montant_arbitrage',
        #     'arbitrage_commission',
        #     'commentaire_provisoire_commission',
        #     'commentaire_definitif_commission',
        #     'quantite_validee_conditional',  # hidden
        #     'montant_qte_validee',
        #     'montant_valide_conditional',
        #     'montant_final',
        #     'montant_consomme',
        #     'gel',
        # )
        selectable_columns__remove = (
            'commentaire_biomed',
            'avis_biomed',
            'prix_unitaire_conditional',
            'arbitrage_commission',
            'commentaire_provisoire_commission',
            'commentaire_definitif_commission',
            'quantite_validee_conditional',  # hidden
            'montant_valide_conditional',
            'arbitrage',
            'gel',
        )
        user_filters__update = {
            'programme': {'type': 'select'},
            'domaine': {'type': 'select'},
            'expert_metier': {'type': 'select'},
            # 'avis_biomed': {'type': 'select'},
            # 'arbitrage_commission': {'type': 'select'},
            # 'gel': {'type': 'select'},
        }
        exports = {
            'xlsx': {
                'engine': 'xlsx',
                'label': 'Microsoft Excel 2003+',
                'filename': "Demandes en cours.xlsx",
            }
        }
        current_row_manager = False

    # Maintenant les colonnes créées 'manuellement' (déclarées)
    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'dem:request-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir la demande"),
                },
            ],
        },
    )


class DemandesArchiveesExpertSmartView(DemandesArchiveesSmartView):
    class Meta:
        help_text = _(
            "Ce tableau reprend toutes les demandes archivées : Les demandes refusées <b>et</b>"
            " les demandes acceptées."
            " Vous pouvez renouveler une demande refusée en cliquant sur l'icône &laquo;&nbsp;copier&nbsp;&raquo;"
            " dans la dernière colonne du tableau"
        )
        # columns__add = ('commentaire_provisoire_commission',)
        # selectable_columns__add = ('commentaire_provisoire_commission',)

        def base_filter(self, params):  # NOQA
            return Q(gel=True)

        row_styler = {
            'fieldname': 'arbitrage',
            'styles': {
                False: ("background:#fcc", "Demande non validée"),
                True: ("background:#cfc", "Demande validée"),
            },
        }

        # Cette redéfinition des filtres ne sert qu'à reforcer le calcul lors de l'héritage pour obliger la SmartView
        # à prendre en compte la modification de row_styler dans le filtre (le '__STYLES__' n'est pas dynamique :-( )
        user_filters__update = {
            'state_code': {
                'type': 'select',
                'choices': '__STYLES__',
                'position': 'bar',
            },
            'programme': {
                'type': 'select',
            },
        }


class DemandesExpertiseSmartView(DemandeEqptSmartView):
    class Meta:
        help_text = _(
            "On retrouve dans ce tableau toutes les demandes dont l'expertise n'est pas encore faite."
            " L'expertise consiste à évaluer la pertinence technique d'une demande, à évaluer le prix"
            " (ou à le déterminer s'il n'a pas été donné par le demandeur puis à donner un avis."
            " Une demande est considérée comme 'expertisée' une fois qu'elle a un avis"
            " (favorable ou défavorable) de l'expert désigné <b>et</b> un prix."
        )
        columns__remove = (
            'gel',
            'arbitrage_commission',
            'commentaire_provisoire_commission',
            'commentaire_definitif_commission',
            'quantite_validee_conditional',
            'quantite_validee',
            # 'montant_valide_conditional',
            # 'montant_valide',
            'arbitrage',
        )
        selectable_columns__remove = (
            'arbitrage_commission',
            'commentaire_provisoire_commission',
            'commentaire_definitif_commission',
            'quantite_validee_conditional',
            # 'quantite_validee',
            'montant_valide_conditional',
            # 'montant_valide',
            # 'montant_unitaire_expert_metier',
            'arbitrage',
            'gel',
        )
        columns__add = (
            'workflow_alert',
            # 'valide_flag',
            # 'montant_final', # test
        )
        settings = {
            'montant_valide_conditional': {
                'hidden': True,
            },
        }
        user_filters__update = {
            'programme': {'type': 'select'},
            'domaine': {'type': 'select'},
            'expert_metier': {'type': 'select'},
            'avis_biomed': {'type': 'select'},
        }
        exports = {
            'xlsx': {
                'engine': 'xlsx',
                'label': 'Microsoft Excel 2003+',
                'filename': "Demandes en cours.xlsx",
            }
        }
        base_filter = [
            # Demandes non validées
            Q(gel=False) | Q(gel__isnull=True),
            # Qui a un expert nommé
            Q(expert_metier__isnull=False),
            # Qui n'a pas d'avis défavorable du chef de pôle ou du directeur
            Q(decision_validateur=True) | Q(decision_validateur__isnull=True),
            # Qui reste à expertise
            (Q(prix_unitaire__isnull=True) & Q(montant_unitaire_expert_metier__isnull=True)) | Q(avis_biomed__isnull=True),
            ~Q(discipline_dmd__code='TX'),  # Exclut les demandes de travaux
        ]
        current_row_manager = False

    # Maintenant les colonnes créées 'manuellement' (déclarées)
    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'dem:request-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir la demande"),
                },
            ],
        },
    )


class DemandesEnCoursExpSmartView(DemandeEqptSmartView):
    class Meta:
        user_filters__update = {
            'programme': {
                'type': 'select',
                'choices': {
                    'fieldname': 'programme',
                    'label': Concat(F('programme__code'), Value(' - '), F('programme__nom')),
                    'sort': F('programme__code'),
                },
            },
            'domaine': {'type': 'select'},
            'expert_metier': {'type': 'select'},
            'avis_biomed': {'type': 'select'},
            'arbitrage_commission': {'type': 'select'},
        }
        exports = {
            'xlsx': {
                'engine': 'xlsx',
                'label': 'Microsoft Excel 2003+',
                'filename': "Demandes en cours.xlsx",
            }
        }

        def base_filter(self, view_params: dict):  # NOQA : Unused parameter
            return ~Q(calendrier__code__contains='TVX') & (Q(gel__isnull=True) | Q(gel=False))


class DemandesEnCoursTable(SmartTable):
    smart_view_class = DemandeEqptSmartView
    columns = (
        'num_dmd',
        'code',
        'calendrier',
        'campagne_redirect',
        'roles',
        'state_code',
        'redacteur',
        'contact',
        'dect_contact',
        'discipline_dmd',
        'date_premiere_demande',
        'uf',
        'pole_nom',
        'uf_code',
        'uf_nom',
        'redacteur_nom',
        'priorite',
        'nom_projet',
        'libelle',
        'description',
        'localisation',
        'cause',
        'it_caracteristiques_minimales',
        'it_a_installer',
        'referent',
        'materiel_existant',
        'quantite',
        'prix_unitaire',
        'montant_initial',
        'it_cout_formation',
        'impact_travaux',
        'impact_informatique',
        'consommables_eventuels',
        'argumentaire_detaille',
        'documents_sf',
        'avis_cadre_sup',
        'commentaire_cadre_sup',
        'decision_validateur',
        'decision_soumission',
        'programme',
        'domaine',
        'expert_metier',
        'prix_unitaire_conditional',
        'arg_interet_medical',
        'arg_commentaire_im',
        'arg_oblig_reglementaire',
        'arg_commentaire_or',
        'arg_recommandations',
        'arg_commentaire_r',
        'arg_confort_patient',
        'arg_commentaire_cp',
        'arg_confort_perso_ergo',
        'arg_commentaire_pe',
        'arg_notoriete',
        'arg_commentaire_n',
        'arg_projet_chu_pole',
        'arg_commentaire_pcp',
        'arg_gain_financier',
        'arg_commentaire_gf',
        'arg_mutualisation',
        'arg_commentaire_m',
        'arg_innovation_recherche',
        'arg_commentaire_ir',
        'autre_argumentaire',
        'commentaire_biomed',
        'avis_biomed',
        'montant_arbitrage',
        'arbitrage_commission',
        'commentaire_provisoire_commission',
        'commentaire_definitif_commission',
        'quantite_validee_conditional',  # hidden
        'montant_qte_validee',
        'montant_valide_conditional',
        'montant_final',
        'montant_consomme',
        'arbitrage',
        'gel',
        'tools',
    )

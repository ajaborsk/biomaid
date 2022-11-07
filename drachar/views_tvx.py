#  Copyright (c)

#
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
from django.db.models import F, Value, Q, Case, When
from django.db.models.functions import Concat
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.db_utils import filter_choices_from_column_values
from dem.apps import DRACHAR_DELAI_DEMANDE_TERMINEE
from dem.utils import roles_demandes_possibles
from dem.views_tvx import DemTvxSmartView
from drachar.models import Previsionnel
from drachar.smart_views import PrevTvxSmartView
from drachar.views21 import DracharView
from smart_view.smart_fields import ComputedSmartField
from smart_view.smart_page import SmartPage
from smart_view.views import DoubleSmartViewMixin


class PrevTvxSmartView21(PrevTvxSmartView):
    class Meta:
        form_layout = (
            'form',
            {},
            (
                ('title', "Titre du formulaire"),
                ('row', ('$num_dmd$',)),
                (
                    'section',
                    {},
                    (
                        ('title', "Titre de la section"),
                        ('row', ('$num_dmd$', '$dmd_quantite$')),
                        ('row', ('$dmd_libelle$', '$commentaire$')),
                        ('sep',),
                    ),
                ),
            ),
        )
        user_filters__update = {
            'domaine': {
                'type': 'select',
                'choices': filter_choices_from_column_values(
                    Previsionnel,
                    'num_dmd__domaine',
                    label_expr=Concat(
                        F('num_dmd__domaine__code'),
                        Value(' - '),
                        F('num_dmd__domaine__nom'),
                    ),
                    order_by='num_dmd__domaine__code',
                ),
            },
        }
        views = 'table'


class PrevTvxUtilisateursSmartView(PrevTvxSmartView):
    class Meta:
        columns = (
            # 'num_dmd_pk',
            'demande_code',
            'discipline_dmd',
            'code_uf',
            'nom_uf',
            'nom_pole',
            'dmd_quantite',
            'dmd_libelle',
            'budget',
            'expert',
            'suivi_besoin',
            'suivi_etude',
            'suivi_autorisation',
            'suivi_preparation',
            'suivi_execution',
            'suivi_reception',
            'suivi_mes',
            'commentaire_public',
            'date_estimative_mes',
            'roles',
        )
        selectable_columns = (
            # 'num_dmd_pk',
            'code_uf',
            'nom_uf',
            'nom_pole',
            'dmd_quantite',
            'dmd_libelle',
            'budget',
            'expert',
            'suivi_besoin',
            'suivi_etude',
            'suivi_autorisation',
            'suivi_preparation',
            'suivi_execution',
            'suivi_reception',
            'suivi_mes',
            'commentaire_public',
            'date_estimative_mes',
        )
        settings = {
            'commentaire_public': {
                'title': _("Commentaire"),
                'help_text': _("Commentaire du chargé d'opération"),
            },
            'suivi_besoin': {
                'title': _("Programme"),
                'help_text': _("__### Commentaire___"),
                'formatter': "'suivi_couleur'",
            },
            'suivi_etude': {
                'help_text': _("__### Commentaire___"),
                'formatter': "'suivi_couleur'",
            },
            'suivi_autorisation': {
                'help_text': _("__### Commentaire___"),
                'formatter': "'suivi_couleur'",
            },
            'suivi_preparation': {
                'help_text': _("__### Commentaire___"),
                'formatter': "'suivi_couleur'",
            },
            'suivi_execution': {
                'help_text': _("__### Commentaire___"),
                'formatter': "'suivi_couleur'",
            },
            'suivi_reception': {
                'help_text': _("__### Commentaire___"),
                'formatter': "'suivi_couleur'",
            },
            'suivi_mes': {
                'help_text': _("__### Commentaire___"),
                'formatter': "'suivi_couleur'",
            },
            'date_estimative_mes': {
                'title': "Estimation date Mise en Service",
                'datetime_format': "%Q [trim.] %Y",
            },
        }
        current_row_manager = None
        row_styler = None
        exports = ()
        help_text = _(
            "Vous trouverez dans ce tableau toutes les demandes de travaux qui ont été validées"
            " et pour lesquelles les travaux sont en cours (et jusqu'à trois mois après la fin des travaux). "
            "Pour chaque demande, vous pouvez voir qui est en charge"
            " du suivi des travaux, l'état d'avancement des principales étapes"
            " et la date prévisionnelle de mise en service."
        )

        # Filtre de base : Uniquement le prévisionnel associé
        # aux demandes sur les UF pour lesquelles je peux faire une demande...
        def base_filter(self, view_params: dict):  # NOQA
            # Liste des rôles pour lesquels je peux faire une demande
            # sur une UF (objet qui devrait être partagé sur l'ensemble
            #  de l'application _dem_
            tmp_scope = roles_demandes_possibles(view_params['user'])
            return (
                (
                    Q(num_dmd__uf__in=tmp_scope.values('uf'))
                    | Q(num_dmd__uf__service__in=tmp_scope.values('service'))
                    | Q(num_dmd__uf__centre_responsabilite__in=tmp_scope.values('centre_responsabilite'))
                    | Q(num_dmd__uf__pole__in=tmp_scope.values('pole'))
                    | Q(num_dmd__uf__site__in=tmp_scope.values('site'))
                    | Q(num_dmd__uf__etablissement__in=tmp_scope.values('etablissement'))
                )
                & (
                    # Uniquement les demandes de travaux
                    Q(programme__discipline__code='TX')
                    # Uniquement les demandes qui ne sont pas terminées depuis 'longtemps'
                    & (~Q(suivi_mes__startswith='1-') | Q(date_modification__gte=timezone.now() - DRACHAR_DELAI_DEMANDE_TERMINEE))
                ),
            )

    num_dmd_pk = (
        ComputedSmartField,
        {
            'title': 'Numéro',
            'data': F('num_dmd__pk'),
        },
    )


class SuiviTravaux(SmartPage):
    application = 'drachar'
    name = 'suivi-travaux'
    permissions = ('AMAR', 'DRP', 'CAP', 'CAD', 'CHS', 'CSP', 'ACHP', 'CHP', 'COP', 'DIR', 'EXP')
    smart_view_class = PrevTvxUtilisateursSmartView
    title = "Suivi des demandes de travaux acceptées"
    smart_modes = {
        None: {'view': 'list'},
    }


class SingleDemandeTvxSmartView(DemTvxSmartView):
    class Meta:
        columns = (
            'num_dmd',
            'roles',
            # 'state_code',
            # 'date_premiere_demande',
            'pole_nom',
            'uf_code',
            'uf_nom',
            'redacteur_nom',
            'priorite',
            # 'nom_projet',
            'libelle',
            # 'cause',
            # 'materiel_existant',
            'referent',
            # 'quantite',
            # 'prix_unitaire',
            # 'montant',
            # 'impact_travaux',
            # 'impact_informatique',
            'argumentaire_detaille',
            # 'documents_joints',
            'documents_sf',
            'avis_cadre_sup',
            'commentaire_cadre_sup',
            'decision_validateur',
            'decision_soumission',
            'programme',
            # 'domaine',
            'expert_metier',
            # 'soumis_a_avis',
            'montant_unitaire_expert_metier',
            # 'montant_total_expert_metier',
            'commentaire_biomed',
            'avis_biomed',
            'montant_arbitrage',
            'arbitrage_commission',
            # 'commentaire_provisoire_commission',
            'commentaire_definitif_commission',
            # 'quantite_validee',
            # 'qte',  # Quantité validée OU quantité initiale
            'enveloppe_allouee',
            # 'gel',
        )
        # form_layout = (
        #     'form',
        #     {},
        #     (
        #         ('title', "Titre du formulaire"),
        #         ('row', ('$num_dmd$',)),
        #         (
        #             'section',
        #             {},
        #             (
        #                 ('title', "Titre de la section"),
        #                 ('row', ('$priorite$', '$quantite$')),
        #                 ('row', ('$libelle$', '$nom_projet$')),
        #                 ('sep',),
        #             ),
        #         ),
        #     ),
        # )
        views = ('table',)

    qte = (
        ComputedSmartField,
        {
            'title': 'Qté validée',
            'format': 'integer',
            'data': Case(
                When(quantite_validee__isnull=False, then=F('quantite_validee')),
                default=F('quantite'),
            ),
        },
    )


class PrevisionnelTvxSmartView21(PrevTvxSmartView):
    class Meta:
        form_layout = (
            'form',
            {},
            (
                ('title', "Titre du formulaire"),
                ('row', ('$num_dmd$',)),
                (
                    'section',
                    {},
                    (
                        ('title', "Titre de la section"),
                        ('row', ('$num_dmd$', '$dmd_quantite$')),
                        ('row', ('$dmd_libelle$', '$commentaire$')),
                        ('sep',),
                    ),
                ),
            ),
        )
        user_filters__update = {
            'domaine': {
                'type': 'select',
                'choices': filter_choices_from_column_values(
                    Previsionnel,
                    'num_dmd__domaine',
                    label_expr=Concat(
                        F('num_dmd__domaine__code'),
                        Value(' - '),
                        F('num_dmd__domaine__nom'),
                    ),
                    order_by='num_dmd__domaine__code',
                ),
            },
        }
        views = 'table'


class PrevisionnelTvxView(DoubleSmartViewMixin, DracharView):
    main_smart_view_class = PrevisionnelTvxSmartView21
    name = 'previsionnel-tvx'
    main_field_name = 'num_dmd'
    field_smart_view_class = SingleDemandeTvxSmartView
    title = _("Suivi exécution des travaux")

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
from django.db.models import Q, F, Value, Case, When, TextField, ExpressionWrapper
from django.db.models.functions import Concat
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from common import config
from common.base_views import BiomAidViewMixin
from common.models import Discipline, Programme, UserUfRole, Uf
from dem.models import Demande, Arbitrage
from dem.smart_views import DemandeSmartView
from dem.utils import roles_demandes_possibles, user_campagnes
from smart_view.smart_fields import ComputedSmartField, ToolsSmartField
from smart_view.smart_page import SmartPage


class DemTvxSmartView(DemandeSmartView):
    class Meta:
        fields__add = (
            'montant_qte_validee',
            'montant_arbitrage',
            'localisation',
            'tvx_contrainte_lib',
            'tvx_contrainte_alib',
            'tvx_contrainte_lar',
            'tvx_contrainte_autre',
            'tvx_contrainte',
        )
        selectable_columns = (
            'calendrier',
            # 'roles',
            # 'tvx_state',
            # 'state_code',
            # 'discipline_dmd',
            # 'couts_complementaires',
            # 'num_dmd',
            'code',
            'date',
            'uf',
            'service_view',
            'pole_view',
            # 'redacteur',
            'redacteur_view',
            'referent',
            'libelle',
            # 'nom_projet',
            'tvx_batiment',
            'tvx_etage',
            'localisation',
            'description',
            'tvx_contraintes_view',
            'tvx_priorite',
            'argumentaire_detaille_tvx',
            'documents_sf',
            'programme',
            'expert_metier',
            'tvx_eval_devact',
            'tvx_eval_contin',
            'tvx_eval_confort',
            'tvx_eval_securite',
            'tvx_eval_qvt',
            'tvx_eval_synthese',
            'commentaire_biomed',
            # 'montant_unitaire_expert_metier',
            'avis_biomed',
            'prix_unitaire_conditional',
            'montant_arbitrage',
            # 'quantite_validee_conditional',  # hidden
            # 'montant_qte_validee',
            'montant_valide_conditional',
            # 'montant_final',
            # 'montant_consomme',
            'arbitrage_commission',
            'commentaire_definitif_commission',
            'gel',
        )
        columns = (
            'calendrier',
            'roles',
            'tvx_state',
            # 'state_code',
            'discipline_dmd',
            'nature',
            'couts_complementaires',
            'num_dmd',
            'code',
            'date',
            'uf',
            'service_view',
            'pole_view',
            'redacteur',
            'redacteur_view',
            'referent',
            'libelle',
            'nom_projet',
            'tvx_batiment',
            'tvx_etage',
            'localisation',
            'description',
            'tvx_contrainte_lib',
            'tvx_contrainte_alib',
            'tvx_contrainte_lar',
            'tvx_contrainte_autre',
            'tvx_contrainte',
            'tvx_contraintes_view',
            'tvx_priorite',
            'tvx_arg_normes',
            'tvx_arg_normes_comment',
            'tvx_arg_reorg',
            'tvx_arg_reorg_comment',
            'tvx_arg_devact',
            'tvx_arg_devact_comment',
            'tvx_arg_eqpt',
            'tvx_arg_eqpt_comment',
            'tvx_arg_qvt',
            'tvx_arg_qvt_comment',
            'tvx_arg_securite',
            'tvx_arg_securite_comment',
            'tvx_arg_vetustes',
            'tvx_arg_vetustes_comment',
            'autre_argumentaire',
            'argumentaire_detaille_tvx',
            'documents_sf',
            'decision_validateur',
            'decision_soumission',
            'programme',
            'expert_metier',
            'tvx_eval_devact',
            'tvx_eval_contin',
            'tvx_eval_confort',
            'tvx_eval_securite',
            'tvx_eval_qvt',
            'tvx_eval_synthese',
            'commentaire_biomed',
            'montant_unitaire_expert_metier',
            'avis_biomed',
            'prix_unitaire_conditional',
            'montant_arbitrage',
            'quantite_validee_conditional',  # hidden
            'montant_qte_validee',
            'montant_valide_conditional',
            'montant_final',
            'montant_consomme',
            'arbitrage_commission',
            'commentaire_definitif_commission',
            'gel',
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
            'demande_contains': {
                'type': 'contains',
                'fieldnames': [
                    'referent',
                    'contact',
                    'libelle',
                    'nom_projet',
                    'description',
                    'commentaire_cadre_sup',
                    'decision_soumission',
                    'commentaire_biomed',
                    'commentaire_definitif_commission',
                    'autre_argumentaire',
                    'montant_arbitrage',
                    'localisation',
                    'tvx_contrainte_lib',
                    'tvx_contrainte_alib',
                    'tvx_contrainte_lar',
                    'tvx_contrainte_autre',
                    'tvx_contrainte',
                ],
                'label': _('Demande contient'),
            },
        }
        settings = {
            'roles': {
                # For debug only
                'title': _("Rôles (debug)"),
                'hidden': not (hasattr(config.settings, 'SMARTVIEW_DEBUG') and config.settings.SMARTVIEW_DEBUG),
            },
            'calendrier': {
                'form.hidden': True,
                'title': _("Campagne"),
                'choices': lambda view_params: [(campagne.pk, campagne.nom) for campagne in user_campagnes(view_params, tvx=True)],
            },
            'redacteur': {
                'hidden': True,
                'initial': lambda params: params['user'].pk,
            },
            'discipline_dmd': {
                'hidden': True,
                'initial': lambda params: Discipline.objects.filter(code='TX')[0],
            },
            'nature': {
                'hidden': True,
                'initial': lambda params: 'TX',
            },
            'couts_complementaires': {
                'hidden': True,
                'initial': False,
            },
            'num_dmd': {
                'hidden': True,
            },
            'code': {
                'title': _("Numéro"),
                'initial.form': None,
            },
            'date': {
                'datetime_format': "%d/%m/%Y",
            },
            'libelle': {
                'title': _("Travaux demandés"),
                'form.title': _("Travaux demandés"),
                'help_text': _("En quelques mots (ce sera le titre de la demande)"),
            },
            'nom_projet': {
                'title': _("Sera caché"),
                'smart-copy': 'libelle',
                'hidden': True,
            },
            'tvx_contrainte_lib': {
                'table.hidden': True,
            },
            'tvx_contrainte_alib': {
                'table.hidden': True,
            },
            'tvx_contrainte_lar': {
                'table.hidden': True,
            },
            'tvx_contrainte_autre': {
                'table.hidden': True,
                'form.title': _("Autre contrainte (précisez ci-contre)"),
            },
            'tvx_contrainte': {
                'table.hidden': True,
            },
            'tvx_batiment': {
                'title': _("Bâtiment"),
                'form.title': _("Bâtiment concerné"),
                'choices': dict({None: '-- Indéfini --'}, **{p[0]: p[0] + ' - ' + p[1] for p in Demande.TVX_BATIMENT_CHOICE}),
                # null & blank are True in the model since this field isn't used for equipments
                # but this field is needed for this SmartView
                'blank': False,
            },
            'tvx_etage': {
                'title': _("Etage"),
                'form.title': _("Etage concerné"),
                'choices': dict({None: '-- Indéfini --'}, **{p[0]: p[0] + ' - ' + p[1] for p in Demande.TVX_ETAGE_CHOICE}),
                # null & blank are True in the model since this field isn't used for equipments
                # but this field is needed for this SmartView
                'blank': False,
            },
            'tvx_priorite': {
                'choices': dict({None: '-- Indéfinie --'}, **{p[0]: p[0] + ' - ' + p[1] for p in Demande.TVX_PRIORITE}),
                # null & blank are True in the model since this field isn't used for equipments
                # but this field is needed for this SmartView
                'blank': False,
            },
            'description': {
                'title': _("Description détaillée"),
                'help_text': _(
                    "Décrivez le plus précisément possible les travaux à effectuer."
                    " Vous pouvez joindre à la demande des documents, plans, schémas, etc."
                ),
            },
            'tvx_arg_normes': {
                'table.hidden': True,
            },
            'tvx_arg_normes_comment': {
                'show-if': 'tvx_arg_normes',
                'title': _("Détaillez"),
                'table.hidden': True,
            },
            'tvx_arg_reorg': {
                'table.hidden': True,
            },
            'tvx_arg_reorg_comment': {
                'show-if': 'tvx_arg_reorg',
                'title': _("Détaillez"),
                'table.hidden': True,
            },
            'tvx_arg_devact': {
                'table.hidden': True,
            },
            'tvx_arg_devact_comment': {
                'show-if': 'tvx_arg_devact',
                'title': _("Détaillez"),
                'table.hidden': True,
            },
            'tvx_arg_eqpt': {
                'table.hidden': True,
            },
            'tvx_arg_eqpt_comment': {
                'show-if': 'tvx_arg_eqpt',
                'title': _("Détaillez"),
                'table.hidden': True,
            },
            'tvx_arg_qvt': {
                'table.hidden': True,
            },
            'tvx_arg_qvt_comment': {
                'show-if': 'tvx_arg_qvt',
                'title': _("Détaillez"),
                'table.hidden': True,
            },
            'tvx_arg_securite': {
                'table.hidden': True,
            },
            'tvx_arg_securite_comment': {
                'show-if': 'tvx_arg_securite',
                'title': _("Détaillez"),
                'table.hidden': True,
            },
            'tvx_arg_vetustes': {
                'table.hidden': True,
            },
            'tvx_arg_vetustes_comment': {
                'show-if': 'tvx_arg_vetustes',
                'title': _("Détaillez"),
                'table.hidden': True,
            },
            'autre_argumentaire': {
                'format': 'text',
                'table.hidden': True,
                'help_text': "Précisez quels autres arguments peuvent justifier ces travaux",
            },
            'programme': {
                'title': _("Intervenants"),
                'autocomplete': True,
                'choices': lambda view_params: tuple(Programme.objects.filter(discipline__code='TX').values_list('pk', 'nom')),
            },
            # Limitons le choix pour l'expert métier aux personnes qui ont au moins un rôle d'expert
            # L'utilisation d'une fonction (ici une fonction lambda) permet de faire cette évaluation à chaque instanciation
            # (ouverture de la page) et non pas seulement au lancement de Django
            'expert_metier': {
                'format': 'choice',
                'autocomplete': True,
                'editor': 'autocomplete',
                'choices': lambda view_params=None: tuple(
                    UserUfRole.objects.order_by()
                    .filter(role_code='EXP', discipline__code='TX')
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
            'tvx_eval_devact': {
                'format': 'choice',
                'choices': {i: str(i) for i in range(1, 6)},
            },
            'tvx_eval_contin': {
                'format': 'choice',
                'choices': {i: str(i) for i in range(1, 6)},
            },
            'tvx_eval_confort': {
                'format': 'choice',
                'choices': {i: str(i) for i in range(1, 6)},
            },
            'tvx_eval_securite': {
                'format': 'choice',
                'choices': {i: str(i) for i in range(1, 6)},
            },
            'tvx_eval_qvt': {
                'format': 'choice',
                'choices': {i: str(i) for i in range(1, 6)},
            },
            'avis_biomed': {
                'title': _("Avis expert"),
            },
            'montant_unitaire_expert_metier': {
                'hidden': True,
            },
            'prix_unitaire_conditional': {
                'hidden': True,
            },
            'montant_arbitrage': {
                'hidden': True,
            },
            'quantite_validee_conditional': {
                'hidden': True,
            },  # hidden
            'montant_qte_validee': {
                'hidden': True,
            },
            'montant_valide_conditional': {
                'hidden': True,
            },
            'montant_final': {
                'hidden': True,
            },
            'montant_consomme': {
                'hidden': True,
            },
            'arbitrage_commission': {
                'title': _("Arbitrage"),
                'width': 100,
                'choices': lambda view_params: Arbitrage.objects.filter(
                    Q(cloture__isnull=True) | Q(cloture__gt=timezone.now()),
                    discipline__code='TX',
                )
                .annotate(label=Concat(F('code'), Value(' - '), F('nom')))
                .values_list('pk', 'label'),
            },
            'gel': {
                'hidden': True,
            },
        }

        def base_filter(self, view_params: dict):
            # Liste des rôles pour lesquels je peux faire une demande sur une UF
            tmp_scope = roles_demandes_possibles(view_params['user'])
            return (
                (
                    Q(discipline_dmd__code='TX'),
                    Q(uf__in=tmp_scope.values('uf'))
                    | Q(uf__service__in=tmp_scope.values('service'))
                    | Q(uf__centre_responsabilite__in=tmp_scope.values('centre_responsabilite'))
                    | Q(uf__pole__in=tmp_scope.values('pole'))
                    | Q(uf__site__in=tmp_scope.values('site'))
                    | Q(uf__etablissement__in=tmp_scope.values('etablissement')),
                ),
                {},
            )

        form_layout = """
        # demande de travaux courants {{ instance.code }}
            <calendrier>
            <discipline_dmd> <nature>
            <couts_complementaires>
            <nom_projet>
            <redacteur>
            # Demandeur
                <referent> <redacteur_view>
            # Projet
                <tvx_batiment> <tvx_etage>
                <uf> <localisation>
                <service_view> <pole_view>
                <libelle-+---->
                <description+--->
                # Contraintes dans la zone
                    <tvx_contrainte_lib----> <tvx_contrainte-+--->
                    <tvx_contrainte_alib---> <tvx_contrainte-+--->
                    <tvx_contrainte_lar----> <tvx_contrainte-+--->
                    <tvx_contrainte_autre--> <tvx_contrainte-+--->
            # Argumentaire
                <tvx_priorite--+--+--+-->
                <tvx_arg_reorg> <tvx_arg_reorg_comment--+--+-->
                <tvx_arg_devact> <tvx_arg_devact_comment--+--+-->
                <tvx_arg_securite> <tvx_arg_securite_comment--+--+-->
                <tvx_arg_qvt> <tvx_arg_qvt_comment--+--+-->
                <tvx_arg_vetustes> <tvx_arg_vetustes_comment--+--+-->
                <tvx_arg_eqpt> <tvx_arg_eqpt_comment--+--+-->
                <tvx_arg_normes> <tvx_arg_normes_comment--+--+-->
                <autre_argumentaire--+---+--+-->
            # Documents joints
                <--documents_sf-+--+--+->
        """
        exports = {
            'xlsx': {
                'engine': 'xlsx',
                'label': 'Microsoft Excel 2003+',
                'filename': "Demandes de travaux.xlsx",
            }
        }

    # Workflow des demandes de travaux (à l'envers) :
    # Dans tous les cas, il faut la discipline 'TX' ; sinon, ce n'est pas une demande de travaux...
    # L'état est toujours caché, sauf lorsqu'on est en mode DEBUG de Django
    #
    # Etat archivé / validé : gel = True ET arbitrage_commission__valeur = True
    #   L'arbitre peut le dégeler
    # Etat archivé / refusé : gel = True ET arbitrage_commission__valeur = False
    #   L'arbitre peut le dégeler
    # Etat archivable_v : gel = False
    # (acceptable)              ET arbitrage_commission__valeur = True
    # (validable)               ET montant_valide_value__isnull = False
    #                           ET expert__isnull = False
    # Etat archivable_r : gel = False
    # (refusable)               ET arbitrage_commission__valeur = False
    # Etat arbitrable :
    tvx_state = (
        ComputedSmartField,
        {
            'special': 'state',
            'title': _("Etat (debug)"),
            # For debug only
            'hidden': not (hasattr(config.settings, 'SMARTVIEW_DEBUG') and config.settings.SMARTVIEW_DEBUG),
            'data': Case(
                When(
                    discipline_dmd__code='TX',
                    then=Case(
                        When(
                            programme__isnull=False,
                            expert_metier__isnull=False,
                            programme__enveloppe__gte=1,
                            decision_validateur__isnull=True,
                            then=Case(
                                When(
                                    gel=True,
                                    arbitrage_commission__valeur=True,
                                    then=Value('TVX_VALIDE'),
                                ),
                                When(
                                    gel=True,
                                    arbitrage_commission__valeur=False,
                                    then=Value('TVX_REFUSE'),
                                ),
                                When(
                                    decision_validateur__isnull=False,
                                    then=Value('TVX_APPROB'),  # demande avec avis approbation (par le chef de pôle / directeur)
                                ),
                                When(
                                    avis_biomed__isnull=True,
                                    then=Value('TVX_ANA'),  # demande à analyser par un expert
                                ),
                                default=Value('TVX_ARB'),  # Demande à arbitrer
                            ),
                        ),
                        default=Value('TVX_NEW'),  # Demande à approuver
                    ),
                ),
                default=Value('TVX_OTHER'),  # Pas une demande de travaux
            ),
            'depends': [
                'discipline_dmd',
                'programme',
                'expert_metier',
                'avis_biomed',
            ],
        },
    )

    redacteur_view = (
        ComputedSmartField,
        {
            'title': 'Rédacteur',
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

    argumentaire_detaille_tvx = (
        ComputedSmartField,
        {
            'title': _("Argumentaire"),
            'format': 'html',
            'width': 500,
            'min_width': 100,
            'depends': [
                'tvx_arg_normes',
                'tvx_arg_normes_comment',
                'tvx_arg_reorg',
                'tvx_arg_reorg_comment',
                'tvx_arg_devact',
                'tvx_arg_devact_comment',
                'tvx_arg_eqpt',
                'tvx_arg_eqpt_comment',
                'tvx_arg_qvt',
                'tvx_arg_qvt_comment',
                'tvx_arg_securite',
                'tvx_arg_securite_comment',
                'tvx_arg_vetustes',
                'tvx_arg_vetustes_comment',
                'autre_argumentaire',
            ],
            'data': Concat(
                Value('<p>'),
                Case(
                    When(
                        tvx_arg_reorg=True,
                        then=Concat(
                            Value("<b>Réorganisation des activités :</b>&nbsp;"),
                            F('tvx_arg_reorg_comment'),
                            Value("<br>"),
                            output_field=TextField(),
                        ),
                    ),
                ),
                Case(
                    When(
                        tvx_arg_devact=True,
                        then=Concat(
                            Value("<b>Développement de l'activité :</b>&nbsp;"),
                            F('tvx_arg_devact_comment'),
                            Value("<br>"),
                            output_field=TextField(),
                        ),
                    ),
                ),
                Case(
                    When(
                        tvx_arg_securite=True,
                        then=Concat(
                            Value("<b>Confort et/ou sécurité des patients :</b>&nbsp;"),
                            F('tvx_arg_securite_comment'),
                            Value("<br>"),
                            output_field=TextField(),
                        ),
                    ),
                ),
                Case(
                    When(
                        tvx_arg_qvt=True,
                        then=Concat(
                            Value("<b>Confort et/ou sécurité des personnels :</b>&nbsp;"),
                            F('tvx_arg_qvt_comment'),
                            Value("<br>"),
                            output_field=TextField(),
                        ),
                    ),
                ),
                Case(
                    When(
                        tvx_arg_vetustes=True,
                        then=Concat(
                            Value("<b>Locaux vétustes :</b>&nbsp;"),
                            F('tvx_arg_vetustes_comment'),
                            Value("<br>"),
                            output_field=TextField(),
                        ),
                    ),
                ),
                Case(
                    When(
                        tvx_arg_eqpt=True,
                        then=Concat(
                            Value("<b>Arrivée d'un équipement :</b>&nbsp;"),
                            F('tvx_arg_eqpt_comment'),
                            Value("<br>"),
                            output_field=TextField(),
                        ),
                    ),
                ),
                Case(
                    When(
                        tvx_arg_normes=True,
                        then=Concat(
                            Value("<b>Remise aux normes :</b>&nbsp;"),
                            F('tvx_arg_normes_comment'),
                            Value("<br>"),
                            output_field=TextField(),
                        ),
                    ),
                ),
                Case(
                    When(
                        autre_argumentaire__gt=' ',
                        then=Concat(
                            Value("<b>Autre argumentaire :</b>&nbsp;"),
                            F('autre_argumentaire'),
                            Value("<br>"),
                            output_field=TextField(),
                        ),
                    ),
                ),
                Value('</p>'),
                output_field=TextField(),
            ),
        },
    )
    tvx_contraintes_view = (
        ComputedSmartField,
        {
            'title': _("Contraintes"),
            'data': Concat(
                Value('<ul>', output_field=TextField()),
                Case(
                    When(
                        tvx_contrainte_lib=True,
                        then=Value(
                            _("<li>Les locaux seront libérés</li>"),
                            output_field=TextField(),
                        ),
                    ),
                ),
                Case(
                    When(
                        tvx_contrainte_alib=True,
                        then=Value(
                            _("<li>Locaux provisoires à trouver</li>"),
                            output_field=TextField(),
                        ),
                    ),
                ),
                Case(
                    When(
                        tvx_contrainte_lar=True,
                        then=Value(
                            _("<li>Les locaux sont à risque</li>"),
                            output_field=TextField(),
                        ),
                    ),
                ),
                Case(
                    When(
                        tvx_contrainte_autre=True,
                        then=Value(
                            _("<li>Une autre contrainte existe</li>"),
                            output_field=TextField(),
                        ),
                    ),
                ),
                Case(
                    When(
                        tvx_contrainte__gt=' ',
                        then=Concat(
                            Value(_("<li>Précisions&nbsp;:&nbsp;")),
                            'tvx_contrainte',
                            Value("</li>"),
                            output_field=TextField(),
                        ),
                    ),
                ),
                Value('</ul>', output_field=TextField()),
                output_field=TextField(),
            ),
            'depends': [
                'tvx_contrainte_lib',
                'tvx_contrainte_alib',
                'tvx_contrainte_lar',
                'tvx_contrainte_autre',
                'tvx_contrainte',
            ],
            'format': 'html',
        },
    )
    tvx_eval_synthese = (
        ComputedSmartField,
        {
            'title': _("Evaluation globale"),
            'data': F('tvx_eval_devact')
            + F('tvx_eval_contin')
            + F('tvx_eval_confort')
            + F('tvx_eval_securite')
            + F('tvx_eval_qvt'),
            'depends': [
                'tvx_eval_devact',
                'tvx_eval_contin',
                'tvx_eval_confort',
                'tvx_eval_securite',
                'tvx_eval_qvt',
            ],
        },
    )
    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'dem:tvx-demande-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir la demande"),
                },
                # {'tool': 'copy', 'url_name': 'dem:tvx-demande-copy', 'url_args': ('${id}',), "tooltip": "Copier la demande"},
                {
                    'tool': 'delete',
                    'url_name': 'dem:tvx-demande-ask-delete',
                    'url_args': ('${id}',),
                    "tooltip": "Supprimer la demande",
                },
            ],
        },
    )


class DemTvxEnCoursSmartView(DemTvxSmartView):
    class Meta:
        columns__remove = (
            'calendrier',
            'programme',
            # 'tvx_eval_devact',
            # 'tvx_eval_contin',
            # 'tvx_eval_confort',
            # 'tvx_eval_securite',
            # 'tvx_eval_qvt',
            # 'montant_unitaire_expert_metier',
            'prix_unitaire_conditional',
            'montant_arbitrage',
            'arbitrage_commission',
            # 'commentaire_provisoire_commission',
            'commentaire_definitif_commission',
            'quantite_validee_conditional',  # hidden
            'montant_qte_validee',
            'montant_valide_conditional',
            'montant_final',
            'montant_consomme',
            'gel',
        )
        columns__add = ('tools',)
        user_filters = {
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
            'demande_contains': {
                'type': 'contains',
                'fieldnames': [
                    'referent',
                    'contact',
                    'libelle',
                    'nom_projet',
                    'description',
                    'commentaire_cadre_sup',
                    'decision_soumission',
                    'commentaire_biomed',
                    'commentaire_definitif_commission',
                    'autre_argumentaire',
                    'montant_arbitrage',
                    'localisation',
                    'tvx_contrainte_lib',
                    'tvx_contrainte_alib',
                    'tvx_contrainte_lar',
                    'tvx_contrainte_autre',
                    'tvx_contrainte',
                ],
                'label': _('Demande contient'),
            },
            'tvx_batiment': {
                'type': 'select',
            },
            'tvx_etage': {
                'type': 'select',
            },
            'tvx_priorite': {
                'type': 'select',
            },
        }

        settings = {
            'tvx_eval_devact': {
                'hidden': True,
            },
            'tvx_eval_contin': {
                'hidden': True,
            },
            'tvx_eval_confort': {
                'hidden': True,
            },
            'tvx_eval_securite': {
                'hidden': True,
            },
            'tvx_eval_qvt': {
                'hidden': True,
            },
        }


class DemTvxApprobSmartView(DemTvxSmartView):
    class Meta:
        def base_filter(self, view_params: dict):
            # Liste des rôles pour lesquels je peux faire une demande sur une UF
            tmp_scope = roles_demandes_possibles(view_params['user'])
            return (
                (
                    Q(discipline_dmd__code='TX'),
                    Q(tvx_state='TVX_NEW'),
                    Q(uf__in=tmp_scope.values('uf'))
                    | Q(uf__service__in=tmp_scope.values('service'))
                    | Q(uf__centre_responsabilite__in=tmp_scope.values('centre_responsabilite'))
                    | Q(uf__pole__in=tmp_scope.values('pole'))
                    | Q(uf__site__in=tmp_scope.values('site'))
                    | Q(uf__etablissement__in=tmp_scope.values('etablissement')),
                ),
                {},
            )

        columns__remove = (
            # 'calendrier',
            'programme',
            # 'tvx_eval_devact',
            # 'tvx_eval_contin',
            # 'tvx_eval_confort',
            # 'tvx_eval_securite',
            # 'tvx_eval_qvt',
            # 'montant_unitaire_expert_metier',
            'prix_unitaire_conditional',
            'montant_arbitrage',
            'arbitrage_commission',
            # 'commentaire_provisoire_commission',
            'commentaire_definitif_commission',
            'quantite_validee_conditional',  # hidden
            'montant_qte_validee',
            'montant_valide_conditional',
            'montant_final',
            'montant_consomme',
            'gel',
        )
        columns__add = ('tools',)
        user_filters = {
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
            'demande_contains': {
                'type': 'contains',
                'fieldnames': [
                    'referent',
                    'contact',
                    'libelle',
                    'nom_projet',
                    'description',
                    'commentaire_cadre_sup',
                    'decision_soumission',
                    'commentaire_biomed',
                    'commentaire_definitif_commission',
                    'autre_argumentaire',
                    'montant_arbitrage',
                    'localisation',
                    'tvx_contrainte_lib',
                    'tvx_contrainte_alib',
                    'tvx_contrainte_lar',
                    'tvx_contrainte_autre',
                    'tvx_contrainte',
                ],
                'label': _('Demande contient'),
            },
            'tvx_batiment': {
                'type': 'select',
            },
            'tvx_etage': {
                'type': 'select',
            },
            'tvx_priorite': {
                'type': 'select',
            },
        }

        settings = {
            'tvx_eval_devact': {
                'hidden': True,
            },
            'tvx_eval_contin': {
                'hidden': True,
            },
            'tvx_eval_confort': {
                'hidden': True,
            },
            'tvx_eval_securite': {
                'hidden': True,
            },
            'tvx_eval_qvt': {
                'hidden': True,
            },
        }


class DemTvxEnCoursTechSmartView(DemTvxSmartView):
    class Meta:
        columns__add = ('tools',)

        def base_filter(self, view_params: dict):  # NOQA : Unused parameter
            return ~Q(tvx_state__endswith='_OTHER') & (Q(gel__isnull=True) | Q(gel=False))

            # {
            #    'tvx_state__contains': 'TVX',
            # }

        user_filters = {
            'campagne': {
                'type': 'select',
                'choices': {
                    'fieldname': 'calendrier',
                    'label': F('calendrier__nom'),
                    'sort': F('calendrier__code'),
                },
            },
            'redacteur': {
                'type': 'select',
                'choices': lambda view_params, base_filter_args, base_filter_kwargs, manager: [
                    {'label': "Tous", 'value': '{}'},
                ]
                + [
                    {
                        'label': '%s %s' % (record[0], record[1]),
                        'value': '{"redacteur":%d}' % record[2],
                    }
                    for record in Demande.objects.filter(redacteur__isnull=False, discipline_dmd__code='TX')
                    .order_by()
                    .values_list('redacteur__first_name', 'redacteur__last_name', 'redacteur__pk')
                    .distinct()
                ],
            },
            'demande_contains': {
                'type': 'contains',
                'fieldnames': [
                    'referent',
                    'contact',
                    'libelle',
                    'nom_projet',
                    'description',
                    'commentaire_cadre_sup',
                    'decision_soumission',
                    'commentaire_biomed',
                    'commentaire_definitif_commission',
                    'autre_argumentaire',
                    'montant_arbitrage',
                    'localisation',
                    'tvx_contrainte_lib',
                    'tvx_contrainte_alib',
                    'tvx_contrainte_lar',
                    'tvx_contrainte_autre',
                    'tvx_contrainte',
                ],
                'label': _('Demande contient'),
            },
            'uf': {
                'type': 'select',
                #    'choices': {'fieldname': 'uf', 'label': Concat(F('uf__code'),
                #    Value(' - '), F('uf__nom')), 'sort': F('uf__code')},
            },
            'tvx_batiment': {
                'type': 'select',
            },
            'tvx_etage': {
                'type': 'select',
            },
            'tvx_priorite': {
                'type': 'select',
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
        # Demande de travaux courants {{ instance.code }}
            <calendrier>
            <discipline_dmd>
            <couts_complementaires>
            <nom_projet>
            <redacteur>
            # Demandeur
                <referent> <redacteur_view>
            # Projet
                <tvx_batiment> <tvx_etage>
                <uf> <localisation>
                <service_view> <pole_view>
                <libelle-+---->
                <description+--->
                # Contraintes dans la zone
                    <tvx_contrainte_lib----> <tvx_contrainte-+--->
                    <tvx_contrainte_alib---> <tvx_contrainte-+--->
                    <tvx_contrainte_lar----> <tvx_contrainte-+--->
                    <tvx_contrainte_autre--> <tvx_contrainte-+--->
            # Argumentaire
                <tvx_priorite--+--+--+-->
                <tvx_arg_reorg> <tvx_arg_reorg_comment--+--+-->
                <tvx_arg_devact> <tvx_arg_devact_comment--+--+-->
                <tvx_arg_securite> <tvx_arg_securite_comment--+--+-->
                <tvx_arg_qvt> <tvx_arg_qvt_comment--+--+-->
                <tvx_arg_vetustes> <tvx_arg_vetustes_comment--+--+-->
                <tvx_arg_eqpt> <tvx_arg_eqpt_comment--+--+-->
                <tvx_arg_normes> <tvx_arg_normes_comment--+--+-->
                <autre_argumentaire--+---+--+-->
            # Pré-analyse
                <programme> <expert_metier>
            # Analyse
                <tvx_eval_devact>
                <tvx_eval_contin>
                <tvx_eval_confort>
                <tvx_eval_securite>
                <tvx_eval_qvt>
                <montant_unitaire_expert_metier>
                <commentaire_biomed--+-->
                <avis_biomed>
            # Validation
                <arbitrage_commission> <gel>
                <commentaire_definitif_commission>
            # Documents joints
                <--documents_sf-+--+--+->
        """

    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'dem:tvx-demande-tech-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir la demande"),
                },
            ],
        },
    )


class DemTvxPreAnalyseSmartView(DemTvxSmartView):
    class Meta:
        help_text = _(
            "Le responsable technique doit déterminer :"
            " <b>Le programme</b> et <b>l'expert métier</b> qui va chiffer et évaluer le bien fondé de la demande."
            " Une fois ces choix effectués, la demande passera à l'étape suivant, l'analyse par l'expert métier."
        )
        columns__add = ('tools',)
        columns__remove = (
            'calendrier',
            'arbitrage_commission',
            # 'commentaire_provisoire_commission',
            'commentaire_definitif_commission',
            'tvx_eval_devact',
            'tvx_eval_contin',
            'tvx_eval_confort',
            'tvx_eval_securite',
            'tvx_eval_qvt',
            'tvx_eval_synthese',
            'montant_qte_validee',
            'montant_final',
            'montant_consomme',
            'montant_unitaire_expert_metier',
            'prix_unitaire_conditional',
            'commentaire_biomed',
            'montant_valide_conditional',
        )

        # def base_filter(self, request):
        #     return {
        #         'tvx_state': 'TVX_APPROB',
        #     }

        def base_filter(self, view_params):
            return (
                [
                    (Q(programme__isnull=True) | Q(domaine__isnull=True) | Q(expert_metier__isnull=True))
                    & (Q(gel__isnull=True) | Q(gel=False))
                ],
                # Il faut (juste) que l'utilisateur soit dispatcheur...
                {'calendrier__dispatcher': view_params['user']},
            )

        user_filters = {
            'redacteur': {
                'type': 'select',
                'choices': lambda view_params, base_filter_args, base_filter_kwargs, manager: [
                    {'label': "Tous", 'value': '{}'},
                ]
                + [
                    {
                        'label': '%s %s' % (record[0], record[1]),
                        'value': '{"redacteur":%d}' % record[2],
                    }
                    for record in Demande.objects.filter(redacteur__isnull=False, discipline_dmd__code='TX')
                    .order_by()
                    .values_list('redacteur__first_name', 'redacteur__last_name', 'redacteur__pk')
                    .distinct()
                ],
            },
            'demande_contains': {
                'type': 'contains',
                'fieldnames': [
                    'referent',
                    'contact',
                    'libelle',
                    'nom_projet',
                    'description',
                    'commentaire_cadre_sup',
                    'decision_soumission',
                    'commentaire_biomed',
                    'commentaire_definitif_commission',
                    'autre_argumentaire',
                    'montant_arbitrage',
                    'localisation',
                    'tvx_contrainte_lib',
                    'tvx_contrainte_alib',
                    'tvx_contrainte_lar',
                    'tvx_contrainte_autre',
                    'tvx_contrainte',
                ],
                'label': _('Demande contient'),
            },
            'tvx_batiment': {
                'type': 'select',
            },
            'tvx_etage': {
                'type': 'select',
            },
            'tvx_priorite': {
                'type': 'select',
            },
        }
        form_layout = """
        # Demande de travaux courants {{ instance.code }}
            <discipline_dmd>
            <couts_complementaires>
            <nom_projet>
            <redacteur>
            # Demandeur
                <referent> <redacteur_view>
            # Projet
                <tvx_batiment> <tvx_etage>
                <uf> <localisation>
                <service_view> <pole_view>
                <libelle-+---->
                <description+--->
                # Contraintes dans la zone
                    <tvx_contrainte_lib----> <tvx_contrainte-+--->
                    <tvx_contrainte_alib---> <tvx_contrainte-+--->
                    <tvx_contrainte_lar----> <tvx_contrainte-+--->
                    <tvx_contrainte_autre--> <tvx_contrainte-+--->
            # Argumentaire
                <tvx_priorite--+--+--+-->
                <tvx_arg_reorg> <tvx_arg_reorg_comment--+--+-->
                <tvx_arg_devact> <tvx_arg_devact_comment--+--+-->
                <tvx_arg_securite> <tvx_arg_securite_comment--+--+-->
                <tvx_arg_qvt> <tvx_arg_qvt_comment--+--+-->
                <tvx_arg_vetustes> <tvx_arg_vetustes_comment--+--+-->
                <tvx_arg_eqpt> <tvx_arg_eqpt_comment--+--+-->
                <tvx_arg_normes> <tvx_arg_normes_comment--+--+-->
                <autre_argumentaire--+---+--+-->
            # Pré-analyse
                <programme> <expert_metier>
            # Documents joints
                <--documents_sf-+--+--+->
        """

    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'dem:tvx-pre-analyse-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir la demande"),
                },
            ],
        },
    )


class DemTvxAnalyseSmartView(DemTvxSmartView):
    class Meta:
        columns__add = ('tools',)
        columns__remove = (
            'calendrier',
            'arbitrage_commission',
            # 'commentaire_provisoire_commission',
            'commentaire_definitif_commission',
        )
        settings = {
            'prix_unitaire_conditional': {
                'hidden': False,
                'title': _("Coût estimé"),
            },
        }

        # def base_filter(self, request):
        #     return {
        #         'tvx_state': 'TVX_ANA',
        #     }

        base_filter = [
            # Demandes non validées
            Q(gel=False) | Q(gel__isnull=True),
            # Qui a un expert nommé
            Q(expert_metier__isnull=False),
            # Qui n'a pas d'avis défavorable du chef de pôle ou du directeur
            Q(decision_validateur=True) | Q(decision_validateur__isnull=True),
            # Qui reste à expertise
            (Q(prix_unitaire__isnull=True) & Q(montant_unitaire_expert_metier__isnull=True)) | Q(avis_biomed__isnull=True),
            Q(discipline_dmd__code='TX'),  # Exclut les demandes de travaux
        ]

        user_filters = {
            # Petit contournement ici car le calcul automatique du filtre (liste de tous les experts métiers valides dans la vue)
            # ne fonctionne pas en raison d'un défaut de conception de SmartView. Donc on fait le calcul 'à la main'
            # Sans utiliser base_filter_args et base_filter_kwargs
            'expert_metier': {
                'type': 'select',
                'choices': lambda view_params, base_filter_args, base_filter_kwargs, manager: [
                    {'label': "Tous", 'value': '{}'},
                ]
                + [
                    {
                        'label': '%s %s' % (record[0], record[1]),
                        'value': '{"expert_metier":%d}' % record[2],
                    }
                    for record in Demande.objects.filter(expert_metier__isnull=False, discipline_dmd__code='TX')
                    .order_by()
                    .values_list(
                        'expert_metier__first_name',
                        'expert_metier__last_name',
                        'expert_metier__pk',
                    )
                    .distinct()
                ],
            },
            'redacteur': {
                'type': 'select',
                'choices': lambda view_params, base_filter_args, base_filter_kwargs, manager: [
                    {'label': "Tous", 'value': '{}'},
                ]
                + [
                    {
                        'label': '%s %s' % (record[0], record[1]),
                        'value': '{"redacteur":%d}' % record[2],
                    }
                    for record in Demande.objects.filter(redacteur__isnull=False, discipline_dmd__code='TX')
                    .order_by()
                    .values_list('redacteur__first_name', 'redacteur__last_name', 'redacteur__pk')
                    .distinct()
                ],
            },
            'demande_contains': {
                'type': 'contains',
                'fieldnames': [
                    'referent',
                    'contact',
                    'libelle',
                    'nom_projet',
                    'description',
                    'commentaire_cadre_sup',
                    'decision_soumission',
                    'commentaire_biomed',
                    'commentaire_definitif_commission',
                    'autre_argumentaire',
                    'montant_arbitrage',
                    'localisation',
                    'tvx_contrainte_lib',
                    'tvx_contrainte_alib',
                    'tvx_contrainte_lar',
                    'tvx_contrainte_autre',
                    'tvx_contrainte',
                ],
                'label': _('Demande contient'),
            },
            'tvx_batiment': {
                'type': 'select',
            },
            'tvx_etage': {
                'type': 'select',
            },
            'tvx_priorite': {
                'type': 'select',
            },
        }

        form_layout = """
        # Demande de travaux courants {{ instance.code }}
            <discipline_dmd>
            <couts_complementaires>
            <nom_projet>
            <redacteur>
            # Demandeur
                <referent> <redacteur_view>
            # Projet
                <tvx_batiment> <tvx_etage>
                <uf> <localisation>
                <service_view> <pole_view>
                <libelle-+---->
                <description+--->
                # Contraintes dans la zone
                    <tvx_contrainte_lib----> <tvx_contrainte-+--->
                    <tvx_contrainte_alib---> <tvx_contrainte-+--->
                    <tvx_contrainte_lar----> <tvx_contrainte-+--->
                    <tvx_contrainte_autre--> <tvx_contrainte-+--->
            # Argumentaire
                <tvx_priorite--+--+--+-->
                <tvx_arg_reorg> <tvx_arg_reorg_comment--+--+-->
                <tvx_arg_devact> <tvx_arg_devact_comment--+--+-->
                <tvx_arg_securite> <tvx_arg_securite_comment--+--+-->
                <tvx_arg_qvt> <tvx_arg_qvt_comment--+--+-->
                <tvx_arg_vetustes> <tvx_arg_vetustes_comment--+--+-->
                <tvx_arg_eqpt> <tvx_arg_eqpt_comment--+--+-->
                <tvx_arg_normes> <tvx_arg_normes_comment--+--+-->
                <autre_argumentaire--+---+--+-->
            # Pré-analyse
                <programme> <expert_metier>
            # Analyse
                <tvx_eval_devact>
                <tvx_eval_contin>
                <tvx_eval_confort>
                <tvx_eval_securite>
                <tvx_eval_qvt>
                <montant_unitaire_expert_metier>
                <commentaire_biomed--+-->
                <avis_biomed>
            # Documents joints
                <--documents_sf-+--+--+->
        """

    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'dem:tvx-analyse-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir la demande"),
                },
            ],
        },
    )


class DemTvxValidationSmartView(DemTvxSmartView):
    class Meta:
        columns__add = ('tools',)
        columns__remove = ('calendrier',)
        settings = {
            'montant_arbitrage': {
                'hidden': False,
                'title': _("Estimation"),
            },
            'montant_valide_conditional': {
                'hidden': False,
                'title': _("Enveloppe"),
            },
            'commentaire_definitif_commission': {
                'title': _("Commentaire validation"),
            },
            'gel': {
                'hidden': False,
            },
        }

        def base_filter(self, view_params):
            return {
                'tvx_state': 'TVX_ARB',
            }

        user_filters__update = {
            'expert_metier': {'type': 'select'},
            'arbitrage_commission': {'type': 'select'},
            'gel': {'type': 'select'},
        }

        form_layout = """
        # Demande de travaux courants {{ instance.code }}
            <discipline_dmd>
            <couts_complementaires>
            <nom_projet>
            <redacteur>
            # Demandeur
                <referent> <redacteur_view>
            # Projet
                <tvx_batiment> <tvx_etage>
                <uf> <localisation>
                <service_view> <pole_view>
                <libelle-+---->
                <description+--->
                # Contraintes dans la zone
                    <tvx_contrainte_lib----> <tvx_contrainte-+--->
                    <tvx_contrainte_alib---> <tvx_contrainte-+--->
                    <tvx_contrainte_lar----> <tvx_contrainte-+--->
                    <tvx_contrainte_autre--> <tvx_contrainte-+--->
            # Argumentaire
                <tvx_priorite--+--+--+-->
                <tvx_arg_reorg> <tvx_arg_reorg_comment--+--+-->
                <tvx_arg_devact> <tvx_arg_devact_comment--+--+-->
                <tvx_arg_securite> <tvx_arg_securite_comment--+--+-->
                <tvx_arg_qvt> <tvx_arg_qvt_comment--+--+-->
                <tvx_arg_vetustes> <tvx_arg_vetustes_comment--+--+-->
                <tvx_arg_eqpt> <tvx_arg_eqpt_comment--+--+-->
                <tvx_arg_normes> <tvx_arg_normes_comment--+--+-->
                <autre_argumentaire--+---+--+-->
            # Pré-analyse
                <programme> <expert_metier>
            # Analyse
                <tvx_eval_devact>
                <tvx_eval_contin>
                <tvx_eval_confort>
                <tvx_eval_securite>
                <tvx_eval_qvt>
                <montant_unitaire_expert_metier>
                <commentaire_biomed--+-->
                <avis_biomed>
            # Validation
                <arbitrage_commission> <gel>
                <commentaire_definitif_commission>
            # Documents joints
                <--documents_sf-+--+--+->
        """

    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'dem:tvx-demande-validation-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir la demande"),
                },
            ],
        },
    )


class DemTvxArchiveesSmartView(DemTvxSmartView):
    class Meta:
        columns__remove = (
            # 'calendrier',
            'programme',
            'tvx_eval_devact',
            'tvx_eval_contin',
            'tvx_eval_confort',
            'tvx_eval_securite',
            'tvx_eval_qvt',
            'tvx_eval_synthese',
            'avis_biomed',
            'commentaire_biomed',
            # 'montant_unitaire_expert_metier',
            'prix_unitaire_conditional',
            'montant_arbitrage',
            'arbitrage_commission',
            # 'commentaire_provisoire_commission',
            # 'commentaire_definitif_commission',
            'quantite_validee_conditional',  # hidden
            'montant_qte_validee',
            'montant_valide_conditional',
            'montant_final',
            'montant_consomme',
            'gel',
        )
        columns__add = ('tools',)

        def base_filter(self, request):
            return (Q(gel=True, discipline_dmd__code='TX'),)

        row_styler = {
            'fieldname': 'tvx_state',
            'styles': {
                ('TVX_REFUSE',): ("background:#fcc", "Demande non validée"),
                'TVX_VALIDE': ("background:#cfc", "Demande validée"),
            },
        }
        user_filters = {
            'campagne': {
                'type': 'select',
                'choices': {
                    'fieldname': 'calendrier',
                    'label': F('calendrier__nom'),
                    'sort': F('calendrier__code'),
                },
            },
            'demande_contains': {
                'type': 'contains',
                'fieldnames': [
                    'referent',
                    'contact',
                    'libelle',
                    'nom_projet',
                    'description',
                    'commentaire_cadre_sup',
                    'decision_soumission',
                    'commentaire_biomed',
                    'commentaire_definitif_commission',
                    'autre_argumentaire',
                    'montant_arbitrage',
                    'localisation',
                    'tvx_contrainte_lib',
                    'tvx_contrainte_alib',
                    'tvx_contrainte_lar',
                    'tvx_contrainte_autre',
                    'tvx_contrainte',
                ],
                'label': _('Demande contient'),
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
            'tvx_batiment': {
                'type': 'select',
            },
            'tvx_etage': {
                'type': 'select',
            },
            'tvx_priorite': {
                'type': 'select',
            },
            'state_code': {
                'type': 'select',
                'choices': '__STYLES__',
                'position': 'bar',
            },
        }

        settings = {
            'tvx_eval_devact': {
                'hidden': True,
            },
            'tvx_eval_contin': {
                'hidden': True,
            },
            'tvx_eval_confort': {
                'hidden': True,
            },
            'tvx_eval_securite': {
                'hidden': True,
            },
            'tvx_eval_qvt': {
                'hidden': True,
            },
        }


class DemTvxHome(BiomAidViewMixin, TemplateView):
    application = 'dem'
    name = 'tvx-home'
    title = _("Portail gestion des demandes de Travaux")
    permissions = '__LOGIN__'
    template_name = 'dem/tvx-home.html'


class DemandeTvx(SmartPage):
    application = 'dem'
    name = 'tvx-demande'
    title = _("Demandes de travaux en cours")
    permissions = (
        'RMA',
        'CAD',
        'RUN',
        'CHS',
        'CADS',
        'AMAR',
        'DRP',
        'CAP',
        'CSP',
        'ACHP',
        'CHP',
        'COP',
        'DIR',
        'EXP',
        'DIS',
        'ARB',
    )
    smart_view_class = DemTvxEnCoursSmartView

    header_message = _("Liste de toutes les demandes de travaux en cours d'expertise ou d'arbitrage")

    record_ok_message = _("Demande de travaux {code} enregistrée avec succès")
    deleted_done_message = _("La demande de travaux {code} a été supprimée.")
    no_grant_to_delete_record_message = _("Vous n'avez pas les droits suffisants pour supprimer la demande {code}.")
    try_to_delete_wthout_confirm_message = _(
        "La demande {code} ne peut être supprimée sans passer par le formulaire de confirmation"
    )

    smart_modes__update = {
        'create': {
            # 'kwargs': {
            #     'campagne': {'type': 'str'},
            # },
            'title': _("Saisie d'une nouvelle"),
            'buttons': (
                {
                    'type': 'submit',
                    'label': _("Enregistrer et ajouter un autre demande"),
                    'value': 'record',
                    'redirect': 'create',  # Attention : Redirection vers le mode None (mode par défaut)
                    # 'redirect_params': '{"campagne":"{{campagne}}"}',
                },
                {
                    'type': 'submit',
                    'label': _("Ajouter et retour à la liste"),
                    'value': 'record-then-list',
                    'message': _("<br><br>Vous allez être redirigé vers la liste"),
                    'redirect': None,  # Attention : Redirection vers le mode None (mode par défaut)
                },
                {
                    'type': 'reset',
                    'label': _("Réinitialiser le formulaire"),
                    'redirect_url_params': lambda vp: vp['request_get'].urlencode(),
                },
            ),
        },
    }


class DemandeTvxApprob(SmartPage):
    application = 'dem'
    name = 'tvx-demande-approb'
    title = _("Demandes de travaux en attente d'approbation")
    permissions = (
        'RMA',
        'CAD',
        'RUN',
        'CHS',
        'CADS',
        'AMAR',
        'DRP',
        'CAP',
        'CSP',
        'ACHP',
        'CHP',
        'COP',
        'DIR',
        'EXP',
        'DIS',
        'ARB',
    )
    smart_view_class = DemTvxApprobSmartView
    record_ok_message = _("Demande de travaux {code} enregistrée avec succès")
    deleted_done_message = _("La demande de travaux {code} a été supprimée.")
    no_grant_to_delete_record_message = _("Vous n'avez pas les droits suffisants pour supprimer la demande {code}.")
    try_to_delete_wthout_confirm_message = _(
        "La demande {code} ne peut être supprimée sans passer par le formulaire de confirmation"
    )


class DemandeTvxTech(SmartPage, BiomAidViewMixin, TemplateView):
    application = 'dem'
    name = 'tvx-demande-tech'
    title = _("Demandes de travaux en cours")
    permissions = (
        'EXP',
        'DIS',
        'ARB',
    )
    smart_view_class = DemTvxEnCoursTechSmartView
    record_ok_message = _("Demande de travaux {code} enregistrée avec succès")
    deleted_done_message = _("La demande de travaux {code} a été supprimée.")
    no_grant_to_delete_record_message = _("Vous n'avez pas les droits suffisants pour supprimer la demande {code}.")
    try_to_delete_wthout_confirm_message = _(
        "La demande {code} ne peut être supprimée sans passer par le formulaire de confirmation"
    )


class DemandeTvxPreAnalyse(SmartPage, BiomAidViewMixin, TemplateView):
    application = 'dem'
    name = 'tvx-pre-analyse'
    title = _("Demandes de travaux : Pré-analyse")
    permissions = ('DIS',)
    record_ok_message = _("Demande de travaux {code} enregistrée avec succès")
    deleted_done_message = _("La demande de travaux {code} a été supprimée.")
    no_grant_to_delete_record_message = _("Vous n'avez pas les droits suffisants pour supprimer la demande {code}.")
    try_to_delete_wthout_confirm_message = _(
        "La demande {code} ne peut être supprimée sans passer par le formulaire de confirmation"
    )
    smart_view_class = DemTvxPreAnalyseSmartView


class DemandeTvxAnalyse(SmartPage, BiomAidViewMixin, TemplateView):
    application = 'dem'
    name = 'tvx-analyse'
    title = _("Demandes de travaux : Analyse")
    permissions = ('EXP',)
    smart_view_class = DemTvxAnalyseSmartView
    record_ok_message = _("Demande de travaux {code} enregistrée avec succès")
    deleted_done_message = _("La demande de travaux {code} a été supprimée.")
    no_grant_to_delete_record_message = _("Vous n'avez pas les droits suffisants pour supprimer la demande {code}.")
    try_to_delete_wthout_confirm_message = _(
        "La demande {code} ne peut être supprimée sans passer par le formulaire de confirmation"
    )


class DemandeTvxValidation(SmartPage, BiomAidViewMixin, TemplateView):
    application = 'dem'
    name = 'tvx-demande-validation'
    title = _("Demandes de travaux : Validation")
    permissions = ('ARB',)
    smart_view_class = DemTvxValidationSmartView
    record_ok_message = _("Demande de travaux {code} enregistrée avec succès")
    deleted_done_message = _("La demande de travaux {code} a été supprimée.")
    no_grant_to_delete_record_message = _("Vous n'avez pas les droits suffisants pour supprimer la demande {code}.")
    try_to_delete_wthout_confirm_message = _(
        "La demande {code} ne peut être supprimée sans passer par le formulaire de confirmation"
    )


class DemandeTvxArchivees(SmartPage, BiomAidViewMixin, TemplateView):
    application = 'dem'
    name = 'tvx-demandes-archivees'
    title = _("Demandes de travaux : Archives")
    permissions = (
        'RMA',
        'CAD',
        'RUN',
        'CHS',
        'CADS',
        'AMAR',
        'DRP',
        'CAP',
        'CSP',
        'ACHP',
        'CHP',
        'COP',
        'DIR',
        'EXP',
        'DIS',
        'ARB',
    )
    smart_view_class = DemTvxArchiveesSmartView

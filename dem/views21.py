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
import json
from urllib.parse import quote_plus

from django.db.models import Q
from django.template import Context, Engine
from django.utils.timezone import now

from django.utils.translation import gettext as _
from html_sanitizer.django import get_sanitizer

# from common.base_views import BiomAidView
from django.views.generic import TemplateView
from common import config

from common.base_views import BiomAidViewMixin
from common.models import UserUfRole
from dem.models import Demande, Campagne

# from dem.views import DemView
from dem.smart_views import (
    DemandesAApprouverSmartView,
    DemandesArchiveesExpertSmartView,
    DemandesEtudeSmartView,
    DemandesEnCoursSmartView,
    DemandesEnCoursExpSmartView,
    DemandesArchiveesSmartView,
    DemandesRepartitionSmartView,
    DemandesExpertiseSmartView,
    DemandesArbitrageSmartView,
)
from smart_view.smart_page import SmartPage


class DemHomeView(BiomAidViewMixin, TemplateView):
    application = 'dem'
    name = 'home'
    permissions = '__LOGIN__'
    template_name = 'dem/home.html'

    def main_tour_steps(self, context):
        return super().main_tour_steps(context) + [
            {
                'selector': 'ul.main_menu',
                'title': "Le menu pricipal",
                'content': "Comme sur l'Intranet, vous avez à cet endroit le menu qui vous permet"
                " d'accéder à toutes les pages du site.",
            },
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        engine = Engine.get_default()
        content_context = Context({'url_prefix': self.url_prefix})
        template = engine.from_string(
            config.get('dem.home.template', default="""Set the dem.home.template variable in a config file !""")
        )
        # html sanitizer
        sanitizer = get_sanitizer('page_content')
        context['content_html'] = sanitizer.sanitize(template.render(content_context))

        context['title'] = "Accueil"
        context['campagne_code_kwargs'] = {'campagne_code': '2022-PE'}
        return context


class DemCockpit(BiomAidViewMixin, TemplateView):
    title = 'Cockpit gestion demandes de matériel'
    permissions = ('DIS', 'EXP', 'ARB', 'ADM')
    template_name = 'dem/cockpit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Liste des campagnes (sauf travaux) pour lesquelles
        #   il y a au moins une demande non traitées OU avec un recensement en cours
        # Et pour lesquelles l'utilisateur est soit dispatcher, soit arbitre, soit expert.
        campagnes = (
            Campagne.records.order_by()
            .filter(
                ~Q(code__contains='TVX')
                & (
                    Q(dispatcher=self.request.user)
                    | Q(programme__arbitre=self.request.user)
                    | Q(demande__expert_metier=self.request.user)
                )
                & (
                    (Q(demande__gel__isnull=True) | Q(demande__gel=False))
                    | (Q(debut_recensement__lte=now()) & Q(fin_recensement__gt=now()))
                )
            )
            .distinct()
            .order_by('code')
        )

        tmp_scope = UserUfRole.records.filter(
            user=self.request.user,
            role_code__in=('CHP', 'DIR'),
        )
        a_valider_par_moi_qs = Demande.records.filter(
            Q(gel__isnull=True) | Q(gel=False),
            ~Q(calendrier__code__contains='TVX'),
            Q(uf__in=tmp_scope.values('uf'))
            | Q(uf__service__in=tmp_scope.values('service'))
            | Q(uf__centre_responsabilite__in=tmp_scope.values('centre_responsabilite'))
            | Q(uf__pole__in=tmp_scope.values('pole'))
            | Q(uf__site__in=tmp_scope.values('site'))
            | Q(uf__etablissement__in=tmp_scope.values('etablissement')),
            decision_validateur__isnull=True,
        )

        context['campagne_rows'] = []
        queryset = Demande.records.filter(
            ~Q(discipline_dmd__code='TX') & (Q(gel=False) | Q(gel__isnull=True)),
        )
        for campagne in campagnes:
            context['campagne_rows'].append(
                {
                    'campagne': campagne,
                    'toutes': queryset.filter(calendrier=campagne.pk),
                    'non_soumises': queryset.filter(decision_validateur__isnull=True, calendrier=campagne.pk),
                    'non_soumises_moi': a_valider_par_moi_qs.filter(calendrier=campagne.pk),
                    'repartir': queryset.filter(
                        Q(programme__isnull=True) | Q(expert_metier__isnull=True) | Q(domaine__isnull=True),
                        calendrier=campagne.pk,
                    ),
                    'repartir_moi': queryset.filter(
                        Q(programme__isnull=True) | Q(expert_metier__isnull=True) | Q(domaine__isnull=True),
                        calendrier__dispatcher=self.request.user,
                        calendrier=campagne.pk,
                    ),
                    'expertiser': queryset.filter(
                        Q(expert_metier__isnull=False)
                        & (Q(decision_validateur=True) | Q(decision_validateur__isnull=True))
                        & (
                            (Q(prix_unitaire__isnull=True) & Q(montant_unitaire_expert_metier__isnull=True))
                            | Q(avis_biomed__isnull=True)
                        ),
                        calendrier=campagne.pk,
                    ),
                    'expertiser_moi': queryset.filter(
                        Q(expert_metier=self.request.user)
                        & (Q(decision_validateur=True) | Q(decision_validateur__isnull=True))
                        & (
                            (Q(prix_unitaire__isnull=True) & Q(montant_unitaire_expert_metier__isnull=True))
                            | Q(avis_biomed__isnull=True)
                        ),
                        calendrier=campagne.pk,
                    ),
                    'expertiser_filters': quote_plus(
                        json.dumps(
                            [
                                {
                                    'name': 'calendrier',
                                    'value': {'calendrier': campagne.pk},
                                },
                                {
                                    'name': 'expert_metier',
                                    'value': {'expert_metier': self.request.user.pk},
                                },
                            ]
                        )
                    ),
                    'arbitrer': queryset.filter(
                        Q(prix_unitaire__isnull=False) | Q(montant_unitaire_expert_metier__isnull=False),
                        avis_biomed__isnull=False,
                        programme__isnull=False,
                        # decision_validateur__isnull=False,
                        calendrier=campagne.pk,
                    ),
                    'arbitrer_moi': queryset.filter(
                        Q(prix_unitaire__isnull=False) | Q(montant_unitaire_expert_metier__isnull=False),
                        avis_biomed__isnull=False,
                        programme__isnull=False,
                        # decision_validateur__isnull=False,
                        programme__arbitre=self.request.user,
                        calendrier=campagne.pk,
                    ),
                    'arbitrer_filters': quote_plus(
                        json.dumps(
                            [
                                {
                                    'name': 'campagne',
                                    'value': {'calendrier': campagne.pk},
                                },
                                {
                                    'name': 'avis_biomed',
                                    'value': {'avis_biomed__isnull': False},
                                },
                            ]
                        )
                    ),
                }
            )

        context['non_soumises_total'] = Demande.records.filter(
            ~Q(discipline_dmd__code='TX') & (Q(decision_validateur__isnull=True)) & (Q(gel=False) | Q(gel__isnull=True)),
        ).count()

        context['non_soumises_total_moi'] = a_valider_par_moi_qs.count()

        context['repartir_total'] = Demande.records.filter(
            ~Q(discipline_dmd__code='TX')
            & (Q(programme__isnull=True) | Q(expert_metier__isnull=True) | Q(domaine__isnull=True))
            & (Q(gel=False) | Q(gel__isnull=True)),
        ).count()

        context['repartir_total_moi'] = Demande.records.filter(
            ~Q(discipline_dmd__code='TX')
            & (Q(programme__isnull=True) | Q(expert_metier__isnull=True) | Q(domaine__isnull=True))
            & (Q(gel=False) | Q(gel__isnull=True)),
            calendrier__dispatcher=self.request.user,
        ).count()

        # if 'entries' in context['main_menu'][4]:
        #     context['repartir_me'] = [
        #         {
        #             'label': Calendrier.records.get(code=entry['url_kwargs']['campagne_code']),
        #             'count': Demande.records.filter(
        #                 ~Q(discipline_dmd__code='TX')
        #                 & (Q(programme__isnull=True) | Q(expert_metier__isnull=True) | Q(domaine__isnull=True))
        #                 & (Q(gel=False) | Q(gel__isnull=True)),
        #                 calendrier__dispatcher=self.request.user,
        #                 calendrier__code=entry['url_kwargs']['campagne_code'],
        #             ).count(),
        #             'kwargs': entry['url_kwargs'],
        #         }
        #         for entry in context['main_menu'][4]['entries']
        #     ]
        # else:
        #     context['repartir_me'] = 0

        context['expertiser_total'] = Demande.records.filter(
            ~Q(discipline_dmd__code='TX')
            & Q(expert_metier__isnull=False)
            & (Q(decision_validateur=True) | Q(decision_validateur__isnull=True))
            & ((Q(prix_unitaire__isnull=True) & Q(montant_unitaire_expert_metier__isnull=True)) | Q(avis_biomed__isnull=True))
            & (Q(gel=False) | Q(gel__isnull=True)),
        ).count()

        context['expertiser_total_moi'] = Demande.records.filter(
            ~Q(discipline_dmd__code='TX')
            & Q(expert_metier=self.request.user)
            & (Q(decision_validateur=True) | Q(decision_validateur__isnull=True))
            & ((Q(prix_unitaire__isnull=True) & Q(montant_unitaire_expert_metier__isnull=True)) | Q(avis_biomed__isnull=True))
            & (Q(gel=False) | Q(gel__isnull=True)),
        ).count()

        context['expertiser_total_filters'] = quote_plus(
            json.dumps(
                [
                    {
                        'name': 'expert_metier',
                        'value': {'expert_metier': self.request.user.pk},
                    }
                ]
            )
        )
        context['arbitrer_total_filters'] = quote_plus(
            json.dumps(
                [
                    {
                        'name': 'avis_biomed',
                        'value': {'avis_biomed__isnull': False},
                    }
                ]
            )
        )

        context['arbitrer_total'] = Demande.records.filter(
            ~Q(discipline_dmd__code='TX')
            & Q(programme__isnull=False)
            & Q(programme__arbitre__isnull=False)
            # & Q(decision_validateur__isnull=False)
            & ((Q(prix_unitaire__isnull=False) | Q(montant_unitaire_expert_metier__isnull=False)) & Q(avis_biomed__isnull=False))
            & (Q(gel=False) | Q(gel__isnull=True)),
        ).count()

        context['arbitrer_total_moi'] = Demande.records.filter(
            ~Q(discipline_dmd__code='TX')
            & Q(programme__isnull=False)
            & Q(programme__arbitre=self.request.user)
            # & Q(decision_validateur__isnull=False)
            & ((Q(prix_unitaire__isnull=False) | Q(montant_unitaire_expert_metier__isnull=False)) & Q(avis_biomed__isnull=False))
            & (Q(gel=False) | Q(gel__isnull=True)),
        ).count()

        context['toutes_total'] = queryset.count()

        context['traitees_total'] = Demande.records.filter(
            ~Q(discipline_dmd__code='TX') & Q(gel=True),
        ).count()

        return context


class DemandesAApprouverView(SmartPage):
    application = 'dem'
    name = 'demandes-a-approuver'
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
        'TECH',
    )
    smart_view_class = DemandesAApprouverSmartView
    title = _("Demandes à approuver")


class DemandesEtudeView(SmartPage):
    application = 'dem'
    name = 'demandes-a-l-etude'
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
        'TECH',
    )
    smart_view_class = DemandesEtudeSmartView
    title = _("Demandes à l'étude")


class DemandesEnCoursView(SmartPage):
    application = 'dem'
    name = 'demandes-en-cours'
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
        'TECH',
    )
    smart_view_class = DemandesEnCoursSmartView
    title = _("Demandes en cours")


class DemandesEnCoursExpView(SmartPage):
    application = 'dem'
    name = 'demandes-en-cours-exp'
    permissions = ('DIS', 'EXP', 'ARB', 'ADM')
    smart_view_class = DemandesEnCoursExpSmartView
    title = _("Demandes en cours (vue expert)")


class DemandesArchivees(SmartPage):
    application = 'dem'
    name = 'demandes-tout'
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
        'TECH',
    )
    smart_view_class = DemandesArchiveesSmartView
    title = "Demandes archivées"


class DemandesArchiveesExpert(SmartPage):
    application = 'dem'
    name = 'demandes-archivees-expert'
    permissions = ('DIS', 'EXP', 'ARB', 'ADM')
    smart_view_class = DemandesArchiveesExpertSmartView
    title = "Demandes archivées (vue expert)"


class DemandesRepartitionView(SmartPage):
    application = 'dem'
    name = 'repartition'
    smart_view_class = DemandesRepartitionSmartView
    title = "Répartition"
    permissions = {'DIS'}

    def view_filters(self, *args, **kwargs):  # NOQA : Unused self, but it could have been
        # print('view_filters')
        return {'calendrier__code': kwargs['campagne_code']}


class DemandesExpertiseView(SmartPage):
    application = 'dem'
    name = 'expertise'
    smart_view_class = DemandesExpertiseSmartView
    title = "Expertise"
    permissions = {'ACH', 'EXP'}


class DemandeArbitrageView(SmartPage):
    application = 'dem'
    name = 'arbitrage'
    permissions = ('ARB', 'ADM')
    smart_view_class = DemandesArbitrageSmartView
    title = "Arbitrage"
    menu_left = ({'label': 'Synthèse', 'url_name': 'dem:vue-filtre-synthese'},)

    def view_filters(self, *args, **kwargs):  # NOQA : Unused self, but it could have been
        if 'programme_code' in kwargs:
            return {'programme__code': kwargs['programme_code']}
        else:
            return {}

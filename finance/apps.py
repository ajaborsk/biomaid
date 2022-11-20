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
import re

from django.apps import AppConfig, apps
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


no_interv_re = re.compile(r"(\b\d\d\d\d\d+\b)")
inv_re_list = [re.compile(s) for s in (r'\b20\d\d-\d\d\d\d\d\b', r'\b\d\d\d\d.\d\d.\d\d\d/\d+\b')]


def get_intv_from_order(order, rows=[]):
    from assetplusconnect.models import BEq1996
    from assetplusconnect.models import EnCours
    from assetplusconnect.models import BFt1996

    interventions = {}

    # Interventions anonymes (non rattachées à une ligne de commande)
    nu_intv_bn = set(no_interv_re.findall(order['bloc_note']))

    # Interventions liées aux lignes
    for row in rows:
        nu_intv_bn.update(set(no_interv_re.findall(row['libelle'])))

    interventions_qs = (
        EnCours.objects.using('gmao')
        .filter(Q(nu_int__in=nu_intv_bn) | Q(nu_bon_c=order['commande']))
        .values('nu_int', 'nu_imm', 'nu_bon_c', 'n_uf', 'code_four')
    )
    if interventions_qs.count():
        interventions_qs._fetch_all()
        interventions.update({i['nu_int']: i for i in interventions_qs})
    interventions_qs = (
        BFt1996.objects.using('gmao')
        .filter(Q(nu_int__in=nu_intv_bn) | Q(nu_bon_c=order['commande']))
        .values('nu_int', 'nu_imm', 'nu_bon_c', 'n_uf', 'code_four')
    )
    if interventions_qs.count():
        interventions_qs._fetch_all()
        interventions.update({i['nu_int']: i for i in interventions_qs})

    for intv in interventions.values():
        eqpt = BEq1996.objects.using('gmao').filter(n_imma=intv['nu_imm'])
        if len(eqpt):
            intv.update({'n_seri': eqpt[0].n_seri})
            intv.update({'marque': eqpt[0].marque})
            intv.update({'typ_mod': eqpt[0].typ_mod})
        else:
            intv.update({'n_seri': 'Inconnu'})
            intv.update({'marque': 'Inconnu'})
            intv.update({'typ_mod': 'Inconnu'})

    return interventions


def commande_non_soldee_interventions_archivees(name, data):
    print("commande_non_soldee_interventions_archivees...")

    """
      Pour chaque commande non soldée, ce qui peut être incorrect :
      - Pas d'intervention associée du tout ==> très vieille commande en général (+ 2 ans)
      - Tous les équipements concernés sont réformés ==> très vieille commande en général
      - Toutes les lignes (non soldées) sont engagées à 0 € ==> vieille commande (+ 6 mois)
      - Nb interventions archivées > nb lignes soldées (on ne compte que les lignes
            avec engagement != 0 €) ==> retard dans les soldes
      - Nb interventions associées != nombre de lignes de commande (on ne compte que les lignes avec engagement != 0 €)
            ==> erreur(s) de saisie (probablement dans magh2)
      - Toutes les interventions associées ne référencent pas le n° de commande
            ==> erreur de saisie (probablement dans Asset+ ou dans le BN)
      - âge > X jours ==> relance à faire ?
    """
    alerts = []
    ext_commande_model = apps.get_model('extable', 'ExtCommande')
    order_ids = (
        ext_commande_model.objects.filter(gest_ec='IF', lg_soldee_lc='N')
        .order_by()
        .values('commande', 'bloc_note')
        .distinct()
        .order_by('commande')
    )
    # print(order_ids, len(order_ids))

    for order in order_ids:
        print(order['commande'], end=' ')
        intvs = get_intv_from_order(order)
        print(intvs)

    print("commande_non_soldee_interventions_archivees:", len(alerts), alerts)

    return alerts, {'categorie': name}


class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance'
    verbose_name = _("Gestion économique et financière")

    # C'est une application biom_aid (avec son portail)
    biom_aid = {
        'portal': {
            # Only users with one of these roles can access the portal
            'permissions': (
                'ACH',
                'EXP',
                'ADM',
                'DIS',
                'GES',
            ),
            # Label of the portal
            'main-name': _("Finances"),
            'label': _("Gestion Economique et Financière"),
            # Home page, default is 'appname:home' where appname is the application name
            'home': 'finance:home',
            'global-status-message': _("Hi, there, everybody"),
            'user-status-message': _("Hi, there, everybody"),
            'main-menu': (
                {
                    'label': _("Accueil"),
                    'url_name': 'finance:home',
                },
                {
                    'label': _("Programmes"),
                    'entries': (
                        {
                            'label': _("Liste des programmes"),
                            'url_name': 'common:programme',
                        },
                        {
                            'label': _("Bilan demandes"),
                            'url_name': 'finance:dem-assessment',
                        },
                    ),
                },
                {
                    'label': _("Commandes"),
                    'entries': (
                        {
                            'label': _("Recherche"),
                            'url_name': 'finance:order',
                        },
                        {
                            'label': _("Liste des commandes"),
                            'url_name': 'finance:orders',
                        },
                    ),
                },
                {
                    'label': _("Factures"),
                    'url_name': 'finance:invoices',
                },
                {
                    'label': _("Immobilisations"),
                    'url_name': 'finance:immobilisations',
                },
            ),
        },
    }
    biom_aid_roles = (
        'ADM',
        'ACH',
        'EXP',
        'DIS',
        'GES',
    )
    biom_aid_alert_categories = {
        'commande-non-soldee-1': {
            'label': _("Commandes non soldées / interventions archivées"),
            'check_func': commande_non_soldee_interventions_archivees,
        }
    }

    def ready(self):
        from django.apps import apps
        from finance.analytics import orders_flaws_processor

        apps.get_app_config('analytics').register_data_processor('orders_flaws_processor', orders_flaws_processor)

    # def server_ready(self) -> None:
    #     from analytics.data import set_datasource

    #     set_datasource(
    #         'finance.orders-flaws',
    #         label=_("Problèmes liés aux commandes"),
    #         auto=[{}],
    #         parameters={},
    #         processor='orders_flaws_processor',
    #     )

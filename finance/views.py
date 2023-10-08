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
from datetime import datetime
from functools import reduce

from altair import Chart, Data, Y
from django.apps import apps
from django.db import DatabaseError, Error as DbError
from django.db.models import Value, F, CharField, When, Case, Q, Sum, Count
from django.db.models.functions import Replace
from django.http import HttpRequest
from django.utils.connection import ConnectionDoesNotExist
from django.utils.timezone import now
from django.views.generic import TemplateView
from django_tables2 import Table, Column, TemplateColumn
from django.utils.translation import gettext as _
from django.shortcuts import render

import tomlkit
import pathlib

import finance
from analytics.data import get_last_data
from finance.analytics import get_intv
from smart_view.smart_widget import (
    AltairWidget,
    ContainerWidget,
    GridWidget,
    HtmlWidget,
    SimpleLightWidget,
    WidgetPageMetaClass,
    SimpleTextWidget,
    LightAndTextWidget,
)
from assetplusconnect.models import BFt1996, EnCours, Docliste, BEq1996
from common.models import Programme, Etablissement, Discipline

# from common.base_views import BiomAidView
from common.base_views import BiomAidViewMixin

from finance.apps import no_interv_re, inv_re_list
from finance.management.commands.gest_analyse import ORDER_ANOMALIES
from finance.smart_views import DemAssessmentSmartView
from smart_view.smart_page import SmartPage

from drachar.models import Previsionnel


class FinanceView(BiomAidViewMixin, TemplateView):
    # Droits de base pour toutes les vues de l'application. A modifier par héritage au besoin.
    permissions = {
        'EXP',
        'ACH',
        'DIS',
        'ARB',
        'ADM',
        'GES',
    }

    # Nom de l'application
    application = 'finance'

    # Titre général de l'application
    application_title = _("Gestion Economique et Financière")

    # module dans lequel il faut chercher la liste des vues (pour le menu)
    views_module = finance


def flawed_orders(gest='IF'):
    """
    Niveaux d'anomalie synthétique :
    =================================

    C'est le premier caractère du code d'anomalie

    4 - ERROR = Il y a une erreur suffisamment grave pour empêcher le fonctionnement
       (données incomplètes) et/ou la suite de l'analyse
    3 - THINGTODO = Il semble y avoir quelque chose à faire (Ex: Commande à solder)
    2 - MINOR = Il y a une erreur mais récupérable grâce à la ou sans impact direct
       (Ex: n° commande pas indiqué dans l'intervention)
    1 - NOTICE = Quelque chose est notable, mais pas forcément anormal (Ex: commande très ancienne)
    0 - NOTHING = Tout va bien :-)

    Ajout d'un 'score', facultatif, par catégorie qui permet de classer les anomalies (dans sa catégorie)

    Pour chaque commande **non soldée**, ce qui peut être incorrect :
    =================================================================

    - Pas d'intervention associée du tout ==> très vieille commande en général (+ 2 ans)
    - Tous les équipements concernés sont réformés ==> très vieille commande en général
    DONE - Toutes les lignes (non soldées) sont engagées à 0 € ==> vieille commande (+ 6 mois)
    - Nb interventions associées != nombre de lignes de commande
       (on ne compte que les lignes avec engagement != 0 €) ==> erreur(s) de saisie (probablement dans magh2)
    - Toutes les interventions associées ne référencent pas le n° de commande ==> erreur de saisie
       (probablement dans Asset+ ou dans le BN)

    - Nb interventions archivées > nb lignes soldées
       (on ne compte que les lignes avec engagement != 0 €) ==> retard dans les soldes

    DONE - âge > X jours ==> relance à faire ?
    """

    ext_commande_model = apps.get_model('extable', 'ExtCommande')
    order_qs = (
        ext_commande_model.records.filter(gest_ec=gest, lg_soldee_lc='N')
        .order_by()
        .annotate(
            lg_zero=Case(When(mt_engage_lc__gt=-0.01, mt_engage_lc__lt=0.01, then=Value(1))),
            default=Value(0),
        )
        .annotate(
            lg_soldee=Case(When(lg_soldee_lc='O', lg_zero=0, then=Value(1))),
            default=Value(0),
        )
        .values(
            'commande',
            'date_passation_ec',
            'no_fournisseur_fr',
            'intitule_fournisseur_fr',
            'objet_depense_ec',
            'bloc_note',
        )
        .annotate(
            lignes=Count('no_ligne_lc'),
            engage=Sum('mt_engage_lc'),
            liquide=Sum('mt_liquide_lc'),
            lgs_zero=Sum('lg_zero'),
            lgs_soldees=Sum('lg_soldee'),
        )
        .distinct()
        .order_by('date_passation_ec')
    )
    ret = {
        'old_orders': [],
        'to_close_orders': [],
        'bad_orders': [],
        'ok': [],
        'count': order_qs.count(),
    }

    return ret

    for order in order_qs:
        score = 0  # Score de 'non qualité' (pour le tri)
        destination = 'ok'  # poll de destination par défaut
        # order_is_null = False  # Toutes les lignes de la commande sont à 0.00 €
        order['problemes'] = []  # Liste (sous forme de texte) des problèmes rencontrés
        anomalies = set()
        rows = [
            dict(row, **{'interv': no_interv_re.findall(row['libelle'])})
            for row in ext_commande_model.records.filter(commande=order['commande']).values(
                'no_ligne_lc',
                'libelle',
                'mt_engage_lc',
                'lg_soldee_lc',
                'commande',
                'analyse',
            )
        ]

        print(order['commande'], repr(rows[0]['analyse']))

        age_over_limit = max((now() - order['date_passation_ec']).days // 30 - 6, 0)
        if age_over_limit > 0:
            score += age_over_limit
            order['problemes'].append(_("Commande ancienne ({} mois)").format(age_over_limit + 6))
            destination = 'old_orders'

        if rows[0]['analyse']['unlinked_intvs']:
            score += 50
            order['problemes'].append(
                'Interventions liées mais non rattachées à des lignes : {}'.format(', '.join(rows[0]['analyse']['unlinked_intvs']))
            )
            destination = 'bad_orders'

        if order['engage'] < 0.01:
            score += 100
            order['problemes'].append('Montant total engagé à 0 €')
            # order_is_null = True
            destination = 'bad_orders'

        # linked_rows_count = 0  # Nombre de lignes de commande liées à des interventions
        # not_null_rows_count = 0  # Nombre de lignes de commande de valeur != 0

        # Balaye toutes les lignes de la commande
        for row in rows:
            if row['mt_engage_lc'] > 0.01:
                if not row['analyse']['linked_intvs']:
                    score += 10
                    order['problemes'].append(
                        'Ligne {} ne peut pas être rapprochée d\'une intervention.'.format(row['no_ligne_lc'])
                    )
                    # order_is_null = True
                    destination = 'bad_orders'
            if 'intv' in row['analyse']:
                if row['analyse']['intv']['nu_bon_c'].upper() != order['commande'].upper():
                    order['problemes'].append(
                        'L\'intervention Asset+ {} associée ne référence pas correctement la commande'.format(
                            row['analyse']['intv']['nu_int']
                        )
                    )
                if row['analyse']['intv']['etat'] == 'Archivée':
                    if row['lg_soldee_lc'] == 'N':
                        score += 50
                        order['problemes'].append(
                            _("La ligne {} associée à l'intervention {} pourrait sans doute être soldée").format(
                                row['no_ligne_lc'], row['analyse']['intv']['nu_int']
                            )
                        )
                        destination = 'to_close_orders'
            else:
                pass

        # intvs = get_intv_from_order(order, rows)
        # # matcher = IntvLignesRecordMatcher({row['no_ligne_lc']: row for row in rows}, intvs)
        # # pprint(matcher.get_all_results())
        #
        # order['interventions'] = list(intvs.keys())
        # if not order['lgs_zero']:
        #     order['lgs_zero'] = 0
        # if not order['lgs_soldees']:
        #     order['lgs_soldees'] = 0
        #
        # # print(f"order {order}")
        #
        # age_over_limit = max((now() - order['date_passation_ec']).days // 30 - 6, 0)
        # if age_over_limit > 0:
        #     score += age_over_limit
        #     order['problemes'].append(_("Commande ancienne ({} mois)").format(age_over_limit + 6))
        #     destination = 'old_orders'
        #
        # nb_intvs_arch = BFt1996.records.using('gmao').filter(nu_int__in=list(intvs.keys())).count()
        # if nb_intvs_arch > order['lgs_soldees']:
        #     score += 25
        #     order['problemes'].append('Probablement {} lignes à solder'.format(nb_intvs_arch - order['lgs_soldees']))
        #     destination = 'to_close_orders'
        #
        # if not intvs:
        #     score += 100
        #     order['problemes'].append('Aucune intervention attachée')
        #     destination = 'bad_orders'
        # else:
        #     if len(intvs) != order['lignes'] - order['lgs_zero'] and not order_is_null:
        #         score += 100
        #         order['problemes'].append(
        #             "Nombre d\'interventions attachées ({}) différent du nombre de lignes non nulles ({})".format(
        #                 len(intvs), order['lignes'] - order['lgs_zero']
        #             )
        #         )
        #         destination = 'bad_orders'

        order['score'] = score
        # if score > 0:
        order['bloc_note'] = '<br>'.join(order['bloc_note'].split('\n'))
        order['problemes'] = '<br>'.join(order['problemes'])

        order['anomalies'] = '<br>'.join([ORDER_ANOMALIES[anomaly]['label'] for anomaly in sorted(anomalies, reverse=True)])

        ret[destination].append(order)

    return ret


class MyTestWidget1(AltairWidget):
    def __init__(self, *args, **kwargs):
        order_class = apps.get_model('extable', 'ExtCommande')

        qs = (
            order_class.records.filter(
                Q(gest_ec__in=['IF', 'II', 'IM', 'IN']),
                ~Q(no_fournisseur_fr=33034),
                exercice_ec__lt=2022,
            )
            .annotate(hm=Case(When(no_marche_ma=0, then=Value(True)), default=Value(False)))
            .filter(hm=True)
            .values('exercice_ec', 'mt_liquide_lc', 'hm')
        )

        chart = (
            Chart(Data(values=list(qs)))
            .transform_aggregate(mt_total='sum(mt_liquide_lc)', groupby=['exercice_ec', 'hm'])
            .mark_bar()
            .encode(x='exercice_ec:O', y=Y('mt_total:Q', stack=True), color='hm:N')
            .properties(width='container', height='container')
        )
        super().__init__(*args, chart=chart, **kwargs)


class GestWidget(HtmlWidget):
    template_string = """
    {% load render_table from django_tables2 %}
    <div>
      {% if flawed_orders %}
      <center><h2>{{ intro_text }} {{ nb_flawed_orders }}</h2></center>
      {% render_table flawed_orders %}
      {% endif %}
    </div>
    """

    class OrdersTable(Table):
        class Meta:
            attrs = {'class': 'tables2', 'style': 'width:100%'}

        commande = TemplateColumn(
            verbose_name=_("Commande"),
            orderable=False,
            template_code='<a href="../order?order_id={{value}}">{{value}}</a>',
        )
        date_passation_ec = Column(orderable=False)
        no_fournisseur_fr = Column(orderable=False)
        intitule_fournisseur_fr = Column(orderable=False)
        objet_depense_ec = Column(orderable=False)
        bloc_note = TemplateColumn(verbose_name=_("Bloc note"), orderable=False, template_code='{{value|safe}}')
        lignes = Column(verbose_name=_("Lignes non soldées"), orderable=False)
        engage = Column(verbose_name=_("Mt Engagé"), orderable=False)
        liquide = Column(verbose_name=_("Mt Liquidé"), orderable=False)
        interventions = TemplateColumn(
            verbose_name=_("Interventions"),
            orderable=False,
            template_code='{% for v in value %}{{ v }}<br>{% endfor %}',
        )
        score = Column(verbose_name=_("Score"), orderable=False)
        problemes = TemplateColumn(verbose_name=_("Problèmes"), orderable=False, template_code='{{value|safe}}')

    def _get_context_data(self, **kwargs):
        context = super()._get_context_data(**kwargs)

        gestionnaire = self.params['request_get'].get('gest')
        indicateur = self.params['request_get'].get('indic')

        context['intro_text'] = {
            'ok': _("Commandes sans problème détecté :"),
            'old_orders': _("Commande à relancer :"),
            'to_close_orders': _("Commandes avec des lignes à solder :"),
            'bad_orders': _("Commandes avec des erreurs de saisie :"),
        }[indicateur]

        orders = flawed_orders(gestionnaire)[indicateur]

        if orders:
            orders.sort(key=lambda a: a['score'], reverse=True)
            context['nb_flawed_orders'] = len(orders)
            context['flawed_orders'] = self.OrdersTable(orders)

        return context


class GestLightWidget(SimpleLightWidget):
    def _setup(self, **params):
        super()._setup(**params)

        try:
            data = get_last_data(self.data_code, self.data_params)
        except ValueError:
            data = None

        if data is None:
            self.params['color'] = 'gray'
        else:
            value = data.data
            if value > 0:
                self.params['color'] = self.alert_color
            else:
                self.params['color'] = 'green'


class GestTextWidget(SimpleTextWidget):
    def _setup(self, **params):
        super()._setup(**params)

        info_orders = 0
        try:
            if self.data_params.get('level') == 0:
                data = get_last_data(self.data_code, self.data_params)
                # For 'OK' labelled orders, also add all orders with only informative anomalies
                info_data = get_last_data(self.data_code, dict(self.data_params, level=1))
                if info_data is not None:
                    info_orders = info_data.data
            else:
                data = get_last_data(self.data_code, self.data_params)
        except ValueError:
            data = None

        if data is None:
            self.params['text'] = '-----'
        else:
            value = data.data + info_orders
            if value > 0:
                if info_orders:
                    self.params['text'] = _(
                        '<a href="../orders/?filters='
                        '[{{&quot;name&quot;%3A&quot;gest&quot;%2C'
                        '&quot;value&quot;%3A{{&quot;commande__startswith&quot;%3A+&quot;{}&quot;}}}},'
                        '{{&quot;name&quot;%3A&quot;anomaly_level_cmd&quot;%2C'
                        '&quot;value&quot;%3A{{&quot;analyse_cmd__max_level__lt&quot;%3A+2}}}}]">'
                        '{}&nbsp;Commande{}</a>'
                    ).format(
                        self.data_params['gest'],
                        value,
                        {False: '', True: 's'}[value > 1],
                    )
                else:
                    self.params['text'] = _(
                        '<a href="../orders/?filters='
                        '[{{&quot;name&quot;%3A&quot;gest&quot;%2C'
                        '&quot;value&quot;%3A{{&quot;commande__startswith&quot;%3A+&quot;{}&quot;}}}},'
                        '{{&quot;name&quot;%3A&quot;anomaly_level_cmd&quot;%2C'
                        '&quot;value&quot;%3A{{&quot;analyse_cmd__max_level&quot;%3A+{}}}}}]">'
                        '{}&nbsp;Commande{}</a>'
                    ).format(
                        self.data_params['gest'],
                        self.data_params['level'],
                        value,
                        {False: '', True: 's'}[value > 1],
                    )
            else:
                self.params['text'] = _("Aucune")


class GestGrid(GridWidget):
    # _template_mapping_add = {'asset_ooo': 'asset_ooo'}

    gest_list = ('IF', 'II', 'IM')

    def _setup(self, **params):
        super()._setup(**params)
        ...
        # try:
        #     self.params['indicators'] = {gest: flawed_orders(gest) for gest in self.gest_list}
        #     # self.params['flawed_orders'] = flawed_orders('IM')
        #     self.params['asset_ooo'] = False
        # except DatabaseError as exception:
        #     # Asset+ connection is Out Of Order !
        #     self.params['asset_ooo'] = str(exception)
        #     self._children[0].params['text'] = (
        #         '<div style="background-color:#ffe0a0;padding:8px;border:1px solid black;width:90%;height:100%;">'
        #         + '<b>Connexion à Asset+ impossible :</b><br>'
        #         + str(exception)
        #         + '</div>'
        #     )

    base_columns = 5

    base_children = tuple(
        [
            SimpleTextWidget._factory(default_text=''),
            SimpleTextWidget._factory(
                default_text='<center><b>Avec problème(s)</b><br>Commandes avec '
                'au moins un problème de saisie dans magh2 ou Asset+</center>'
            ),
            SimpleTextWidget._factory(
                default_text='<center><b>A solder</b><br>Commandes pour lesquelles'
                ' des interventions Asset+ sont terminées</center>'
            ),
            SimpleTextWidget._factory(
                default_text='<center><b>Anciennes</b><br>Commandes de plus de 6 mois, Peut-être à relancer</center>'
            ),
            SimpleTextWidget._factory(default_text='<center><b>Ok</b><br>Commandes sans problème détecté</center>'),
        ]
        + reduce(
            lambda a, b: a + b,
            (
                [
                    SimpleTextWidget._factory(default_text='Gestionnaire ' + gest),
                    LightAndTextWidget._factory(
                        base_children=(
                            GestLightWidget._factory(
                                data_code='nb-orders-flaws',
                                data_params={'gest': gest, 'level': 4},
                                alert_color='red',
                            ),
                            GestTextWidget._factory(
                                data_code='nb-orders-flaws',
                                data_params={'gest': gest, 'level': 4},
                            ),
                        )
                    ),
                    LightAndTextWidget._factory(
                        base_children=(
                            GestLightWidget._factory(
                                data_code='nb-orders-flaws',
                                data_params={'gest': gest, 'level': 3},
                                alert_color='orange',
                            ),
                            GestTextWidget._factory(
                                data_code='nb-orders-flaws',
                                data_params={'gest': gest, 'level': 3},
                            ),
                        )
                    ),
                    LightAndTextWidget._factory(
                        base_children=(
                            GestLightWidget._factory(
                                data_code='nb-orders-flaws',
                                data_params={'gest': gest, 'level': 2},
                                alert_color='yellow',
                            ),
                            GestTextWidget._factory(
                                data_code='nb-orders-flaws',
                                data_params={'gest': gest, 'level': 2},
                            ),
                        )
                    ),
                    LightAndTextWidget._factory(
                        base_children=(
                            GestLightWidget._factory(
                                data_code='nb-orders-flaws',
                                data_params={'gest': gest, 'level': 0},
                                alert_color='green',
                            ),
                            GestTextWidget._factory(
                                data_code='nb-orders-flaws',
                                data_params={'gest': gest, 'level': 0},
                            ),
                        )
                    ),
                ]
                for gest in gest_list
            ),
        )
    )


class FinanceHome(FinanceView, metaclass=WidgetPageMetaClass):
    name = 'home'
    label = _("Accueil")
    title = _("Portail de la Gestion Economique et Financière")
    template_name = 'finance/home.html'

    main_widget_class = GestGrid
    main_widget_class_bis = GestWidget

    # Shouldn't this __init__ part be in a WidgetPageMixin ??
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Shouldn't this setup be in a WidgetPageMixin ??
    def setup(self, request, *args, **kwargs):
        if request.GET.get('gest') and request.GET.get('indic'):
            self.main_widget = self.main_widget_class_bis()
        else:
            self.main_widget = self.main_widget_class()
        super().setup(request, *args, **kwargs)
        self.main_widget._setup(**self.view_params)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # This statement shouldn't be in a WidgetPageMixin ??
        context['main_widget'] = self.main_widget
        context['title'] = _("Commandes de maintenance externe - Biomédical")

        return context


class OrdersDiagnostic(FinanceView):
    name = 'orders-diag'
    label = _("Diagnostic")
    title = _("Analyse des commandes")
    template_name = 'common/basic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_widget'] = GestWidget()
        return context


class OrdersView(SmartPage):
    name = 'orders'
    label = _("Lignes de commandes")
    title = _("Lignes de commandes")
    # template_name = 'finance/orders.html'
    views_module = finance
    smart_view_config = 'orders'
    # smart_view_class = smart_view_factory('OrdersSmartView', {})  # OrdersSmartView
    permissions = {
        'EXP',
        'ACH',
        'DIS',
        'ARB',
        'ADM',
        'GES',
    }  # Todo : Définir une valeur par défaut à partir des droits de l'application
    smart_modes = {
        None: {'view': 'list'},
    }


class AnomalyWidget(HtmlWidget):
    """ """

    class Media:
        css = {'all': ['smart_view/css/analysis.css']}

    template_string = """<div class="widget level-{{ level }} message">{{ message }}</div>"""
    _template_mapping_add = {
        'message': 'message',
        'level': 'level',
        'code': 'code',
    }


class AnalyseWidget(ContainerWidget):
    """"""

    class Media:
        css = {'all': ['smart_view/css/analysis.css']}

    template_string = """<div class="widget analysis">{% if ok %}{{ ok|safe }}{% else %}
    {% for anomaly in anomalies %}{{ anomaly.widget }}{% endfor %}{% endif %}</div>"""
    _template_mapping_add = {'anomalies': 'anomalies', 'ok': 'ok'}

    def _setup(self, **params):
        super()._setup(**params)
        if 'anomalies' in self.params and self.params['anomalies']:
            self.params['ok'] = None
            for idx, anomaly in enumerate(self.params['anomalies']):
                print('anomaly+', idx)
                anomaly['widget'] = self._add_child(AnomalyWidget, 'anomaly-' + str(idx), anomaly)
        else:
            self.params['ok'] = _("<div class=\"widget level-0 message\">RAS</div>")
            self.params['anomalies'] = []


class OrderIdFormWidget(HtmlWidget):
    """Very basic widget (a simple form to get a order id)"""

    template_string = """<div class="widget"><form><input name="order_id"><button type="submit">Envoyer</button></form></div>"""


class OrderHeaderWidget(ContainerWidget):
    class Media:
        css = {
            'all': [
                'smart_view/css/simple_table.css',
            ]
        }

    template_string = """{% load l10n %}<div class="widget" id="{{ html_id }}">
        <tr>
            <th>N°</th><td class="key center">{{ header.commande }}</td>
            <th>Exercice</th><td>{{ header.exercice_ec|unlocalize }}</td>
            <th>Date passation</th><td>{{ header.date_passation_ec }}</td>
            <th>Founisseur</th><td>{{ header.no_fournisseur_fr|unlocalize }}</td><td>{{ header.intitule_fournisseur_fr }}</td>
            <th>Opération</th><td>{{ header.no_operation_op|unlocalize|default_if_none:"" }}</td>
                <td>{{ header.lib_operation_op|default_if_none:"" }}</td>
        </tr>
        <tr>
            <th>Objet dépense</th><td colspan="5">{{ header.objet_depense_ec|default_if_none:"" }}</td>
            <th>Bloc note</th><td colspan="5">{{ header.bloc_note|safe }}</td>
        </tr>
        {% if analyse_widget %}
            <tr><th colspan="2">Analyse ({{ header.analyse_cmd.timestamp }})</th><td colspan="10">{{ analyse_widget }}</td></tr>
        {% endif %}
    </div>"""
    _template_mapping_add = {
        'header': 'header',
        'analyse_widget': 'analyse_widget',
    }


class IntervWidget(HtmlWidget):
    class Media:
        css = {
            'all': [
                'smart_view/css/simple_table.css',
            ]
        }

    _template_mapping = {
        'no_intv': 'no_intv',
        'intv': 'intv',
        'db_err': 'db_err',
    }
    # observ/, code_tech/, da_int/, da_fin/, nu_imm, n_seri, n_marche/, nu_compte/, mt_engag/
    template_string = """{% if intv %}<div id="{{ html_id }}" class="widget"><table class="simple" style="width:95%;">
      <tr>
        <th>Intervention</th><th>Code UF</th><th>N° Inventaire</th><th>Technicien</th><th>Date début</th><th>Date fin</th>
        <th>Etat</th><th>Demande initiale</th><th>Commentaire technique</th><th>Documents</th>
      </tr>
      <tr>
        <td rowspan="3" class="key center">{{ no_intv }}</td><td>{{ intv.n_uf }}</td><td>{{ intv.nu_imm }}</td>
        <td>{{ intv.code_techn }}</td><td>{{ intv.da_int }}</td><td>{{ intv.da_fin }}</td><td>{{ intv.etat }}</td>
        <td rowspan="3">{{ intv.observ }}</td><td rowspan="3">{{ intv.observ2 }}</td><td rowspan="3">{{ intv.docs|safe }}</td>
      </tr>
      <tr>
        <th>Fournisseur</th><th>N° Série</th><th>Commande liée</th><th>Compte</th><th>Marché</th><th>Engagé</th>
      </tr>
      <tr>
        <td>{{ intv.code_four }} - {{ intv.fourni }}</td><td>{{ intv.n_seri }}</td><td>{{ intv.nu_bon_c }}</td>
        <td>{{ nu_compte }}</td><td>{{ n_marche }}</td><td>{{ intv.mt_engage }}</td>
      </tr>
    </table></div>
    {% else %}<div id="{{ html_id }}" class="widget analysis">
    <div class="widget level-3 message">Intervention {{ no_intv }} non accessible ({{ db_err }}) !</div></div>{% endif %}"""

    def _setup(self, **params):
        super()._setup(**params)
        try:
            self.params.update({'intv': get_intv(self.params['no_intv'])})
        except DatabaseError as exc:
            self.params['db_err'] = str(exc)


class OrderRowWidget(ContainerWidget):
    class Media:
        css = {
            'all': [
                'smart_view/css/simple_table.css',
            ]
        }

    template_string = """{% load l10n %}<div id="{{ html_id }}">
    <table class="simple" style="width:96%;margin:10px 2%;background-color:#eee;">
        <tr>
            <td class="center key" rowspan="8" style="width:5%;">{{ row.no_ligne_lc }}</td>
            <th colspan="2">Unité Fonctionnelle</th>
            <th style="width:12%;">N° Marché</th>
            <th style="width:12%;">Nomenclature</th>
            <th style="width:12%;">N° compte</th>
            <th style="width:35%;">Libellé</th>
        </tr>
        <tr>
            <td colspan="2" class="center">{{ row.no_uf_uf|unlocalize }} - {{ row.libelle_uf_uf }}</td>
            <td class="center">{{ row.no_marche_ma|unlocalize }}</td>
            <td></td>
            <td class="center">{{ row.no_compte_cp|unlocalize }}</td>
            <td rowspan="3">{{ row.libelle|safe }}</td>
        </tr>
        <tr>
            <th style="width:12%;">Qté commandée</th>
            <th style="width:12%;">Qté reçue</th>
            <th>Mt Engagé</th><th>Mt liquidé</th>
            <th>Soldé</th>
        </tr>
        <tr>
            <td class="number">{{ row.qte_cdee_lc }}</td>
            <td class="number">{{ row.qte_recue_lc }}</td>
            <td class="euros">{{ row.mt_engage_lc }} €</td>
            <td class="euros">{{ row.mt_liquide_lc|default_if_none:"---,--" }} €</td>
            <td>{{ row.lg_soldee_lc }}</td>
        </tr>
        {% if row.analyse_widget %}
            <tr>
                <th>Analyse ({{ row.analyse.timestamp }})</th>
                <td colspan="6">{{ row.analyse_widget }}</td>
            </tr>
        {% endif %}
        {% if row.intv_widgets %}
            <tr>
                <td colspan="6" style="background:#fff;">{% for widget in row.intv_widgets %}{{ widget }}{% endfor %}</td>
            </tr>
        {% endif %}
      </table>
    </div>"""
    _template_mapping_add = {
        'row': 'row',
    }

    def _setup(self, **params):
        super()._setup(**params)
        print("Row.params_process()...")

        # Analyse widget
        if self.params['row']['analyse']:
            self.params['row']['analyse_widget'] = self._add_child(AnalyseWidget, '-analyse', self.params['row']['analyse'])
            # date conversion (workaround test since it should always be a string :-( )
            if isinstance(self.params['row']['analyse']['timestamp'], str):
                self.params['row']['analyse']['timestamp'] = datetime.fromisoformat(self.params['row']['analyse']['timestamp'])
            if 'anomalies' in self.params['row']['analyse']:
                for idx, anomaly in enumerate(self.params['row']['analyse']['anomalies']):
                    if anomaly['code'] == '1L01':  # match code
                        self.params['row']['intv_widgets'] = self.params['row'].get('intv_widgets', []) + [
                            self._add_child(IntervWidget, '-interv-' + str(idx), {'no_intv': anomaly['data']['intv']})
                        ]

        # HTML-ize
        self.params['row']['libelle'] = self.params['row']['libelle'].replace('\n', '<br>')


class OrderWidget(ContainerWidget):
    template_string = """<div id="{{ html_id }}">
            {% if order %}
                <table class="simple" style="width:80%;margin:0 10%;background-color:#eee;">
                {{ order.header.widget }}
                <tr><td colspan="12" style="background:#fff;">
                {% for row in order.rows %}
                    {{ row.widget }}
                {% endfor %}
                </td></tr>
                </table>
            {% else %}
                Pas de commande avec ce n° : {{ order_id }}
            {% endif %}
        </div>"""
    _template_mapping_add = {'order': 'order'}

    def _setup(self, **params):
        super()._setup(**params)
        qs = self.params['smart_view'].get_base_queryset(view_attrs=self.params)
        qs = qs.filter(commande=self.params['order_id']).annotate(
            libelle_html=Replace(F('libelle'), Value('\n'), Value('<br>'), output_field=CharField())
        )
        if qs.count():
            # Order header
            header = (
                qs.values(
                    'gest_ec',
                    'no_cde_ec',
                    'exercice_ec',
                    'no_fournisseur_fr',
                    'intitule_fournisseur_fr',
                    'date_passation_ec',
                    'no_operation_op',
                    'lib_operation_op',
                    'commande',
                    'objet_depense_ec',
                    'bloc_note',
                    'analyse_cmd',
                )
                .distinct()
                .order_by('no_ligne_lc')[0]
            )

            # Add links if orders are cited & transform to a multilines html text
            header['bloc_note'] = re.sub(
                r"\b((?:[0-9A-Za-z][0-9A-Za-z])\d\d\d\d\d\d)\b",
                lambda a: '<a href="./?order_id=' + a.groups()[0] + '">' + a.groups()[0] + '</a>',
                header['bloc_note'].replace('\n', '<br>'),
            )

            # Order rows
            rows = qs.order_by('no_ligne_lc').values()
            self.params['order'] = {
                'rows': [
                    {'widget': self._add_child(OrderRowWidget, '-row-' + str(idx), {'row': row})} for idx, row in enumerate(rows)
                ],
            }
            if header['analyse_cmd']:
                self.params['order']['analyse_widget'] = self._add_child(AnalyseWidget, '-analyse', header['analyse_cmd'])
                # date conversion (workaround test since it should always be a string :-( )
                if isinstance(header['analyse_cmd']['timestamp'], str):
                    header['analyse_cmd']['timestamp'] = datetime.fromisoformat(header['analyse_cmd']['timestamp'])

            self.params['order']['header'] = {
                'widget': self._add_child(
                    OrderHeaderWidget,
                    'header',
                    {'header': header, 'analyse_widget': self.params['order'].get('analyse_widget')},
                ),
            }

            # Is there a associated invoice ?
            ...

        else:
            self.params['order'] = None

        # super().params_process()


class OrderView(BiomAidViewMixin, TemplateView):
    name = 'order'
    label = _("Commande")
    title = _("Commande")
    template_name = 'common/basic.html'
    permissions = {
        'EXP',
        'ACH',
        'DIS',
        'ARB',
        'ADM',
        'GES',
    }
    main_widget_class = OrderWidget

    def setup(self, request: HttpRequest, *args: list, **kwargs: dict):
        super().setup(request, *args, **kwargs)
        self.message = None
        if 'order_id' in request.GET:
            order_id = request.GET.get('order_id')
            if order_id:
                order_id = order_id.strip().upper().replace(' ', '').replace(' ', '')
                if len(order_id) > 2 and len(order_id) < 8:
                    order_id = order_id[:2] + (8 - len(order_id)) * '0' + order_id[2:]
                elif len(order_id) > 8:
                    self.message = _("Numéro de commande non conforme (trop long) : {}").format(order_id)
                elif len(order_id) <= 2:
                    self.message = _("Numéro de commande non conforme (trop court) : {}").format(order_id)
            OrdersView.smart_view_class._meta['appname'] = 'finance'
            self.smart_view = OrdersView.smart_view_class(prefix=self.url_prefix, view_params=self.view_params)
            self.order_id = order_id
            self.title = _("Commande {}").format(self.order_id)
            self.main_widget = OrderWidget(None, dict(self.view_params, order_id=self.order_id, smart_view=self.smart_view))
        else:
            self.smart_view = None
            self.order_id = None
            self.title = _("Commande à rechercher")
            self.main_widget = OrderIdFormWidget(None, self.view_params)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_widget'] = self.main_widget
        context['message'] = self.message
        return context


class OrderViewBak(FinanceView):
    name = 'order_bak'
    label = _("Commande")
    title = _("Commande")
    template_name = 'finance/order.html'

    class RowsTable(Table):
        class Meta:
            attrs = {'class': 'tables2', 'style': 'width:100%'}

        no_ligne_lc = Column(orderable=False)
        no_uf_uf = Column(orderable=False)
        libelle_uf_uf = Column(orderable=False)
        no_marche_ma = Column(orderable=False)
        nomenclature_lc = Column(orderable=False)
        compte_ordonnateur_cp = Column(orderable=False)
        libelle_html = TemplateColumn(verbose_name=_("Libellé"), orderable=False, template_code='{{value|safe}}')
        qte_cdee_lc = Column(orderable=False)
        qte_recue_lc = Column(orderable=False)
        mt_engage_lc = Column(orderable=False, attrs={'td': {'class': 'euros'}})
        mt_liquide_lc = Column(orderable=False, attrs={'td': {'class': 'euros'}})
        lg_soldee_lc = Column(orderable=False)

    class InvoicesTable(Table):
        class Meta:
            attrs = {'class': 'tables2', 'style': 'width:100%'}

        type = Column(orderable=False)
        fournisseur = Column(orderable=False)
        reference_facture = Column(orderable=False)
        emission = Column(orderable=False)
        reception = Column(orderable=False)
        n_engagement = Column(orderable=False)
        etat = Column(orderable=False)
        montant_eur_ttc = Column(orderable=False, attrs={'td': {'class': 'euros'}})
        dernier_commentaire = Column(orderable=False)

    class EqptTable(Table):
        FIELDS = (
            'n_imma',
            'n_order',
            'nom',
            'nom2',
            'marque',
            'typ_mod',
            'n_seri',
            'n_uf',
            'mes1',
            'fdg',
            'prix',
            'filler_eco_3',
            'n_order',
            'date_refor',
        )

        class Meta:
            attrs = {'class': 'tables2', 'style': 'width:100%'}

        n_imma = Column(verbose_name=_("Inventaire"), orderable=False)
        nom = Column(verbose_name=_("Nom"), orderable=False)
        nom2 = Column(verbose_name=_("Nom 2"), orderable=False)
        marque = Column(verbose_name=_("Marque"), orderable=False)
        typ_mod = Column(verbose_name=_("Modèle"), orderable=False)
        n_seri = Column(verbose_name=_("N° Série"), orderable=False)
        n_uf = Column(verbose_name=_("UF"), orderable=False)
        mes1 = Column(verbose_name=_("Mise en service"), orderable=False)
        fdg = Column(verbose_name=_("Fin de garantie"), orderable=False)
        prix = Column(verbose_name=_("Prix achat"), orderable=False)
        # filler_eco_1 = Column(verbose_name=_("Filler 1"), orderable=False)
        # filler_eco_2 = Column(verbose_name=_("Filler 2"), orderable=False)
        filler_eco_3 = Column(verbose_name=_("Code immo"), orderable=False)
        n_order = Column(verbose_name=_("Commande"), orderable=False)
        date_refor = Column(verbose_name=_("Réforme"), orderable=False)
        docs = TemplateColumn(orderable=False, template_code='{{value|safe}}')

    class IntvTable(Table):
        FIELDS = (
            'nu_int',
            'nu_imm',
            'da_int',
            'code_techn',
            'da_fin',
            'observ',
            'observ2',
            'observ3',
            'nu_bon_c',
        )

        class Meta:
            attrs = {'class': 'tables2', 'style': 'width:100%'}

        nu_int = Column(verbose_name=_("Intervention"), orderable=False)
        etat = Column(orderable=False)
        nu_imm = Column(verbose_name=_("Inventaire"), orderable=False)
        da_int = Column(verbose_name=_("Début intervention"), orderable=False)
        code_techn = Column(verbose_name=_("Technicien"), orderable=False)
        da_fin = Column(verbose_name=_("Fin intervention"), orderable=False)
        observ = Column(verbose_name=_("Demande initiale"), orderable=False)
        observ2 = Column(verbose_name=_("Commentaire technique"), orderable=False)
        observ3 = Column(verbose_name=_("Suivi"), orderable=False)
        nu_bon_c = Column(verbose_name=_("N° commande"), orderable=False)
        docs = TemplateColumn(orderable=False, template_code='{{value|safe}}')

    class ImmoTable(Table):
        FIELDS = (
            'fiche',
            'code',
            'libelle_du_bien_fi',
            'date_de_mise_en_service_fi',
            'duree_fi2',
            'no_uf_df',
            'libelle_uf_df',
            'qte_uf_df1',
            'repart_uf_df1',
            'actif_uf_df2',
        )

        class Meta:
            attrs = {'class': 'tables2', 'style': 'width:100%'}

        fiche = Column(verbose_name=_("Fiche"), orderable=False)
        code = Column(orderable=False)
        libelle_du_bien_fi = Column(verbose_name=_("Libellé"), orderable=False)
        date_de_mise_en_service_fi = Column(verbose_name=_("Date MES"), orderable=False)
        duree_fi2 = Column(verbose_name=_("Durée amort."), orderable=False)
        no_uf_df = Column(verbose_name=_("Code UF"), orderable=False)
        libelle_uf_df = Column(verbose_name=_("Libellé UF"), orderable=False)
        qte_uf_df1 = Column(verbose_name=_("Qté UF"), orderable=False)
        repart_uf_df1 = Column(verbose_name=_("Répart. UF"), orderable=False)
        actif_uf_df2 = Column(verbose_name=_("Actif"), orderable=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        OrdersView.smart_view_class._meta['appname'] = 'finance'
        sv = OrdersView.smart_view_class(prefix=self.url_prefix, view_params=self.view_params)

        order_id = self.request.GET.get('order_id')

        if order_id:
            order_id = order_id.strip().upper().replace(' ', '').replace(' ', '')
            if len(order_id) > 2 and len(order_id) < 8:
                order_id = order_id[:2] + (8 - len(order_id)) * '0' + order_id[2:]
            elif len(order_id) > 8:
                context['message'] = _("Numéro de commande non conforme (trop long) : {}").format(order_id)
            elif len(order_id) <= 2:
                context['message'] = _("Numéro de commande non conforme (trop court) : {}").format(order_id)

        if order_id:
            context['order_id'] = order_id

            qs = sv.get_base_queryset(view_attrs=self.view_params)
            qs = qs.filter(commande=order_id).annotate(
                libelle_html=Replace(F('libelle'), Value('\n'), Value('<br>'), output_field=CharField())
            )
            if qs.count():
                context['order'] = qs.values(
                    'gest_ec',
                    'no_cde_ec',
                    'exercice_ec',
                    'no_fournisseur_fr',
                    'intitule_fournisseur_fr',
                    'date_passation_ec',
                    'no_operation_op',
                    'lib_operation_op',
                    'commande',
                    'objet_depense_ec',
                    'bloc_note',
                ).distinct()[0]

                context['order']['bloc_note'] = re.sub(
                    r"\b((?:[0-9A-Za-z][0-9A-Za-z])\d\d\d\d\d\d)\b",
                    lambda a: '<a href="./?order_id=' + a.groups()[0] + '">' + a.groups()[0] + '</a>',
                    context['order']['bloc_note'].replace('\n', '<br>'),
                )
                # print(qs.values())

                context['rows_table'] = self.RowsTable(qs.order_by('no_ligne_lc').values())

                ext_facture_model = apps.get_model('extable', 'ExtFacture')
                f_qs = ext_facture_model.records.filter(commande=order_id)

                if f_qs.count():
                    context['invoices_table'] = self.InvoicesTable(f_qs.values())

                try:
                    equipements = set()

                    # ==================================================================================================

                    # 1 - Les interventions qui sont 'citées' dans le bloc note de la commande
                    interventions = set(re.compile(r"(\b\d\d\d\d\d+\b)").findall(context['order']['bloc_note']))

                    # 2 - On recherche les interventions (en cours et archivées) qui portent
                    #      ce numéro de commande en référence
                    interventions_qs = EnCours.records.using('gmao').filter(nu_bon_c=order_id).values_list('nu_int', flat=True)
                    if interventions_qs.count():
                        interventions_qs._fetch_all()
                        interventions = interventions.union(set(interventions_qs))
                    interventions_qs = BFt1996.records.using('gmao').filter(nu_bon_c=order_id).values_list('nu_int', flat=True)
                    if interventions_qs.count():
                        interventions_qs._fetch_all()
                        interventions = interventions.union(set(interventions_qs))

                    interventions_list = []
                    for intervention in interventions:
                        docs_qs = Docliste.records.using('gmao').filter(nu_int=intervention).values('nom_doc').distinct()
                        docs = []
                        if len(docs_qs):
                            docs += [dict(doc) for doc in docs_qs]

                        intv_qs = (
                            EnCours.records.using('gmao')
                            .filter(nu_int=intervention)
                            .values(*self.IntvTable.FIELDS, 'int_statut', 'lib_statut')
                        )
                        if len(intv_qs):
                            interventions_list.append(
                                dict(
                                    intv_qs[0],
                                    etat={
                                        None: _("Inconnu"),
                                        '1': _("Non visée"),
                                        '2': _("En cours"),
                                        '3': _("A récupérer"),
                                        '4': _("Définitive non archivée"),
                                    }[intv_qs[0]['int_statut'].strip()]
                                    + " : "
                                    + (intv_qs[0]['lib_statut'] if intv_qs[0]['lib_statut'] else '-'),
                                    docs='<br/>'.join(
                                        '<a href="../../common/attachment/gmao/librairie_ASSET/'
                                        + doc['nom_doc'].split('\\')[-1]
                                        + '" onclick="window.open(this.href); return false;">'
                                        + doc['nom_doc'].split('\\')[-1]
                                        + '</a>'
                                        for doc in docs
                                    ),
                                )
                            )

                        intv_qs = (
                            BFt1996.records.using('gmao')
                            .filter(nu_int=intervention)
                            .values(*self.IntvTable.FIELDS, 'int_statut', 'lib_statut')
                        )
                        if len(intv_qs):
                            interventions_list.append(
                                dict(
                                    intv_qs[0],
                                    etat="Archivée",
                                    docs='<br/>'.join(
                                        '<a href="../../common/attachment/gmao/librairie_ASSET/'
                                        + doc['nom_doc'].split('\\')[-1]
                                        + '" onclick="window.open(this.href); return false;">'
                                        + doc['nom_doc'].split('\\')[-1]
                                        + '</a>'
                                        for doc in docs
                                    ),
                                )
                            )
                            if intv_qs[0]['nu_imm']:
                                equipements.add(intv_qs[0]['nu_imm'])

                    if interventions_list:
                        context['interventions_table'] = self.IntvTable(interventions_list)

                    # ==================================================================================================
                    #  Recherche des immobilisations liés à la commande
                    # ==================================================================================================
                    immos_list = []

                    ext_immos_model = apps.get_model('extable', 'ExtImmobilisation')
                    immos_qs = ext_immos_model.records.filter(commande=order_id)

                    immos_list += immos_qs.values(*self.ImmoTable.FIELDS)

                    if immos_list:
                        context['immos_table'] = self.ImmoTable(immos_list)

                    # ==================================================================================================
                    #  Recherche des équipements liés à la commande
                    # ==================================================================================================
                    # Source des références aux équipements :
                    # - équipement sur lequel porte au moins une des interventions liées à la commande (fait en amont)
                    # - n° d'inventaire cité dans le bloc-note (utile ?)
                    # - n° d'inventaire cité dans une ligne de commande (fait)
                    # - équipement dont le N° de commande correspond à la commande examinée (fait)
                    # - equipement dont le n° d'inventaire correspond
                    #       à une fiche d'immobilisation portant ce n° de commande

                    # 1 - équipement dont le N° de commande correspond à la commande examinée (fait)
                    equipements_qs = BEq1996.records.using('gmao').filter(n_order=order_id)
                    if len(equipements_qs):
                        equipements = equipements.union(set(equipements_qs.values_list('n_imma', flat=True)))

                    # 2 - équipements cités dans les intitulés des lignes de commande
                    for ligne in qs:
                        for inv_re in inv_re_list:
                            equipements = equipements.union(set(inv_re.findall(ligne.libelle)))

                    # 5 - équipements liés aux fiches d'immobilisation (ou pas...)
                    equipements = equipements.union(set([immo['fiche'] for immo in immos_list]))

                    equipements_list = []
                    for equipement in sorted(list(equipements)):
                        docs_qs = Docliste.records.using('gmao').filter(n_imma=equipement).values('nom_doc').distinct()
                        docs = []
                        if len(docs_qs):
                            docs += [dict(doc) for doc in docs_qs]
                        equipements_qs = BEq1996.records.using('gmao').filter(n_imma=equipement).values(*self.EqptTable.FIELDS)
                        if len(equipements_qs):
                            equipements_list.append(
                                dict(
                                    equipements_qs[0],
                                    docs='<br/>'.join(
                                        '<a href="../../common/attachment/gmao/librairie_ASSET/'
                                        + doc['nom_doc'].split('\\')[-1]
                                        + '" onclick="window.open(this.href); return false;">'
                                        + doc['nom_doc'].split('\\')[-1]
                                        + '</a>'
                                        for doc in docs
                                    ),
                                )
                            )

                    context['equipements_table'] = self.EqptTable(equipements_list)

                except (DbError, ConnectionDoesNotExist) as db_err:
                    context['database_message'] = str(db_err)
                    print(str(db_err))

            else:
                if 'message' not in context:
                    context['message'] = _("Commande non trouvée dans la base")

        return context


class ImmobilisationsView(SmartPage):
    name = 'immobilisations'
    label = _("Immobilisations")
    title = _("Immobilisations")
    # template_name = 'finance/immobilisations.html'
    smart_view_config = 'assets'
    permissions = {
        'EXP',
        'ACH',
        'DIS',
        'ARB',
        'ADM',
        'GES',
    }
    smart_modes = {
        None: {'view': 'list'},
    }


class InvoicesView(SmartPage):
    name = 'invoices'
    label = _("Factures")
    title = _("Factures")
    smart_view_config = 'invoices'
    # smart_view_class = smart_view_factory('InvoicesSmartView', {'model':''})
    permissions = {
        'EXP',
        'ACH',
        'DIS',
        'ARB',
        'ADM',
        'GES',
    }
    smart_modes = {
        None: {'view': 'list'},
    }


class DemAssessmentView(SmartPage):
    name = 'dem-assessment'
    lable = _("Bilan demandes")
    title = _("Bilan demandes")
    smart_view_class = DemAssessmentSmartView
    permissions = {'ADM', 'P-ARB'}
    smart_modes = {
        None: {'view': 'list'},
    }


class ProgrammStudie(BiomAidViewMixin, TemplateView):
    """Vue admin du fichier de config toml"""

    application = 'finance'
    name = 'prog_studie'
    permissions = {
        'ADM',
        'MAN',
    }
    raise_exception = True  # Refuse l'accès par défaut (pas de demande de login)
    template_name = 'finance/config_studie.html'

    def datageneration(self):
        self.request_data = tomlkit.loads(pathlib.Path("finance/request.toml").read_text())
        """GEt Liste des programmes favoris"""
        self.etab = Etablissement.objects.all()
        self.discipline = Discipline.objects.all()
        self.programme_favori_bibl = self.request_data['PROGRAMME_LISTE']
        self.trigger = "home"
        return self

    def dispatch(self, request, *args, **kwargs):
        # context = self.get_context_data()  # unused
        self.url = "../prog_studie/"
        self.datageneration()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["trigger"] = self.trigger
        if self.trigger == "get_it":
            context["programmestcd"] = self.programmestcd  # TODO : a supprimer juste pour essais
            self.TCD(request)
        else:
            self.programme = Programme.objects.all()
            context["programme"] = self.programme
            context["url"] = self.url
            context["programme_favori_bibl"] = self.programme_favori_bibl
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        if 'save_listes' in request.POST:
            context = self.get_context_data()
            self.trigger = 'NONE'
            context["url"] = self.url
            self.save_listes(request)
            self.datageneration()
        elif 'get_it' in request.POST:
            context = self.get_context_data()
            self.programmestcd = request.POST.get("get_it") or None
            self.trigger = "get_it"
        return self.get(request, *args, **kwargs)

    def save_listes(self, request, *args, **kwargs):  # sauvegarde des listes de programmes favoris)
        for e in self.etab:
            for d in self.discipline:
                self.request_data['PROGRAMME_LISTE'][e.prefix][d.code]['liste'] = request.POST.get(
                    "programme_favori_bibl2-" + e.prefix + "-" + d.code
                )
        # print(self.request_data['PROGRAMME_LISTE'])
        with pathlib.Path('finance/request.toml').open('w') as f:
            f.write(tomlkit.dumps(self.request_data))  # sauvegarde des modifs dans le .toml (=commit true)
        return self

    def TCD(self, request, *arg, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.programmestcd is not None:
            programme_list = self.programmestcd.strip().split(',')
            print(programme_list)
            context["message"] = "filtre sur les programmes : " + str(programme_list)
            my_filter_qs = Q()
            for prog in programme_list:
                print(prog)
                my_filter_qs = my_filter_qs | Q(code=prog)
            filtre_programmes = Programme.objects.filter(my_filter_qs)
            print(filtre_programmes)
            # TODO SLICE le filtre programme
            qs = Previsionnel.objects.filter(programme=filtre_programmes)
            print(qs)
        else:
            print("si pas filtre")
            context["message"] = "Tous les programmes : aucun selectionné"
            qs = Previsionnel.objects.all()

        return self

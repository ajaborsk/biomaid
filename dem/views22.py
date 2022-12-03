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
import json

from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.db.models import F, IntegerField
from django.db.models.functions import Cast
from django.db.models.aggregates import Sum

from altair import Chart, Data, Color, Scale, Theta, Text

from common import config
from common.models import Uf
from common.base_views import BiomAidViewMixin
from dem.smart_views import DemandeEqptSmartView
from drachar.smart_views import PrevisionnelSmartView
from assetplusconnect.models import BEq1996

from smart_view.smart_page import SmartPage
from smart_view.smart_widget import ContainerWidget, AltairWidget


class RequestView(SmartPage):
    application = 'dem'
    name = 'request'
    label = _("Demandes")
    permissions = config.settings.DEM_DEMANDE_CREATION_ROLES
    record_ok_message = _("Demande {code} enregistrée avec succès")
    deleted_done_message = _("La demande {code} a été supprimée.")
    no_grant_to_delete_record_message = _("Vous n'avez pas les droits suffisants pour supprimer la demande {code}.")
    try_to_delete_wthout_confirm_message = _(
        "La demande {code} ne peut être supprimée sans passer par le formulaire de confirmation"
    )
    smart_view_class = DemandeEqptSmartView
    smart_modes = {
        # L'entrée None décrit le comportement par défaut (sans vue) car la page est aussi une vue !
        None: {
            'view': 'list',  # lister les objets du modèle est la vue par défaut
        },
        'create': {
            'view': 'create',  # Facultatif car c'est la vue par défaut si le nom est 'create"
            'title': _("Ajouter une demande"),
            'buttons': (
                {
                    'type': 'submit',
                    'label': _("Enregistrer et ajouter un autre élément"),
                    'value': 'record',
                    'redirect': 'create',
                    'redirect_url_params': lambda vp: vp['request_get'].urlencode(),
                },
                {
                    'type': 'reset',
                    'label': _("Réinitialiser le formulaire"),
                    'redirect_url_params': lambda vp: vp['request_get'].urlencode(),
                },
            ),
        },
        'update': {
            'args': (('pk', 'int'),),
            'title': _("Modifier la demande"),
            'buttons': (
                {
                    'type': 'submit',
                    'label': _("Enregistrer et continuer à modifier"),
                    'value': 'record-then-update',
                    'message': '',
                    # 'redirect': None,  # Attention : Redirection vers le mode None (mode par défaut)
                    'redirect': 'update',  # Attention : Redirection vers le mode None (mode par défaut)
                    'redirect_params': '{%load l10n%}{"pk":{{pk|unlocalize}}}',
                },
                {
                    'type': 'reset',
                    'label': _("Réinitialiser le formulaire"),
                },
            ),
        },
        'copy': {
            'title': _("Copier une demande"),
            'args': (('pk', 'int'),),
            'exclude': (),
            'next': 'create',  # Par défaut, l'action après avoir copié le contenu d'une instance, c'est d'en créer une nouvelle
            'buttons': (
                {
                    'type': 'submit',
                    'label': _("Enregistrer et ajouter un autre élément"),
                    'value': 'record',
                    'redirect': 'create',  # Attention : Redirection vers le mode None (mode par défaut)
                },
                {
                    'type': 'reset',
                    'label': _("Réinitialiser le formulaire"),
                },
            ),
        },
        'view': {
            'args': (('pk', 'int'),),
        },
        'ask-delete': {
            'title': _("Supprimer un élément"),
            'view': 'view',
            'args': (('pk', 'int'),),
            'next': 'delete',
            'buttons': (
                {
                    'type': 'submit',
                    'label': _("Confirmer la suppression"),
                    'value': 'delete',
                    'message': _("<br>Vous allez être redirigé vers le tableau."),
                    'redirect': None,  # Attention : Redirection vers le mode None (mode par défaut)
                },
            ),
        },
        'delete': {
            'args': (('pk', 'int'),),
            'view': 'view',
            # Back to the default view after delete
            'next': None,
        },
    }


class ParametricAnalyticWidget(ContainerWidget):
    base_children = (AltairWidget,)

    class Media:
        css = {
            'all': [
                'smart_view/css/parametric_analytic_widget.css',
            ]
        }

    template_name = 'smart_view/parametric_analytic_widget.html'
    _template_mapping_add = {
        'title': 'title',
        'filters': 'filters',
        'axes': 'axes',
    }

    def _setup(self, **kwargs):
        super()._setup(**kwargs)
        ...
        # self.children[0].params['chart'] = {}

    def _prepare(self):
        ...
        # Temporary implementation
        filters = self.params['filters']

        if self.params.get('data'):
            data = self.params['data']
        elif self.params.get('base_qs'):
            data = list(self.params['base_qs'].filter(**filters).values('pole_name', 'mon_total'))
        else:
            raise RuntimeError("No data specification")

        # base_chart =

        self.children[0].params['chart'] = (
            Chart(Data(values=data))
            .transform_joinaggregate(total='sum(mon_total)')
            .transform_calculate(percent='datum.mon_total / datum.total')
            .encode(
                theta=Theta('sum(percent):Q', stack=True),
                color=Color('pole_name' + ':O', scale=Scale(scheme='Category20')),
                tooltip=['pole_name:O', 'sum(percent):Q'],
            )
            .mark_arc(innerRadius=100)
            + Chart(Data(values=data))
            .transform_joinaggregate(total='sum(mon_total)')
            .transform_calculate(percent='datum.mon_total / datum.total')
            .encode(theta=Theta('sum(percent):Q', stack=True), detail='pole_name' + ':O')
            .mark_text(radius=340, size=16, color='black')
            .encode(text=Text('sum(percent):Q', format='.1%'))
        ).properties(width='container', height='container')

        super()._prepare()

    # def _get_context_data(self, **kwargs):
    #     context = super()._get_context_data(**kwargs)

    #     # context['title'] = '<< Le titre >>'
    #     # context['filters'] = {}  # ...
    #     # context['axes'] = {}  # ...

    #     return context


# class AllAssetsWidget(ParametricAnalyticWidget):
#     _template_mapping_add = {}

#     def _setup(self, **params):
#         super()._setup(**params)
#         self.params['qs'] = []
#         self.params['category'] = 'the_state'
#         self.params['x'] = {'field': 'num_dmd__code', 'type': 'ordinal', 'sort': '-y'}
#         self.params['y'] = 'age_previsionnel:Q'


class AllAssetsView(BiomAidViewMixin, TemplateView):
    application = 'dem'
    name = 'all-assets-view'
    title = _("Vision du parc installé")
    permissions = '__LOGIN__'
    template_name = 'smart_view/main_widget_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            widget_params = {'w_settings': json.loads(self.request.GET.get('settings', '{}'))}
        except json.JSONDecodeError:
            widget_params = {'w_settings': {}}

        widget_params['title'] = ''
        uf_dict = dict(Uf.objects.all().values_list('code', 'pole__nom'))
        qs = (
            BEq1996.objects.using('gmao')
            .filter(date_refor__isnull=True, v_fonc='BM')
            .values('n_uf')
            .annotate(mon_total=Sum(Cast('prix', IntegerField())))
            .values('n_uf', 'mon_total')
        )
        data_dict = {}

        for d in list(qs):
            nom_pole = uf_dict.get(d['n_uf'])
            if nom_pole:
                if nom_pole in data_dict:
                    data_dict[nom_pole] += d['mon_total']
                else:
                    data_dict[nom_pole] = d['mon_total']

        widget_params['data'] = [{'pole_name': k, 'mon_total': v} for k, v in data_dict.items()]
        # widget_params['base_qs'] = (
        #     DemandeEqptSmartView(prefix='dummy', view_params=self.view_params, appname='dem')
        #     .get_base_queryset(self.view_params)
        #     .annotate(pole_name=F('uf__pole__nom'), mon_total=Cast('montant_arbitrage', IntegerField()))
        # )
        widget_params['filters'] = {'programme__code__contains': 'BIO-'}
        widget_params['axes'] = {'color': 'pole_name:O', 'theta': 'sum(mon_total):Q'}

        context['main_widget'] = ParametricAnalyticWidget(params=dict(self.view_params, **widget_params))
        return context


class DemHistoryView(BiomAidViewMixin, TemplateView):
    application = 'dem'
    name = 'history-view'
    title = _("Historique des demandes")
    permissions = '__LOGIN__'
    template_name = 'smart_view/main_widget_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            widget_params = {'w_settings': json.loads(self.request.GET.get('settings', '{}'))}
        except json.JSONDecodeError:
            widget_params = {'w_settings': {}}

        widget_params['title'] = ''
        widget_params['base_qs'] = (
            PrevisionnelSmartView(prefix='dummy', view_params=self.view_params, appname='drachar')
            .get_base_queryset(self.view_params)
            .annotate(pole_name=F('uf__pole__nom'), mon_total=Cast('budget', IntegerField()))
        )
        widget_params['filters'] = {'programme__code__contains': 'BIO-'}
        widget_params['axes'] = {'color': 'pole_name:O', 'theta': 'sum(mon_total):Q'}

        context['main_widget'] = ParametricAnalyticWidget(params=dict(self.view_params, **widget_params))
        return context


class CurrentRequestsView(BiomAidViewMixin, TemplateView):
    application = 'dem'
    name = 'current-request-view'
    title = _("Analyse demandes en cours")
    permissions = '__LOGIN__'
    template_name = 'smart_view/main_widget_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            widget_params = {'w_settings': json.loads(self.request.GET.get('settings', '{}'))}
        except json.JSONDecodeError:
            widget_params = {'w_settings': {}}

        widget_params['title'] = ''
        widget_params['base_qs'] = (
            DemandeEqptSmartView(prefix='dummy', view_params=self.view_params, appname='dem')
            .get_base_queryset(self.view_params)
            .annotate(pole_name=F('uf__pole__nom'), mon_total=Cast('montant_arbitrage', IntegerField()))
        )
        widget_params['filters'] = {'programme__code': 'BIO-23-PC', 'mon_total__gt': 500}
        widget_params['axes'] = {'color': 'pole_name:O', 'theta': 'sum(mon_total):Q'}

        context['main_widget'] = ParametricAnalyticWidget(params=dict(self.view_params, **widget_params))
        return context


class ArbitrationHelpView(BiomAidViewMixin, TemplateView):
    application = 'dem'
    name = 'arbitration-help-view'
    title = _("Aide à l'arbitrage")
    permissions = '__LOGIN__'
    template_name = 'smart_view/main_widget_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            widget_params = {'w_settings': json.loads(self.request.GET.get('settings', '{}'))}
        except json.JSONDecodeError:
            widget_params = {'w_settings': {}}

        widget_params['title'] = ''
        widget_params['base_qs'] = (
            DemandeEqptSmartView(prefix='dummy', view_params=self.view_params, appname='dem')
            .get_base_queryset(self.view_params)
            .annotate(pole_name=F('uf__pole__nom'), mon_total=Cast('enveloppe_allouee', IntegerField()))
        )
        widget_params['filters'] = {}
        widget_params['axes'] = {}

        context['main_widget'] = ParametricAnalyticWidget(params=dict(self.view_params, **widget_params))
        return context

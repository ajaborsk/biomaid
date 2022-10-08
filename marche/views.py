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

from django.db.models import Q, Sum, Count
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from django_pandas.io import read_frame
from django_tables2 import tables, columns
from django_tables2.export import TableExport

# Create your views here.
from common.base_views import BiomAidViewMixin
from finance.views import OrdersView
from marche.smart_views import ExceptionMarcheSmartView, MarcheSmartView
from smart_view.smart_page import SmartPage
import marche


class MarcheView(BiomAidViewMixin, TemplateView):
    # Droits de base pour toutes les vues de l'application. A modifier par héritage au besoin.
    permissions = {
        'EXP',
        'ACH',
        'DIS',
        'ARB',
        'ADM',
    }

    # Nom de l'application
    application = 'marche'

    # Titre général de l'application
    application_title = _("Achats et marchés")

    # module dans lequel il faut chercher la liste des vues (pour le menu)
    views_module = marche

    def main_tour_steps(self, context):
        return super().main_tour_steps(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MarcheHome(MarcheView):
    name = 'home'
    label = _("Accueil")
    title = _("Portail des achats et des marchés")
    template_name = 'marche/home.html'


class MarcheProcedures(MarcheView):
    name = 'procedures'
    label = _("Procédures")
    title = _("Gestion/Suivi des procédures d'achat")
    template_name = 'common/base.html'


class HMTable(tables.Table):

    # cc = columns.Column(verbose_name=_("Montant"), attrs={'td':{'class':'money'}})
    fournisseur = columns.Column(verbose_name=_("Fournisseur"))
    m_2017 = columns.Column(verbose_name=_("2017 (€)"), attrs={'td': {'class': 'euros'}})
    m_2018 = columns.Column(verbose_name=_("2018 (€)"), attrs={'td': {'class': 'euros'}})
    m_2019 = columns.Column(verbose_name=_("2019 (€)"), attrs={'td': {'class': 'euros'}})
    m_2020 = columns.Column(verbose_name=_("2020 (€)"), attrs={'td': {'class': 'euros'}})
    m_2021 = columns.Column(verbose_name=_("2021 (€)"), attrs={'td': {'class': 'euros'}})
    m_2022 = columns.Column(verbose_name=_("2022 (€)"), attrs={'td': {'class': 'euros'}})
    m_Tous = columns.Column(verbose_name=_("Tous (€)"), attrs={'td': {'class': 'euros'}})

    c_2017 = columns.Column(verbose_name=_("2017"), attrs={'td': {'class': 'right'}})
    c_2018 = columns.Column(verbose_name=_("2018"), attrs={'td': {'class': 'right'}})
    c_2019 = columns.Column(verbose_name=_("2019"), attrs={'td': {'class': 'right'}})
    c_2020 = columns.Column(verbose_name=_("2020"), attrs={'td': {'class': 'right'}})
    c_2021 = columns.Column(verbose_name=_("2021"), attrs={'td': {'class': 'right'}})
    c_2022 = columns.Column(verbose_name=_("2022"), attrs={'td': {'class': 'right'}})
    c_Tous = columns.Column(verbose_name=_("Tous"), attrs={'td': {'class': 'right'}})

    class Meta:
        # model = apps.get_model('extable', 'ExtCommande')
        # template_name = "django_tables2/bootstrap.html"

        # fields = ('intitule_fournisseur_fr','cc')
        pass


class HorsMarchePluriannuel(MarcheView):
    name = 'hors-marche-pluriannuel'
    label = _("Hors Marché")
    title = _("Gestion/Suivi du Hors Marché")
    template_name = 'marche/hors-marche-pluriannuel.html'

    def get(self, request, *args, **kwargs):
        OrdersView.smart_view_class._meta['appname'] = 'finance'
        sv = OrdersView.smart_view_class(prefix=self.url_prefix, view_params=self.view_params)
        self.qs = sv.get_base_queryset(view_attrs=self.view_params)

        hm = (
            self.qs.order_by()
            .filter(
                # On enlève la Trésorerie Principale
                ~Q(no_fournisseur_fr=33034),
                # N° de Marché non saisi
                Q(no_marche_ma='0'),
                Q(gest_ec__in=self.request.GET.getlist('gest_ec')),
                Q(compte_ordonnateur_cp__in=self.request.GET.getlist('compte_ordonnateur_cp')),
            )
            .values('exercice_ec', 'intitule_fournisseur_fr')
            .annotate(amount=Sum('mt_liquide_lc'), nb=Count('id'))
        )
        df = read_frame(hm)
        if len(df):
            dfp = df.pivot_table(
                index='intitule_fournisseur_fr',
                columns='exercice_ec',
                aggfunc={'amount': sum, 'nb': sum},
                margins=True,
                margins_name="Tous",
                fill_value=0.0,
            ).fillna(0)
            table = HMTable(
                [
                    dict(
                        {'fournisseur': f},
                        **{'m_' + str(y[1]): dfp.loc[f].loc[y] for y in dfp.loc[f].index if y[0] == 'amount'},
                        **{'c_' + str(y[1]): dfp.loc[f].loc[y] for y in dfp.loc[f].index if y[0] == 'nb'},
                    )
                    for f in dfp.index
                ],
                order_by=self.request.GET.get('sort'),
                request=self.request,
            )
            table.paginate(per_page=10000)
            self.hm_table = table
        else:
            self.hm_table = None

        export_format = request.GET.get("_export", None)
        if TableExport.is_valid_format(export_format) and self.hm_table:
            exporter = TableExport(export_format, self.hm_table)
            return exporter.response("table.{}".format(export_format))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form_parts'] = {
            'gest_ec': {
                'label': _("Gestionnaires"),
                'values': [
                    {
                        'label': v,
                        'value': v,
                        'set': v in self.request.GET.getlist('gest_ec') or not self.request.GET.getlist('gest_ec'),
                    }
                    for v in list(self.qs.all().values_list('gest_ec', flat=True).distinct())
                ],
            },
            'compte_ordonnateur_cp': {
                'label': _("Comptes"),
                'values': [
                    {
                        'label': v,
                        'value': v,
                        'set': v in self.request.GET.getlist('compte_ordonnateur_cp')
                        or not self.request.GET.getlist('compte_ordonnateur_cp'),
                    }
                    for v in list(
                        self.qs.filter(gest_ec__in=self.request.GET.getlist('gest_ec'))
                        .values_list('compte_ordonnateur_cp', flat=True)
                        .distinct()
                    )
                ],
            },
        }

        context['hm_table'] = self.hm_table

        return context


class Marche(SmartPage):
    application = 'marche'  # Todo : découvrir la valeur à partir du module (= de l'application Django)
    name = 'marches'  # Todo : Deviner une valeur par défaut à partir du nom de la classe
    label = _("Marchés")  # Todo : Deviner une valeur par défaut à partir du nom de la classe (moins pertinent que pour name)
    title = _("Gestion des marchés")

    permissions = {
        'EXP',
        'ACH',
        'DIS',
        'ARB',
        'ADM',
    }  # Todo : Définir une valeur par défaut à partir des droits de l'application
    # module dans lequel il faut chercher la liste des vues (pour le menu)
    views_module = marche

    smart_view_class = MarcheSmartView


class AutorisationLocale(SmartPage):
    application = 'marche'
    name = 'exception_marche'
    label = _("Autorisations locales")
    title = _("Autorisations locales de hors-marché")
    permissions = '__LOGIN__'

    smart_view_class = ExceptionMarcheSmartView

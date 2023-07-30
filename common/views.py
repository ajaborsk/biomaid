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
import os
import logging
import tempfile
from os import path
from os.path import exists
from copy import deepcopy

import altair
import pysftp
import tomlkit
import pathlib

from altair import Chart, Data
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from tomlkit.toml_file import TOMLFile

from django.db.models import Q, OuterRef, TextField
from django.db.models.functions import Concat, Cast, JSONObject
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import gettext as _
from django.apps import apps

from django.db.models import F, Value

import common
from analytics.data import get_data
from common.base_views import BiomAidViewMixin
from dem.smart_views import CampagneSmartView
from importationdata.views import BddImportation, FileImportation
from common.forms import (
    UserProfileForm,
    FournisseurForm,
    MarqueForm,
    TypeForm,
    CompteForm,
    UfForm,
    PoleForm,
    ServiceForm,
    CentreResponsabiliteForm,
    SiteForm,
    EtablissementForm,
)
from common.models import (
    Discipline,
    Uf,
    UserUfRole,
    Service,
    Pole,
    CentreResponsabilite,
    Site,
    Etablissement,
    Fournisseur,
    # ContactFournisseur,
    # DataFournisseurGEF,
    Alert,
    Marque,
    Type,
    Compte,
)
from common.smart_views import MyAlertsSmartView, ProgrammeSmartView, RoleScopeSmartView, FournisseurSmartView

from common.db_utils import MyAlertsWidget, StringAgg
from smart_view.smart_page import SmartPage
from smart_view.smart_widget import (
    AltairWidget,
    DemoPieChartWidget,
    HtmlWidget,
    LightAndTextWidget,
    RepartirWidget,
    SimpleLightWidget,
    SimpleTextWidget,
    VueWidget,
)

logger = logging.getLogger(__name__)


def debug(*args, **kwargs):
    logger.debug(' '.join(map(str, args)))


# Page d'erreur (imcompatibilité Internet Explorer)
def no_ie_view(request, **kwargs):
    return render(request, 'common/no_ie.html')


def redirect_to_home(request, url_prefix=None):
    return redirect('dem:home', url_prefix=url_prefix)


def redirect_to_kos_home(request, url_prefix=None):
    return redirect('dem:tvx-home', url_prefix=url_prefix)


class AttachmentView(View):
    """Easy, slow and (quite) dirty static file server.
    This is MUCH slower and consume a lot of memory/power than using regular
    file serving via nginx or your reverse proxy"""

    def get(self, request, *args, **kwargs):
        root = common.config.get('attachment_roots', {}).get(kwargs.get('root'))

        if root:
            if root.startswith('sftp://'):
                sftp_dsn, base_path = root[7:].split(':')
                username, servername = sftp_dsn.split('@')
                with pysftp.Connection(servername, username=username) as sftp:
                    with sftp.cd(base_path):
                        with tempfile.TemporaryDirectory() as tmp:
                            lpath = os.path.join(tmp, os.path.basename(kwargs['path']))
                            # print(os.listdir(tmp))
                            # print(f"lpath: {lpath}")
                            sftp.get(kwargs['path'], lpath, preserve_mtime=True)
                            if exists(lpath):
                                return FileResponse(open(lpath, 'rb'))
            else:
                filename = path.join(root, kwargs['path'])
                if exists(filename):
                    return FileResponse(open(filename, 'rb'))
        raise Http404("Fichier non trouvé")


class Profile(BiomAidViewMixin, TemplateView):
    permissions = '__LOGIN__'
    template_name = 'common/profile.html'

    def setup(self, request, **kwargs):
        self.message = None
        self.errors = None
        super().setup(request, **kwargs)

    def get(self, request, **kwargs):
        self.user_profile_form = UserProfileForm(instance=request.user)
        return super().get(request, **kwargs)

    def post(self, request, **kwargs):
        # mode 'POST' : remplir les formulaires avec les données reçues dans la requête
        self.user_profile_form = UserProfileForm(request.POST)
        # extension_user_profile_form = UserProfileForm(request.POST)

        # tenter d'enregistrer les données dans la base
        if self.user_profile_form.is_valid():
            # Les données saisies sont valides (ouf !)
            # Comme on est sur un formulaire qui ne permet pas la création d'enregistrement
            # et qui ne modifie qu'une partie des données de l'enregistrement
            # on utilise une stratégie différente de d'habitude :
            # 1 - On récupère les instances de la base :
            user = request.user
            # 2 - On met à jour les quelques champs qui sont dans le formulaire :
            user.first_name = self.user_profile_form.cleaned_data['first_name']
            user.last_name = self.user_profile_form.cleaned_data['last_name']
            user.email = self.user_profile_form.cleaned_data['email']
            user.initiales = self.user_profile_form.cleaned_data['initiales']
            user.intitule_fonction = self.user_profile_form.cleaned_data['intitule_fonction']
            user.titre = self.user_profile_form.cleaned_data['titre']
            user.tel_dect = self.user_profile_form.cleaned_data['tel_dect']
            user.tel_fixe = self.user_profile_form.cleaned_data['tel_fixe']
            user.tel_mobile = self.user_profile_form.cleaned_data['tel_mobile']
            # 3 - On sauvegarde les enregistrements dans la base :
            user.save()

            self.message = "Modifications enregistrées"
        else:
            self.message = "Erreur d'enregistrement ; un champ est mal renseigné"
            # TODO: Tester cette partie du code avec des erreurs
            self.errors = self.user_profile_form.errors.get_json_data()
            self.errors.update(self.user_profile_form.errors.get_json_data())

        return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            message=self.message,
            errors=self.errors,
            user_profile_form=self.user_profile_form,
        )
        return context


class SimpleScalarWidget(HtmlWidget):
    template_string = (
        '<div id="{{ html_id }}" style="'
        'text-align:center;font-size:{{ font_size }}px;display:flex;'
        'flex-direction:column;width:100%;height:100%;justify-content:space-evenly;'
        '"><div style="color:{{ text_color }}">{{ prefix }}&nbsp;{{ scalar }}&nbsp;{{ suffix }}</div></div>'
    )
    PARAMS_ADD = ('font_size', 'text_color', 'scalar', 'prefix', 'suffix')
    _template_mapping_add = {
        'text_color': 'text_color',
        'font_size': 'font_size',
        'prefix': 'prefix',
        'suffix': 'suffix',
        'scalar': 'scalar',
    }

    label = _("Donnée simple")
    help_text = _("Donnée unique (nombre)")
    manual_params = {
        'font_size': {'label': 'Taille du texte', 'type': 'int'},
        'text_color': {'label': "Couleur du texte", 'type': 'color'},
        'prefix': {'label': "Préfixe", 'type': 'string'},
        'suffix': {'label': "Suffixe", 'type': 'string'},
    }

    def _setup(self, **params):
        super()._setup(**params)
        self.params['prefix'] = self.params.get('prefix', '')
        self.params['suffix'] = self.params.get('suffix', '')
        self.params['scalar'] = get_data('common.user-active-alerts', all_params=self.params)


class PrevisionnelParExpertWidget(AltairWidget):
    label = _("Nb prévisionnels par expert")

    @staticmethod
    def manual_params(params):
        return {
            'discipline': {
                'label': "Discipline",
                'type': 'choice',
                'choices': list(Discipline.objects.filter(cloture__isnull=True).values_list('code', 'nom')),
            },
        }

    def _setup(self, **params):
        super()._setup(**params)

        qs = get_data('drachar.previsionnel-par-expert', all_params=self.params)
        category = altair.Color('nom_expert', type='nominal', title="Chargé d'opération")
        value = 'nombre:Q'
        self.params['chart'] = (
            Chart(Data(values=list(qs)))
            .transform_calculate(
                url=reverse('drachar:previsionnel', kwargs={'url_prefix': params['url_prefix']})
                + '?filters=['
                + '{"name":+"expert",+"value":+{"expert":+'
                + altair.datum.expert
                + '}},+{"name":+"solder_ligne",+"value":+{"solder_ligne":+false}}]'
            )
            .encode(theta=value, color=category, href='url:N', tooltip=[category, 'nombre:Q'])
            .mark_arc(tooltip=True)
            .properties(width='container', height='container')
            .configure_view(strokeWidth=0)
        )


class MontantPrevisionnelParExpertWidget(AltairWidget):
    label = _("Montant prévisionnel par expert")

    @staticmethod
    def manual_params(params):
        return {
            'discipline': {
                'label': "Discipline",
                'type': 'choice',
                'choices': list(Discipline.objects.filter(cloture__isnull=True).values_list('code', 'nom')),
            },
        }

    def _setup(self, **params):
        super()._setup(**params)

        qs = get_data('drachar.montant-previsionnel-par-expert', all_params=self.params)
        category = 'nom_expert:N'
        value = 'montant_total:Q'
        self.params['chart'] = (
            Chart(Data(values=list(qs)))
            .encode(
                theta=value,
                color=altair.Color(category),
            )
            .mark_arc(tooltip=True)
            .properties(width='container', height='container')
            .configure_view(strokeWidth=0)
        )


class VueGridWidget(VueWidget):
    class Media:
        css = {
            'all': [
                'smart_view/css/vue-grid-layout.css',
                'smart_view/css/vega-widget.css',
            ]
        }
        js = [
            'smart_view/js/vue-grid-layout.umd.min.js',
            'smart_view/js/vega@5.min.js',
            'smart_view/js/vega-lite@4.min.js',
            'smart_view/js/vega-embed@6.min.js',
        ]

    default_grid_layout = [
        {
            'i': 0,
            'x': 0,
            'y': 1,
            'w': 2,
            'h': 2,
            'show_title': True,
            'title': 'Simple text widget',
            'w_class': 'simple_text',
            'w_params': '{"text":"Simple text"}',
        },
        {
            'i': 1,
            'x': 2,
            'y': 1,
            'w': 1,
            'h': 2,
            'show_title': False,
            'title': 'Yes2',
            'w_class': 'simple_light',
            'w_params': '{"color":"green"}',
        },
        {
            'i': 2,
            'x': 3,
            'y': 1,
            'w': 1,
            'h': 3,
            'show_title': True,
            'title': 'Yes3',
            'w_class': 'light_and_text',
            'w_params': '{"text":"Alerte !","color":"red"}',
        },
        {'i': 3, 'x': 4, 'y': 1, 'w': 1, 'h': 4, 'show_title': False, 'title': 'Yes4', 'w_class': 'a_repartir', 'w_params': '{}'},
    ]
    template_name = 'smart_view/smart_widget_vue_grid.html'
    available_widgets = {
        'simple_text': SimpleTextWidget,
        'my_alerts': MyAlertsWidget,
        'demo_pie_chart': DemoPieChartWidget,
        'simple_light': SimpleLightWidget,
        'light_and_text': LightAndTextWidget,
        'a_repartir': RepartirWidget,
        'simple_scalar': SimpleScalarWidget,
        'nb_previsionnel_par_expert': PrevisionnelParExpertWidget,
        'montant_previsionnel_par_expert': MontantPrevisionnelParExpertWidget,
    }

    def __init__(self, *args, **kwargs):
        if 'contents' in kwargs:
            self.contents = kwargs['contents']
            del kwargs['contents']
        else:
            self.contents = None

        if 'portal_name' in kwargs:
            self.portal_name = kwargs['portal_name']
            del kwargs['portal_name']
        else:
            self.portal_name = 'common'

        if isinstance(self.contents, str):
            self.config_name = self.contents
            self.contents = common.config.get(self.config_name)
            if self.contents is None:
                logging.warning("Portal home contents '{}' not found in config files.".format(self.config_name))
            elif not isinstance(self.contents, dict):
                logging.warning("Portal home contents '{}' is not a dict.".format(self.config_name))
            elif 'layout' not in self.contents:
                logging.warning("Portal home contents '{}' does not have a 'layout' entry.".format(self.config_name))
        else:
            self.config_name = 'cockpit'

        if not isinstance(self.contents, dict) or 'layout' not in self.contents:
            logging.warning("Using fallback layout for portal home content (not using {}).".format(repr(self.contents)))
            self.contents = {'layout': self.default_grid_layout}

        try:
            for widget in self.contents['layout']:
                if 'w_params' in widget and not isinstance(widget['w_params'], str):
                    # convert w_params to a JSON string (if needed)
                    widget['w_params'] = json.dumps(widget['w_params'])
        except TypeError:
            logging.warning(
                "Using fallback layout for portal home content (layout is not iterable: {}).".format(repr(self.contents['layout']))
            )
            self.contents = {'layout': self.default_grid_layout}

        self.editable = self.contents.get('editable', True)
        self.columns = self.contents.get('columns', 16)
        self.rows = self.contents.get('rows', 32)
        self.v_spacing = self.contents.get('v_spacing', 12)
        self.h_spacing = self.contents.get('h_spacing', 12)

        super().__init__(*args, **kwargs)

    def _get(self, request, *args, **kwargs):
        layout = json.loads(request.GET['layout'])
        r_layout = {}
        for widget in layout:
            if widget.get('w_class') in self.available_widgets:
                params = json.loads(widget.get('w_params'))
                w = self.available_widgets[widget.get('w_class')](
                    html_id=self.html_id + '-' + str(widget.get('i')), params=dict(self.params, **params)
                )
                r_layout[widget['i']] = {'html': w._as_html(html_only=True)}
                if isinstance(w, AltairWidget):
                    # print("Altair widget", widget)
                    r_layout[widget['i']]['altair'] = w.altair_data
            else:
                r_layout[widget['i']] = {'html': 'Not found'}
        return JsonResponse({'ok': 'it s me !', 'layout': r_layout})

    def _get_as_toml(self, request, cockpit_name, *args, **kwargs):
        toml_doc = tomlkit.TOMLDocument()
        grid_layout = self.contents['layout']
        if self.editable:
            if not request.GET.get('reset'):
                try:
                    grid_layout = self.params['user_preferences'][self.portal_name + '.my-cockpit.grid-layout']
                except KeyError:
                    pass
        base_cfg = {}
        cfg = base_cfg
        if not cockpit_name:
            cockpit_name = self.config_name
        while '.' in cockpit_name:
            root, cockpit_name = cockpit_name.split('.', 1)
            cfg[root] = {}
            cfg = cfg[root]
        cfg[cockpit_name] = {
            'layout': deepcopy(grid_layout),
            'rows': self.rows,
            'columns': self.columns,
            'h_spacing': self.h_spacing,
            'v_spacing': self.v_spacing,
        }
        if self.editable:
            cfg[cockpit_name]['editable'] = True
            cfg[cockpit_name]['available_widgets'] = list(self.available_widgets.keys())
        else:
            cfg[cockpit_name]['editable'] = False
        for widget in cfg[cockpit_name]['layout']:
            widget['w_params'] = json.loads(widget['w_params'])
        toml_doc.update(base_cfg)
        return HttpResponse(toml_doc.as_string(), content_type='text/plain; charset=utf-8')

    def _get_context_data(self, **kwargs):
        context = super()._get_context_data(**kwargs)
        available_widgets = []
        grid_layout = self.contents['layout']
        if self.editable:
            if not self.params['request_get'].get('reset'):
                try:
                    grid_layout = self.params['user_preferences'][self.portal_name + '.my-cockpit.grid-layout']
                except KeyError:
                    pass
            for k, v in self.available_widgets.items():
                label = k
                help_text = ""
                manual_params = {}
                if hasattr(v, 'label'):
                    label = v.label
                if hasattr(v, 'help_text'):
                    help_text = v.help_text
                if hasattr(v, 'manual_params'):
                    if callable(v.manual_params):
                        manual_params = v.manual_params(self.params)
                    else:
                        manual_params = v.manual_params

                available_widgets.append(
                    {
                        'w_class': k,
                        'label': label,
                        'help_text': help_text,
                        'm_params': manual_params,
                    }
                )
        context['grid_params'] = {
            'portal_name': self.portal_name,
            'columns': self.columns,
            'rows': self.rows,
            'v_spacing': self.v_spacing,
            'h_spacing': self.h_spacing,
            'editable': self.editable,
            'init_layout': grid_layout,
            'settings_url': reverse('common:api_user_settings', kwargs={'url_prefix': 'portal-config'}),
            'available_widgets': available_widgets,
            'widget_defs': {w['w_class']: w for w in available_widgets},
        }
        return context


class BiomAidCockpit(BiomAidViewMixin, TemplateView):
    application = 'common'
    name = 'cockpit'
    title = _("")
    permissions = '__LOGIN__'
    template_name = 'smart_view/main_widget_page.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets = {}

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.main_widget = VueGridWidget(
            params=self.view_params, contents=self.portal.get('home-contents'), portal_name=self.url_prefix.split('-', 1)[0]
        )
        self.widgets[self.main_widget.html_id] = self.main_widget

    def get(self, request, *args, **kwargs):
        # Small trick to get toml text response (ready to cut/paste in a config file :-)
        if 'get_toml' in request.GET:
            return self.main_widget._get_as_toml(request, request.GET['get_toml'], *args, **kwargs)

        if 'id' in request.GET and request.GET['id'] in self.widgets:
            return self.widgets[request.GET['id']]._get(request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_widget'] = self.main_widget
        return context


class BiomAidAccount(BiomAidViewMixin, TemplateView):
    permissions = '__LOGIN__'
    template_name = 'common/account.html'


class BiomAidAbout(BiomAidViewMixin, TemplateView):
    permissions = '__PUBLIC__'
    template_name = 'common/about.html'


# ======================================================================================================================
#
# ======================================================================================================================


class Error403View(BiomAidViewMixin, TemplateView):
    name = 'error-403'
    permissions = '__PUBLIC__'
    template_name = 'common/forbidden.html'

    # def get_context_data(self, **kwargs):
    #     # print("403 pre-ctx : ", kwargs)
    #     context = super().get_context_data(**kwargs)
    #     # context['url_prefix'] = self.request.path.split('/')[1]
    #     # print("403 ctx : ", context['url_prefix'])
    #     return context

    def get(self, request, **kwargs):
        # print("403 get : ", kwargs, request.path.split('/')[1])
        context = self.get_context_data()
        if kwargs['exception'].args:
            context['exception_message'] = kwargs['exception'].args[0]
        return render(request, self.template_name, context, status=403)


class Error404View(BiomAidViewMixin, TemplateView):
    name = 'error-404'
    permissions = '__PUBLIC__'
    template_name = 'common/not_found.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data(), status=404)


# page d'accueil
class BiomAidAccueil(BiomAidViewMixin, TemplateView):
    application = 'common'
    name = 'home-main'
    permissions = '__PUBLIC__'
    template_name = 'common/cockpit.html'


# page d'accueil / Cockpite
# class BiomAidCockpit(BiomAidViewMixin, TemplateView):
#     application = 'common'
#     name = 'cockpit'
#     permissions = '__PUBLIC__'
#     template_name = 'common/cockpit.html'


def get_layout_field(layout, path):
    if len(path) == 2:
        return layout[path[0]]
    else:
        return get_layout_field(layout[path[0]], path[1:])


class Preferences(BiomAidViewMixin, TemplateView):
    application = 'common'
    name = 'preferences'
    permissions = '__LOGIN__'
    template_name = 'common/preferences.html'
    title = _('Mes préferences')

    def initial(self, form_class):
        paths = {
            get_layout_field(form_class.helper.layout, p).attrs['data-user-setting-path']: f
            for p, f in form_class.helper.layout.get_field_names()
        }
        return {f: self._user_settings[p] for p, f in paths.items()}

    def get(self, request, **kwargs):
        return super().get(request, **kwargs)

    def post(self, request, **kwargs):
        # print(request.POST)

        self.form = apps.get_app_config('common').user_settings_forms['main'](
            request.POST,
            initial=self.initial(apps.get_app_config('common').user_settings_forms['main']),
            user_roles=self._user_roles,
        )

        paths = {
            f: get_layout_field(self.form.helper.layout, p).attrs['data-user-setting-path']
            for p, f in self.form.helper.layout.get_field_names()
        }
        # pprint(paths)

        # pprint(self.form.changed_data)

        if self.form.is_valid():
            for field in self.form.changed_data:
                self._user_settings[paths[field]] = self.form.cleaned_data[field]
        else:
            # TODO, handle form error...
            ...

        return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'form'):
            context['form'] = self.form
        else:
            context['form'] = apps.get_app_config('common').user_settings_forms['main'](
                initial=self.initial(apps.get_app_config('common').user_settings_forms['main']),
                user_roles=self._user_roles,
            )
        return context


class UserAlerts(SmartPage):
    # application = 'common'
    name = 'user-alerts'
    permissions = '__LOGIN__'
    title = _('Mes alertes')
    smart_view_class = MyAlertsSmartView
    smart_modes = {
        None: {'view': 'list'},
    }

    def get(self, request, **kwargs):
        # Marque mes alertes non vues comme vues !
        Alert.objects.filter(destinataire=request.user, date_lecture__isnull=True).update(date_lecture=timezone.now())
        return super().get(request)


class AdminHome(BiomAidViewMixin, TemplateView):
    """Vue principale pour l'administration du portail"""

    application = 'common'
    name = 'admin-home'
    permissions = {'ADM'}
    raise_exception = True  # Refuse l'accès par défaut (pas de demande de login)
    template_name = 'common/admin_home.html'
    # Seuls les utilisateurs faisant partie du management du projet peuvent
    # accéder à cette page
    # def test_func(self):
    #     return permissions.can(self.request.user, 'admin', 'access')

    def get_context_data(self, **kwargs):
        # logger.error("log test : Page admin error message")
        # logger.warning("log test : Page admin warning message")
        # logger.info("log test : Page admin info message")
        # logger.debug("log test : Page admin debug message")
        context = super().get_context_data(**kwargs)
        # context.update(dem_context(self.request))
        context['etablissements'] = Etablissement.objects.all()
        # TODO : changer le moyen de déterminer le contexte avec le congig.tml et non le .ini
        context['link_structure'] = {}
        for etab in context['etablissements']:
            config = TOMLFile('local/config.toml').read()
            # etabprefix = etab.prefix  # Unused // Commented on 2022-02-03 by Alexandre
            # Original code :
            # context['link_structure'].update({etab.prefix: config['LINK'][etab.prefix]['structure']})

            # Modified code: default to 'OFF' if prefix not found in configuration file
            #   (from AJA on 2021-12-20 / 2022-02-03)
            if not config['LINK'].get(etab.prefix):
                context['link_structure'].update({etab.prefix: config['LINK']["DEFAUT"]['structure']})
                self.message = "attention, établissement %s" % etab.nom + " n'a pas de prefix"
            else:
                context['link_structure'].update({etab.prefix: config['LINK'].get(etab.prefix)['structure']})

            # if common.config.settings.LIEN_GEF['link_structure.'+str(etab.prefix)] == 'ON'
            #       or common.config.settings.LIEN_GEF['link_structure.'+str(etab.prefix)] == 'FILE':
            #    context['link_structure'] = True
            # else:
            #    context['link_structure'] = False
        return context


class ManagerHome(BiomAidViewMixin, TemplateView):
    """Vue principale pour l'administration du portail"""

    application = 'common'
    name = 'manager-home'
    permissions = {'MAN', 'ADM'}
    raise_exception = True  # Refuse l'accès par défaut (pas de demande de login)
    template_name = 'common/manager_home.html'
    # Seuls les utilisateurs faisant partie du management du projet peuvent
    # accéder à cette page
    # def test_func(self):
    #     return permissions.can(self.request.user, 'admin', 'access')

    def get_context_data(self, **kwargs):
        # logger.error("log test : Page admin error message")
        # logger.warning("log test : Page admin warning message")
        # logger.info("log test : Page admin info message")
        # logger.debug("log test : Page admin debug message")
        context = super().get_context_data(**kwargs)
        # context.update(dem_context(self.request))
        context['etablissements'] = Etablissement.objects.all()
        # TODO : changer le moyen de déterminer le contexte avec le congig.tml et non le .ini
        context['link_structure'] = {}
        for etab in context['etablissements']:
            config = TOMLFile('local/config.toml').read()
            # etabprefix = etab.prefix  # Unused // Commented on 2022-02-03 by Alexandre
            # Original code :
            # context['link_structure'].update({etab.prefix: config['LINK'][etab.prefix]['structure']})

            # Modified code: default to 'OFF' if prefix not found in configuration file
            #   (from AJA on 2021-12-20 / 2022-02-03)
            if not config['LINK'].get(etab.prefix):
                context['link_structure'].update({etab.prefix: config['LINK']["DEFAUT"]['structure']})
                self.message = "attention, établissement %s" % etab.nom + " n'a pas de prefix"
            else:
                context['link_structure'].update({etab.prefix: config['LINK'].get(etab.prefix)['structure']})

            # if common.config.settings.LIEN_GEF['link_structure.'+str(etab.prefix)] == 'ON'
            #       or common.config.settings.LIEN_GEF['link_structure.'+str(etab.prefix)] == 'FILE':
            #    context['link_structure'] = True
            # else:
            #    context['link_structure'] = False
        return context


class AdminConfig(BiomAidViewMixin, TemplateView):
    """Vue admin du fichier de config toml"""

    application = 'common'
    name = 'admin-config'
    permissions = {'ADM'}
    raise_exception = True  # Refuse l'accès par défaut (pas de demande de login)
    template_name = 'common/admin_config.html'

    def datageneration(self):
        self.config_data = tomlkit.loads(pathlib.Path("local/config.toml").read_text())
        """Pour la structure"""
        self.etab = Etablissement.objects.all()
        self.linkstruc_bibl = {}
        for e in self.etab:
            self.linkstruc_bibl.update({e.prefix: self.config_data['LINK'].get(e.prefix, {'structure': 'OFF'})['structure']})
        self.linkstrucfile_bibl = {}
        for e in self.etab:
            self.linkstrucfile_bibl.update(
                {e.prefix: self.config_data['LINKED_FILES'].get(e.prefix, {'structure': 'OFF'})['structure']}
            )
        self.dailyupdate_bibl = {}
        for e in self.etab:
            self.dailyupdate_bibl.update(
                {e.prefix: self.config_data['DAILY_UPDATE'].get(e.prefix, {'structure': 'NA'})['structure']}
            )
        """Pour les information des bases de données"""
        self.infosbdd = self.config_data['BDD']
        return self

    def dispatch(self, request, *args, **kwargs):
        # context = self.get_context_data()  # unused
        self.url = "../admin_config/"
        self.datageneration()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["url"] = self.url
        context["linkstruc_bibl"] = self.linkstruc_bibl
        context["linkstrucfile_bibl"] = self.linkstrucfile_bibl
        context["dailyupdate_bibl"] = self.dailyupdate_bibl
        context["bdd"] = self.infosbdd
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["url"] = self.url
        self.save(request)
        self.datageneration()
        return self.get(request, *args, **kwargs)

    def save(self, request, *args, **kwargs):
        print("avant")
        print(self.config_data)
        for e in self.etab:
            self.config_data['LINK'].get(e.prefix, {'structure': 'OFF'})['structure'] = request.POST.get(
                "linkstruc_bibl-" + e.prefix
            )
        for e in self.etab:
            self.config_data['LINKED_FILES'].get(e.prefix, {'structure': 'OFF'})['structure'] = request.POST.get(
                "linkstrucfile_bibl-" + e.prefix
            )
        for e in self.etab:
            self.config_data['DAILY_UPDATE'].get(e.prefix, {'structure': 'NA'})['structure'] = request.POST.get(
                "dailyupdate_bibl-" + e.prefix
            )
        """Pour les information des bases de données"""

        # TODO : faire pour BDD
        self.infosbdd = self.config_data['BDD']

        print("après")
        print(self.config_data)
        with pathlib.Path('local/config.toml').open('w') as f:
            f.write(tomlkit.dumps(self.config_data))  # sauvegarde des modifs dans le .toml (=commit true)
        return self


class CalendrierView(SmartPage):
    application = 'common'
    name = 'calendrier'
    permissions = {'ADM'}
    smart_view_class = CampagneSmartView
    title = "Calendriers / Campagnes (c)"


# class ProgrammeView(SimpleSmartViewMixin, CommonView):
#     application = 'common'
#     name = 'programme'
#     permissions = {'ADM'}
#     smart_view_class = ProgrammeSmartView
#     title = "Programmes / Enveloppes (c)"


class ProgrammePage(SmartPage):
    application = 'common'  # Todo : découvrir la valeur à partir du module (= de l'application Django)
    name = 'programme'  # Todo : Deviner une valeur par défaut à partir du nom de la classe
    label = _("Programmes")  # Todo : Deviner une valeur par défaut à partir du nom de la classe (moins pertinent que pour name)
    title = _("Gestion des programmes / enveloppes")

    permissions = {
        'EXP',
        'ACH',
        'DIS',
        'ARB',
        'ADM',
        'MAN',
    }  # Todo : Définir une valeur par défaut à partir des droits de l'application
    # module dans lequel il faut chercher la liste des vues (pour le menu)
    views_module = common

    smart_view_class = ProgrammeSmartView


class RoleScopeView(SmartPage, BiomAidViewMixin, TemplateView):
    application = 'common'
    name = 'role'
    permissions = {'ADM'}
    smart_view_class = RoleScopeSmartView
    title = _("Rôles")


# ==================================================================================================================
# GESTION DES FOURNISSEURS
# ==================================================================================================================


# def gestion_fournisseurs(request, url_prefix=None):
#     """vue de gestion de la table des Fournisseurs et du Canret Fournisseur
#         - en methode GET : Affichage du tableau des Contacts livraison actifs (date fin = null) et des options disponibles
#         - en methode POST :
#             * status "ajout" : load le template avec formulaire d'ajout
#             * status "enregistrer" : code pour l'enregistrement des données du formulaire d'ajout
#             * status "modifierid" : load le template de Modification avec chargement des données de l'id correspondant
#             * status "update" : code pour la modification des données du formulaire d'ajout
#                 § chargement des données du forme qui sont testées :
#                     ¤ si Nom et prénom fournis existent déjà et que l'id ne correspond pas à celui en cours dans la BDD,
#                      modification rejetée
#                     ¤ si Nom et prénom fournis n'existent pas, modification acceptée
#             * status "supprimerid" : load le template de Suppression avec chargement des données de l'id correspondant
#             * status "delete" : code pour la suppresion des données du formulaire d'ajout
#                 § il s'agit d'un chargement de la date de fin (pas de "delete" réellement de la base de donnée
#             * status "gestion" : retour au tableau de gestion après le POST
#     l'ensemble de ces status sont renvoyés avec des <button> dans l'unique template. Les status sont ensuite gérés par
#     des boucles {% if %} dans le templates.
#     """
#     # affichage des items disponibles dans la table et des options possibles.
#     if request.method == 'GET':
#         status = 'gestion'
#         if status == 'gestion':
#             list_data_fournisseur = DataFournisseurGEF.objects.order_by('etablissement', 'intitule_fournisseur').filter(
#                 Q(cloture__isnull=True)
#             )
#             list_fournisseurs = Fournisseur.objects.order_by('nom').filter(Q(cloture__isnull=True))
#             list_contact_fournisseur = ContactFournisseur.objects.order_by('societe').filter(Q(cloture__isnull=True))
#             context = drachar_context(request, title=_("GESTION DES FOURNISSEURS"), url_prefix=url_prefix)
#             context.update(
#                 {
#                     "status": status,
#                     "list_fournisseurs": list_fournisseurs,
#                     "list_data_fournisseur": list_data_fournisseur,
#                     'list_contact_fournisseur': list_contact_fournisseur,
#                 }
#             )
#         # TODO: vérifier l'utilité de cette partie du code :
#         elif status == 'ajout':
#             contactform = ContactLivForm(request.POST or None)
#             context = drachar_context(request, title=_("GESTION DES FOURNISSEURS"), url_prefix=url_prefix)
#             context.update(
#                 {
#                     "Contactform": contactform,
#                     "status": status,
#                 }
#             )
#     # Requetes POST pour Modification, Ajout et Suppression
#     elif request.method == 'POST':
#         print(request.POST)
#         context = drachar_context(request)
#         status = request.POST.get("status")
#         supprimerfourid = request.POST.get("supprimerfour") or None
#         modifierfourid = request.POST.get("modifierfour") or None
#         supprimercontactid = request.POST.get("supprimercontfour") or None
#         modifiercontactid = request.POST.get("modifiercontfour") or None
#         selectfournisseur = request.POST.get("selectfournisseur") or None
#         print(status)
#         print(supprimerfourid)
#         print(modifierfourid)
#         print(supprimercontactid)
#         print(modifiercontactid)
#         print(selectfournisseur)
#         context.update(
#             {
#                 "status": status,
#             }
#         )
#         # CODE DE MODIFICATION, SUPPRESSION, D'UN CONTACT FOURNISSEUR EXISTANT
#         if modifiercontactid is not None:  # load template intermédiaire formulaire modificatif
#             print("modifiercontactid")
#             status = "modifier"  # => template modifier
#             contactfour_instance = ContactLivraison.objects.get(pk=modifiercontactid)
#             contactfour_form = ContactLivForm(instance=contactfour_instance)
#             context = drachar_context(request, title=_("MODIFIER LE CONTACT N° %s" % modifiercontactid), url_prefix=url_prefix)
#             print(contactfour_instance)
#             context.update(
#                 {
#                     "contactfour_instance": contactfour_instance,
#                     "status": status,
#                     "modifiercontactid": modifiercontactid,
#                     "contactfour_form": contactfour_form,
#                 }
#             )
#         elif supprimercontactid is not None:  # load template intermédiaire confirmation suppression
#             print("supprimercontactid")
#             status = "supprimer"  # => template modifier
#             contactfour_instance = ContactLivraison.objects.get(pk=supprimercontactid)
#             context = drachar_context(request, title=_("SUPPRIMER LE CONTACT N° %s" % supprimercontactid),
#                       url_prefix=url_prefix)
#             contactfour_form = ContactLivForm(instance=contactfour_instance)
#               # pour mettre à jour le champs date fin qui est caché
#             context.update(
#                 {
#                     "contactfour_instance": contactfour_instance,
#                     "status": status,
#                     "supprimercontactid": supprimercontactid,
#                     "contactfour_form": contactfour_form,
#                 }
#             )
#
#         # CODE DE MODIFICATION, SUPPRESSION, AJOUT D'UN FOURNISSEUR GENERIQUE
#         if modifierfourid is not None:  # load template intermédiaire formulaire modificatif
#             print("modifierfour")
#             status = "modifierfour"  # => template modifier
#             fourgenerique_instance = Fournisseur.objects.get(pk=modifierfourid)
#             fourgenerique_form = FournisseurForm(instance=fourgenerique_instance)
#             context = drachar_context(
#                 request,
#                 title=_("MODIFIER LE FOURNISSEUR N° %s" % modifierfourid + ", " + fourgenerique_instance.nom),
#                 url_prefix=url_prefix,
#             )
#             print(fourgenerique_instance)
#             context.update(
#                 {
#                     "fourgenerique_instance": fourgenerique_instance,
#                     "status": status,
#                     "modifierfourid": modifierfourid,
#                     "fournisseurform": fourgenerique_form,
#                 }
#             )
#         elif supprimerfourid is not None:  # load template intermédiaire confirmation suppression
#             print("supprimefour")
#             status = "supprimerfour"  # => template modifier
#             fourgenerique_instance = Fournisseur.objects.get(pk=supprimerfourid)
#             context = drachar_context(
#                 request,
#                 title=_("SUPPRIMER LE FOURNISSEUR N° %s" % supprimerfourid + ", " + fourgenerique_instance.nom),
#                 url_prefix=url_prefix,
#             )
#             fourgenerique_form = FournisseurForm(
#                 instance=fourgenerique_instance
#             )  # pour mettre à jour le champs date fin qui est caché
#             context.update(
#                 {
#                     "fourgenerique_instance": fourgenerique_instance,
#                     "status": status,
#                     "supprimerfourid": supprimerfourid,
#                     "fourgenerique_form": fourgenerique_form,
#                 }
#             )
#         elif status == 'ajoutfournisseur':  # load template intermédiaire formulaire d'ajout fournisseur générique
#             print('ajoutfournisseur')
#             data = {'code_four': '000'}
#             fournisseurform = FournisseurForm(data)
#             context = drachar_context(request, title=_("AJOUTER UN FOURNISSEUR GENERIQUE"), url_prefix=url_prefix)
#             context.update(
#                 {
#                     "fournisseurform": fournisseurform,
#                     "status": status,
#                 }
#             )
#         elif status == 'ajoutcontactfour':  # load template intermédiaire formulaire d'ajout contact fournisseur
#             print('ajoutcontactfournisseur')
#             contactform = ContactFournisseur(request.POST or None)
#             context = drachar_context(request, title=_("AJOUTER UN CONTACT FOURNISSEUR"), url_prefix=url_prefix)
#             context.update(
#                 {
#                     "Contactform": contactform,
#                     "status": status,
#                 }
#             )
#         elif status == 'enregistrerfournisseur':  # code fonction d'enregistrement d'un fournisseur
#             fournisseurform = FournisseurForm(request.POST or None)
#             if fournisseurform.is_valid():
#                 post = fournisseurform.save(commit=False)
#                 post.code_four = fournisseurform.cleaned_data["code_four"]
#                 post.nom = fournisseurform.cleaned_data["nom"]
#                 try:  # test d'unicité dans les contacts non encore supprimés
#                     test = Fournisseur.objects.get(nom__iexact=post.nom, cloture__isnull=True)
#                     message = "impossible de faire cette modification : "
#                           "contact (nom&prenom) existe déjà voyez l'administrateur"
#                 except Fournisseur.DoesNotExist:  # pas de doublons, on sauvegarde
#                     post.save()
#                     post.code_four = post.id  # /!\ ici réenregistrement du code avec id créé après le .save
#                     post.save()
#                     message = "Enregistrement fait avec succès"
#
#                 status = "gestion"
#                 list_fournisseurs = Fournisseur.objects.order_by('nom').filter(Q(cloture__isnull=True))
#                 context = drachar_context(request,
#                       title=_("GESTION DES FOURNISSEURS DE LIVRAISON"), url_prefix=url_prefix)
#                 context.update(
#                     {
#                         "status": status,
#                         "list_fournisseurs": list_fournisseurs,
#                         "message": message,
#                     }
#                 )
#         elif status == "modifierfour":  # Code fonction de modification fournisseur générique
#             modifierid = request.POST.get("modifierfourid") or None
#             print(modifierid)
#             Instance = Fournisseur.objects.get(pk=modifierid)
#             form = FournisseurForm(request.POST or None)
#             if form.is_valid():
#                 Instance.code_four = form.cleaned_data["code_four"]
#                 Instance.nom = form.cleaned_data["nom"]
#                 try:
#                     test = Fournisseur.objects.get(nom__iexact=Instance.nom)
#                     if int(test.id) == int(modifierid):  # normal, c'est celui qu'on modifie
#                         Instance.save()
#                         message = "Modifications faites avec succès"
#                     else:  # pas normal, ce nom et prenom existent déjà sous une autre pk.
#                         message = "impossible de faire cette modification : "
#                                   "Fournisseur existe déjà voyez l'administrateur"
#                 except Fournisseur.DoesNotExist:  # normal, c'est celui qu'on modifie
#                     Instance.save()
#                     message = "Modifications faites avec succès"
#             # recharger la page Gestion
#             status = "gestion"
#             list_fournisseurs = Fournisseur.objects.order_by('nom').filter(Q(cloture__isnull=True))
#             context = drachar_context(request,
#                       title=_("GESTION DES FOURNISSEURS DE LIVRAISON"), url_prefix=url_prefix)
#             context.update(
#                 {
#                     "status": status,
#                     "list_fournisseurs": list_fournisseurs,
#                     "message": message,
#                 }
#             )
#         elif status == "supprimerfour":  # code fonction de suppression
#             supprimerid = request.POST.get("supprimerfourid") or None
#             Instance = Fournisseur.objects.get(pk=supprimerid)
#             Instance.cloture = timezone.now()
#             Instance.save(update_fields=['cloture'])
#
#             # recharger la page Gestion
#             message = "Fournisseur supprimer avec succès"
#             status = "gestion"
#             list_fournisseurs = Fournisseur.objects.order_by('nom').filter(Q(cloture__isnull=True))
#             context = drachar_context(request,
#                           title=_("GESTION DES FOURNISSEURS DE LIVRAISON"), url_prefix=url_prefix)
#             context.update(
#                 {
#                     "status": status,
#                     "list_fournisseurs": list_fournisseurs,
#                     "message": message,
#                 }
#             )
#
#     print('status : ' + str(status))
#     return render(request, "common/gestion_fournisseurs.html", context)


# ==================================================================================================================
# GESTION DES DATAs MARQUES, TYPES, Structure...
# ==================================================================================================================

# TODO : Faire de même pour Type, pour Comptes, Familles d'achat, CNEH,
class GestionData(BiomAidViewMixin, TemplateView, BddImportation):
    """Code pour gestion des items d'une table simple :Marques, Types,... en mode manuel
    class à exploiter dans une class maitresse disposant des paramètres automatisables :
    - nom du template à utiliser
    - titre de la page
    - model à utiliser : l'objet (pour les requetes) et son nom (pour la fonction update)
    - formulaire à utiliser
    - lien avec d'autres BDD #
    - %s pour les messages automatisés
    - les champs de comparaison pour test d'unicité lors d'ajout ou modification #
    """

    permissions = ('ADM',)

    def __init__(self):
        super().__init__()

        # par défaut
        self.etabprefix = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.titre_template
        return context

    # TODO : faire une fonction pour pouvoir choisir le formatage dans le tableau
    # AJA: Je ne comprends pas ce code qui est incorrect et ne semble pas utilisé. Commenté pour l'instant.
    # def formatter(records, formats):
    #     for record in records:
    #         record.exercice = record.exercice.strftime('%Y')
    #     return record

    def get(self, request, **kwargs):
        # recherche des filtres du queryset
        try:
            q_query = self.fonc_q_query(kwargs)  # fonction si récupération d'infos de l'url.
        except Exception:
            q_query = self.q_query
        # définition auto de l'URL :
        try:
            url = self.fonc_url(kwargs)
        except Exception:
            url = self.url
        # définition des paramètres de liens
        self.parametre_connexion(kwargs)
        if self.lien == 'OFF':  # configuré en mode manuel
            if request.GET.get("ajouter") is not None:
                status = 'ajouter'
                titre_template = 'Ajouter %s' % self.item_message
                form = self.form(request.GET)
                return render(
                    request,
                    self.template_name,
                    {
                        'form': form,
                        "lien": self.lien,
                        "status": status,
                        "title": titre_template,
                        "template_col_title": self.template_col_title,
                        "template_lig_var": self.template_lig_var,
                        "template_additional": self.template_additional,
                        "nbcol": self.nbcol,
                        "url": url,
                        "etabprefix": self.etabprefix,
                        **kwargs,
                    },
                )
            elif request.GET.get("modifier") is not None:
                titre_template = 'Modifier %s' % self.item_message
                kwargs['status'] = 'modifier'
                modifierid = request.GET.get("modifier") or None
                instance = self.model.objects.get(pk=modifierid)
                form = self.form(instance=instance)
                return render(
                    request,
                    self.template_name,
                    {
                        'form': form,
                        "instance": instance,
                        "lien": self.lien,
                        "title": titre_template,
                        "template_col_title": self.template_col_title,
                        "template_lig_var": self.template_lig_var,
                        "template_additional": self.template_additional,
                        "nbcol": self.nbcol,
                        "url": url,
                        "etabprefix": self.etabprefix,
                        **kwargs,
                    },
                )
            elif request.GET.get("supprimer") is not None:
                status = 'supprimer'
                titre_template = 'Supprimer %s' % self.item_message
                supprimerid = request.GET.get("supprimer") or None
                instance = self.model.objects.get(pk=supprimerid)
                form = self.form(instance=instance)
                return render(
                    request,
                    self.template_name,
                    {
                        'form': form,
                        'instance': instance,
                        "lien": self.lien,
                        "status": status,
                        "title": titre_template,
                        "template_col_title": self.template_col_title,
                        "template_lig_var": self.template_lig_var,
                        "template_additional": self.template_additional,
                        "nbcol": self.nbcol,
                        "etabprefix": self.etabprefix,
                        "url": url,
                        **kwargs,
                    },
                )
            else:
                status = "Main"
                titre_template = self.titre_template
                titre2 = "mode enregistrement manuel"
                list = self.model.objects.order_by(*self.ordre_affichage).filter(*q_query)
                return render(
                    request,
                    self.template_name,
                    {
                        "list": list,
                        "status": status,
                        "lien": self.lien,
                        "message": kwargs.get('message', None),
                        "title": titre_template,
                        "titre2": titre2,
                        "template_col_title": self.template_col_title,
                        "template_lig_var": self.template_lig_var,
                        "template_additional": self.template_additional,
                        "nbcol": self.nbcol,
                        "etabprefix": self.etabprefix,
                        "url": url,
                        **kwargs,
                    },
                )
        elif self.lien == 'ON' or self.lien == 'FILE':  # configuré en mode automatique
            status = "Main"
            titre_template = self.titre_template
            if self.lien == 'ON':
                titre2 = "mode connecté à BDD"
            elif self.lien == "FILE":
                titre2 = "mode import via un Fichier"
            list = self.model.objects.order_by(*self.ordre_affichage).filter(*q_query)
            # TODO : faire une fonction pour pouvoir choisir le formatage dans le tableau
            # GestionData.formatter(list, self.formats)
            print(url)
            return render(
                request,
                self.template_name,
                {
                    "list": list,
                    "lien": self.lien,
                    "status": status,
                    "message": kwargs.get('message', None),
                    "title": titre_template,
                    "titre2": titre2,
                    "template_col_title": self.template_col_title,
                    "template_lig_var": self.template_lig_var,
                    "template_additional": self.template_additional,
                    "nbcol": self.nbcol,
                    "etabprefix": self.etabprefix,
                    "url": url,
                    **kwargs,
                },
            )
        else:  # Remonté d'erreur fichier config
            message = (
                "Erreur dans la configuration, Contacter l'administrateur, "
                "le fichier de config est mal renseigné choisir ON ou OFF pour link_%s" % self.item_message
            )
            return render(request, self.template_name, {"message": message, "url": url})

    def post(self, request, *args, **kwargs):
        self.parametre_connexion(kwargs)
        if self.lien == 'OFF':  # configuré en mode manuel
            status = request.POST.get('status')
            if status == 'ajouter':  # Fonction Ajout
                form = self.form(request.POST)
                if form.is_valid():
                    item = form.save(commit=False)
                    try:  # test d'unicité dans les items de la table non encore supprimés
                        test = self.model.objects.get(**self.crit_unic_to_get(item))
                        # TODO : prévoir un dexieme critère d'unicité :
                        #   premier général, second sur un champs dimportance.
                        kwargs['message'] = "Impossible d'ajouter %s : %s existe déjà" % (
                            self.item_message,
                            self.item_message,
                        )
                    except self.model.DoesNotExist:  # pas de doublons, on sauvegarde
                        item.save()
                        form.save()
                        if self.template_additional is not None:
                            self.additional_def(request, item)
                        kwargs['message'] = "Enregistré avec succés"
                    return self.get(request, *args, **kwargs)
                else:
                    kwargs['message'] = _("Problème dans le formulaire : " + str(form.errors))
                    return self.get(request, *args, **kwargs)
            elif status == 'modifier':  # Fonction Modification
                modifierid = request.POST.get("modifierid") or None
                item = self.model.objects.get(pk=modifierid)
                form = self.form(request.POST or None, instance=item)
                if form.is_valid():
                    try:
                        test = self.model.objects.get(**self.crit_unic_to_get(item))
                        if int(test.id) == int(modifierid):  # normal, c'est celui qu'on modifie
                            form.save()
                            kwargs['message'] = "Modifications faites avec succès"
                        else:  # pas normal, existe déjà sous une autre pk.
                            kwargs['message'] = (
                                "impossible de faire cette modification : %s existe déjà voyez "
                                "l'administrateur" % self.item_message
                            )
                    except self.model.DoesNotExist:  # normal, c'est celui qu'on modifie
                        form.save()
                        kwargs['message'] = "Modifications faites avec succès"
                    return self.get(request, *args, **kwargs)
                else:
                    kwargs['message'] = _("Problème dans le formulaire : " + str(form.errors))
                    return self.get(request, *args, **kwargs)
            elif status == 'supprimer':  # Fonction Suppression
                supprimerid = request.POST.get("supprimerid") or None
                instance = self.model.objects.get(pk=supprimerid)
                instance.cloture = timezone.now()
                instance.save(update_fields=['cloture'])
                return self.get(request, *args, **kwargs)
        elif self.lien == 'ON':
            maj = request.POST.get("miseajour") or None
            if maj == "miseajour":
                BddImportation.update_def(self, request)
                return self.get(request, *args, **kwargs)
        elif self.lien == 'FILE':  # TODO : fonctions sepéciale de récupération de fichiers txt, excel...
            maj = request.POST.get("miseajour") or None
            if maj == "miseajour":
                FileImportation.update_def(self, request)
                return self.get(request, *args, **kwargs)
        else:  # Remonté d'erreur config lien BDD,
            kwargs['message'] = (
                "Erreur dans le fichier de configuration, Contacter l'administrateur, " "Erreur dans le fichier config"
            )
            return render(request, self.template_name, {"message": kwargs['message']})


class GestionMarques(GestionData):
    """Class maitresse utilisant GestionData"""

    ''' Paramètres de base '''
    url = "../gestion_marques/"
    # nom du template à utiliser (template gestiondata.html par défaut et automatisé à conserver sauf exception
    template_name = 'common/gestiondata.html'
    titre_template = "Marques : Liste"  # titre de la page
    model = Marque  # model à utiliser
    form = MarqueForm  # formulaire à utiliser
    item_message = "Marque"  # %s pour les messages automatisés
    ordre_affichage = [
        'nom'
    ]  # ordre d'affichage de la liste de la fct GET : ajouter dans l'ordre d'autres filtres :['filter1', 'filter2',...]
    template_col_title = ['ID', 'NOM']  # colonne à afficher dans le table
    template_lig_var = ['id', 'nom']  # champs correspondants aux colonnes dans le table
    template_additional = None
    nbcol = len(template_col_title)  # nombre de colonne du tableau
    q_query = [Q(cloture__isnull=True)]  # filtre de la liste du GET
    # critères de tests d'unicité avant enregistrement, suppression ou modification

    def crit_unic_to_get(self, item):
        return {
            'nom__iexact': getattr(item, "nom"),
            'cloture__isnull': True,
        }  # champs de comparaison pour tester les éventuels doublons / test d'unicité

    '''Cas particulier mode Automatique CONNEXION :'''
    # éléments de base à renseigner pour la class "GmaoImportation" :
    bdd = 'GMAO'  # Base de données à utiliser
    model_update = "Marque"  # fonction update à déclancher

    def parametre_connexion(self, kwargs):
        # TODO : utiliser le fichier config toml => config = TOMLFile('local/config.toml').read()
        self.lien = common.config.settings.LIEN_GMAO[
            'link_marque'
        ]  # lien avec d'autres BDD ou fichiers actif ? à renseigner dans fichier config.ini
        self.model_bdd = common.config.settings.GMAOTYPE['model_de_gmao']  # model de la GMAO utilisée (asset+, Optim...)
        self.app_bdd = common.config.settings.GMAOTYPE['app_gmao']  # model de la GMAO utilisée (asset+, Optim...)
        self.version_bdd = common.config.settings.GMAOTYPE['version_de_gmao']


class GestionTypes(GestionData):
    """Class maitresse utilisant GestionData"""

    # éléments de base à renseigner pour la class "GestionData" :
    ''' Paramètres de base '''
    url = "../gestion_types/"
    # nom du template à utiliser (template gestiondata.html par défaut et automatisé à conserver sauf exception
    template_name = 'common/gestiondata.html'
    titre_template = "Types : Liste"  # titre de la page
    model = Type  # model à utiliser
    form = TypeForm  # formulaire à utiliser
    item_message = "Type"  # %s pour les messages automatisés
    ordre_affichage = [
        'type',
        'marque',
    ]  # ordre d'affichage de la liste de la fct GET : ajouter dans l'ordre d'autres filtres :['filter1', 'filter2',...]
    template_col_title = [
        'ID',
        'TYPE',
        'MARQUE',
        'CNEH',
        "CLASSE",
    ]  # colonne à afficher dans le table
    template_lig_var = [
        'id',
        'type',
        'marque',
        'cneh_code',
        "classe_code",
    ]  # champs correspondants aux colonnes dans le table
    template_additional = None
    nbcol = len(template_col_title)  # nombre de colonne du tableau
    q_query = [Q(cloture__isnull=True)]  # filtre de la liste du GET

    # critères de tests d'unicité avant enregistrement, suppression ou modification
    def crit_unic_to_get(self, item):
        return {
            'type__iexact': getattr(item, "type"),
            'cloture__isnull': True,
        }  # champs de comparaison pour tester les éventuels doublons / test d'unicité

    '''Cas particulier mode Automatique CONNEXION :'''
    # éléments de base à renseigner pour la class "GmaoImportation" :
    bdd = 'GMAO'  # Base de données à utiliser
    model_update = "Type"  # fonction update à déclancher

    def parametre_connexion(self, kwargs):
        # TODO : utiliser le fichier config toml => config = TOMLFile('local/config.toml').read()
        self.lien = common.config.settings.LIEN_GMAO[
            'link_marque'
        ]  # lien avec d'autres BDD ou fichiers actif ? à renseigner dans fichier config.ini
        self.model_bdd = common.config.settings.GMAOTYPE['model_de_gmao']  # model de la GMAO utilisée (asset+, Optim...)
        self.app_bdd = common.config.settings.GMAOTYPE['app_gmao']  # model de la GMAO utilisée (asset+, Optim...)
        self.version_bdd = common.config.settings.GMAOTYPE['version_de_gmao']


class GestionComptes(GestionData):
    """Class maitresse utilisant GestionData"""

    # éléments de base à renseigner pour la class "GestionData" :
    ''' Paramètres de base '''
    url = "../gestion_comptes/"
    # nom du template à utiliser (template gestiondata.html par défaut et automatisé à conserver sauf exception
    template_name = 'common/gestiondata.html'
    titre_template = "Liste de Comptes"  # titre de la page
    model = Compte  # model à utiliser
    form = CompteForm  # formulaire à utiliser
    item_message = "Compte"  # %s pour les messages automatisés
    ordre_affichage = [
        'exercice',
        'lettre_budgetaire',
        'discipline',
        'code',
        'nom',
        'budget_montant',
    ]  # ordre d'affichage de la liste de la fct GET : ajouter dans l'ordre d'autres filtres :['filter1', 'filter2',...]
    template_col_title = [
        'EXERCICE',
        'BUDGET',
        'CODE',
        'NOM',
        'DISCIPLINE',
        'budget_montant',
    ]  # colonne à afficher dans le table
    template_lig_var = [
        'exercice',
        'lettre_budgetaire',
        'code',
        'nom',
        'discipline',
        'budget_montant',
    ]  # champs correspondants aux colonnes dans le table
    template_additional = None
    formats = {
        "date": "Y",
        "string": "",
        "None": "",
        "None": "",
        "None": "",
        "None": "",
    }
    nbcol = len(template_col_title)  # nombre de colonne du tableau
    q_query = [Q(cloture__isnull=True)]  # filtre de la liste du GET

    # critères de tests d'unicité avant enregistrement, suppression ou modification
    def crit_unic_to_get(self, item):
        return {
            'lettre_budgetaire__iexact': getattr(item, "lettre_budgetaire"),
            'code__iexact': getattr(item, "code"),
            'cloture__isnull': True,
        }  # champs de comparaison pour tester les éventuels doublons / test d'unicité

    '''Cas particulier mode Automatique CONNEXION :'''
    bdd = 'GEF'  # Base de données à utiliser
    model_update = "Compte"  # fonction update à déclancher

    def parametre_connexion(self, kwargs):
        # TODoO : passer en TOML
        self.lien = common.config.settings.LIEN_GEF['link_compte']
        self.model_bdd = common.config.settings.GEFTYPE['model_gef']
        self.version_bdd = common.config.settings.GEFTYPE['version_gef']
        self.app_bdd = common.config.settings.GEFTYPE['app_gef']
        self.fichier = common.config.settings.LIEN_GEF['file_compte']


class GestionUf(GestionData):
    """Class maitresse utilisant GestionData"""

    # éléments de base à renseigner pour la class "GestionData" :
    ''' Paramètres de base '''

    def fonc_url(self, kwargs):
        url = "../gestion_uf/" + str(kwargs.get('etabid')) + "/"  # fonction création d'URL en fonction de l'entrée
        return url

    # nom du template à utiliser (template gestiondata.html par défaut et automatisé à conserver sauf exception
    template_name = 'common/gestionstructure.html'
    titre_template = "Liste des Unités Fonctionnelles"  # titre de la page
    model = Uf  # model à utiliser
    form = UfForm  # formulaire à utiliser
    item_message = "Uf"  # %s pour les messages automatisés
    ordre_affichage = [
        'code',
        'nom',
        'service',
        'centre_responsabilite',
        'pole',
        'site',
        'etablissement',
        'cloture',
    ]  # ordre d'affichage de la liste de la fct GET : ajouter dans l'ordre d'autres filtres :['filter1', 'filter2',...]
    template_col_title = [
        'NUF',
        'Nom UF',
        'ETABLISSEMENT',
        'SERVICE',
        'CENTRE RESPONSABILITE',
        'SITE',
        'POLE',
        'DATE CLOTURE',
    ]  # colonne à afficher dans le table
    template_lig_var = [
        'code',
        'nom',
        'service',
        'centre_responsabilite',
        'pole',
        'site',
        'etablissement',
        'cloture',
    ]  # champs correspondants aux colonnes dans le table
    template_additional = None
    formats = {
        "string": "",
        "string": "",
        "None": "",
        "None": "",
        "None": "",
        "None": "",
        "date": "Y",
    }
    nbcol = len(template_col_title)  # nombre de colonne du tableau

    def fonc_q_query(self, kwargs):
        q_query = [Q(etablissement=kwargs.get('etabid'))]
        return q_query

    # critères de tests d'unicité avant enregistrement, suppression ou modification
    def crit_unic_to_get(self, item):
        return {
            'nom__iexact': getattr(item, "nom"),
            'code__iexact': getattr(item, "code"),
            'cloture__isnull': True,
        }  # champs de comparaison pour tester les éventuels doublons / test d'unicité

    '''Cas particulier mode Automatique CONNEXION :'''
    # éléments de base à renseigner pour la class "GmaoImportation" :
    bdd = 'GEF'  # Base de données à utiliser
    model_update = "structure"  # fonction update à déclancher

    def parametre_connexion(self, kwargs):
        self.etabprefix = Etablissement.objects.get(id=kwargs.get('etabid')).prefix
        config = TOMLFile('local/config.toml').read()
        self.lien = config['LINK'][self.etabprefix][self.model_update]
        self.model_bdd = config['BDD'][self.bdd]['model']
        self.version_bdd = config['BDD'][self.bdd]['version']
        self.app_bdd = self.model_bdd + "connect"
        if self.lien == "FILE":
            self.fichier = config['LINKED_FILES'][self.etabprefix][self.model_update]
        else:
            self.fichier = None


class GestionPole(GestionData):
    """Class maitresse utilisant GestionData"""

    # éléments de base à renseigner pour la class "GestionData" :
    ''' Paramètres de base '''

    def fonc_url(self, kwargs):
        url = "../gestion_pole/" + str(kwargs.get('etabid')) + "/"  # fonction création d'URL en fonction de l'entrée
        return url

    # nom du template à utiliser (template gestiondata.html par défaut et automatisé à conserver sauf exception
    template_name = 'common/gestionstructure.html'
    titre_template = "Liste des Pôles"  # titre de la page
    model = Pole  # model à utiliser
    form = PoleForm  # formulaire à utiliser
    item_message = "Pole"  # %s pour les messages automatisés
    ordre_affichage = [
        'code',
        'nom',
        'intitule',
        'cloture',
    ]  # ordre d'affichage de la liste de la fct GET : ajouter dans l'ordre d'autres filtres :['filter1', 'filter2',...]
    template_col_title = [
        'N_POLE',
        'NOM POLE',
        'INTITULE',
        'DATE CLOTURE',
    ]  # colonne à afficher dans le table
    template_lig_var = [
        'code',
        'nom',
        'intitule',
        'cloture',
    ]  # champs correspondants aux colonnes dans le table
    template_additional = None
    formats = {"string": "", "string": "", "None": "", "date": "Y"}
    nbcol = len(template_col_title)  # nombre de colonne du tableau
    # filtre de la liste du GET
    # q_query = []  # [Q(cloture__isnull=True)]

    def fonc_q_query(self, kwargs):
        q_query = [Q(etablissement=kwargs.get('etabid'))]
        return q_query

    # critères de tests d'unicité avant enregistrement, suppression ou modification
    def crit_unic_to_get(self, item):
        return {
            'nom__iexact': getattr(item, "nom"),
            'code__iexact': getattr(item, "code"),
            'cloture__isnull': True,
        }  # champs de comparaison pour tester les éventuels doublons / test d'unicité

    '''Cas particulier mode Automatique CONNEXION :'''
    # éléments de base à renseigner pour la class "GmaoImportation" :
    bdd = 'GEF'  # Base de données à utiliser
    model_update = "structure"  # fonction update à déclencher

    def parametre_connexion(self, kwargs):
        self.etabprefix = Etablissement.objects.get(id=kwargs.get('etabid')).prefix
        config = TOMLFile('local/config.toml').read()
        self.lien = config['LINK'][self.etabprefix][self.model_update]
        self.model_bdd = config['BDD'][self.bdd]['model']
        self.version_bdd = config['BDD'][self.bdd]['version']
        self.app_bdd = self.model_bdd + "connect"
        if self.lien == "FILE":
            self.fichier = config['LINKED_FILES'][self.etabprefix][self.model_update]
        else:
            self.fichier = None


class GestionService(GestionData):
    """Class maitresse utilisant GestionData"""

    # éléments de base à renseigner pour la class "GestionData" :
    ''' Paramètres de base '''

    def fonc_url(self, kwargs):
        url = "../gestion_service/" + str(kwargs.get('etabid')) + "/"  # fonction création d'URL en fonction de l'entrée
        return url

    # nom du template à utiliser (template gestiondata.html par défaut et automatisé à conserver sauf exception
    template_name = 'common/gestionstructure.html'
    titre_template = "Liste des Services"  # titre de la page
    model = Service  # model à utiliser
    form = ServiceForm  # formulaire à utiliser
    item_message = "Service"  # %s pour les messages automatisés
    ordre_affichage = [
        'code',
        'nom',
        'intitule',
        'cloture',
    ]  # ordre d'affichage de la liste de la fct GET : ajouter dans l'ordre d'autres filtres :['filter1', 'filter2',...]
    template_col_title = [
        'N_SERVICE',
        'NOM SERVICE',
        'INTITULE',
        'DATE CLOTURE',
    ]  # colonne à afficher dans le table
    template_lig_var = [
        'code',
        'nom',
        'intitule',
        'cloture',
    ]  # champs correspondants aux colonnes dans le table
    template_additional = None
    formats = {"string": "", "string": "", "None": "", "date": "Y"}
    nbcol = len(template_col_title)  # nombre de colonne du tableau

    def fonc_q_query(self, kwargs):
        q_query = [Q(etablissement=kwargs.get('etabid'))]
        return q_query

    # critères de tests d'unicité avant enregistrement, suppression ou modification
    def crit_unic_to_get(self, item):
        return {
            'nom__iexact': getattr(item, "nom"),
            'code__iexact': getattr(item, "code"),
            'cloture__isnull': True,
        }  # champs de comparaison pour tester les éventuels doublons / test d'unicité

    '''Cas particulier mode Automatique CONNEXION :'''
    # éléments de base à renseigner pour la class "GmaoImportation" :
    bdd = 'GEF'  # Base de données à utiliser
    model_update = "structure"  # fonction update à déclencher

    def parametre_connexion(self, kwargs):
        self.etabprefix = Etablissement.objects.get(id=kwargs.get('etabid')).prefix
        config = TOMLFile('local/config.toml').read()
        self.lien = config['LINK'][self.etabprefix][self.model_update]
        self.model_bdd = config['BDD'][self.bdd]['model']
        self.version_bdd = config['BDD'][self.bdd]['version']
        self.app_bdd = self.model_bdd + "connect"
        if self.lien == "FILE":
            self.fichier = config['LINKED_FILES'][self.etabprefix][self.model_update]
        else:
            self.fichier = None


class GestionCentreResponsabilite(GestionData):
    """Class maitresse utilisant GestionData"""

    # éléments de base à renseigner pour la class "GestionData" :
    ''' Paramètres de base '''

    def fonc_url(self, kwargs):
        url = (
            "../gestion_centreresponsabilite/" + str(kwargs.get('etabid')) + "/"
        )  # fonction création d'URL en fonction de l'entrée
        return url

    # nom du template à utiliser (template gestiondata.html par défaut et automatisé à conserver sauf exception
    template_name = 'common/gestionstructure.html'
    titre_template = "Liste des Centres de Responsabilité"  # titre de la page
    model = CentreResponsabilite  # model à utiliser
    form = CentreResponsabiliteForm  # formulaire à utiliser
    item_message = "Centre Responsabilité"  # %s pour les messages automatisés
    ordre_affichage = [
        'code',
        'nom',
        'intitule',
        'cloture',
    ]  # ordre d'affichage de la liste de la fct GET : ajouter dans l'ordre d'autres filtres :['filter1', 'filter2',...]
    template_col_title = [
        'N_CR',
        'NOM CR',
        'INTITULE',
        'DATE CLOTURE',
    ]  # colonne à afficher dans le table
    template_lig_var = [
        'code',
        'nom',
        'intitule',
        'cloture',
    ]  # champs correspondants aux colonnes dans le table
    template_additional = None
    formats = {"string": "", "string": "", "None": "", "date": "Y"}
    nbcol = len(template_col_title)  # nombre de colonne du tableau

    def fonc_q_query(self, kwargs):
        q_query = [Q(etablissement=kwargs.get('etabid'))]
        return q_query

    # critères de tests d'unicité avant enregistrement, suppression ou modification
    def crit_unic_to_get(self, item):
        return {
            'nom__iexact': getattr(item, "nom"),
            'code__iexact': getattr(item, "code"),
            'cloture__isnull': True,
        }  # champs de comparaison pour tester les éventuels doublons / test d'unicité

    '''Cas particulier mode Automatique CONNEXION :'''
    # éléments de base à renseigner pour la class "GmaoImportation" :
    bdd = 'GEF'  # Base de données à utiliser
    model_update = "structure"  # fonction update à déclancher

    def parametre_connexion(self, kwargs):
        self.etabprefix = Etablissement.objects.get(id=kwargs.get('etabid')).prefix
        config = TOMLFile('local/config.toml').read()
        self.lien = config['LINK'][self.etabprefix][self.model_update]
        self.model_bdd = config['BDD'][self.bdd]['model']
        self.version_bdd = config['BDD'][self.bdd]['version']
        self.app_bdd = self.model_bdd + "connect"
        if self.lien == "FILE":
            self.fichier = config['LINKED_FILES'][self.etabprefix][self.model_update]
        else:
            self.fichier = None


class GestionSite(GestionData):
    """Class maitresse utilisant GestionData"""

    # éléments de base à renseigner pour la class "GestionData" :
    ''' Paramètres de base '''

    def fonc_url(self, kwargs):
        url = "../gestion_site/" + str(kwargs.get('etabid')) + "/"  # fonction création d'URL en fonction de l'entrée
        return url

    # nom du template à utiliser (template gestiondata.html par défaut et automatisé à conserver sauf exception
    template_name = 'common/gestionstructure.html'
    titre_template = "Liste des sites"  # titre de la page
    model = Site  # model à utiliser
    form = SiteForm  # formulaire à utiliser
    item_message = "sites"  # %s pour les messages automatisés
    # ordre d'affichage de la liste de la fct GET : ajouter dans l'ordre d'autres filtres :['filter1', 'filter2',...]
    ordre_affichage = [
        'code',
        'nom',
        'intitule',
        'cloture',
    ]
    template_col_title = [
        'N_SITE',
        'NOM SITE',
        'INTITULE',
        'DATE CLOTURE',
    ]  # colonne à afficher dans le table
    template_lig_var = [
        'code',
        'nom',
        'intitule',
        'cloture',
    ]  # champs correspondants aux colonnes dans le table
    template_additional = None
    formats = {"string": "", "string": "", "None": "", "date": "Y"}
    nbcol = len(template_col_title)  # nombre de colonne du tableau

    def fonc_q_query(self, kwargs):
        q_query = [Q(etablissement=kwargs.get('etabid'))]
        return q_query

    # critères de tests d'unicité avant enregistrement, suppression ou modification
    def crit_unic_to_get(self, item):
        return {
            'nom__iexact': getattr(item, "nom"),
            'code__iexact': getattr(item, "code"),
            'cloture__isnull': True,
        }  # champs de comparaison pour tester les éventuels doublons / test d'unicité

    '''Cas particulier mode Automatique CONNEXION :'''
    # éléments de base à renseigner pour la class "GmaoImportation" :
    bdd = 'GEF'  # Base de données à utiliser
    model_update = "structure"  # fonction update à déclancher

    def parametre_connexion(self, kwargs):
        self.etabprefix = Etablissement.objects.get(id=kwargs.get('etabid')).prefix
        config = TOMLFile('local/config.toml').read()
        self.lien = config['LINK'][self.etabprefix][self.model_update]
        self.model_bdd = config['BDD'][self.bdd]['model']
        self.version_bdd = config['BDD'][self.bdd]['version']
        self.app_bdd = self.model_bdd + "connect"
        if self.lien == "FILE":
            self.fichier = config['LINKED_FILES'][self.etabprefix][self.model_update]
        else:
            self.fichier = None


class GestionEtablissement(GestionData):
    """Class maitresse utilisant GestionData"""

    # éléments de base à renseigner pour la class "GestionData" :
    ''' Paramètres de base '''
    url = "../gestion_etablissement/"

    # nom du template à utiliser (template gestiondata.html par défaut et automatisé à conserver sauf exception
    template_name = 'common/gestiondata.html'
    titre_template = "Liste des établissements"  # titre de la page
    model = Etablissement  # model à utiliser
    form = EtablissementForm  # formulaire à utiliser
    item_message = "établissements"  # %s pour les messages automatisés
    ordre_affichage = [
        'code',
        'prefix',
        'nom',
        'intitule',
        'cloture',
    ]  # ordre d'affichage de la liste de la fct GET : ajouter dans l'ordre d'autres filtres :['filter1', 'filter2',...]
    template_col_title = [
        'N_ETABLISSEMENT',
        'PREFIX',
        'NOM ETABLISSEMENT',
        'INTITULE',
        'DATE CLOTURE',
    ]  # colonne à afficher dans le table
    template_lig_var = [
        'code',
        'prefix',
        'nom',
        'intitule',
        'cloture',
    ]  # champs correspondants aux colonnes dans le table
    template_additional = "common/etablissement_conf.html"
    formats = {"string": "", "string": "", "string": "", "None": "", "date": "Y"}
    nbcol = len(template_col_title)  # nombre de colonne du tableau
    q_query = []  # [Q(cloture__isnull=True)]  # filtre de la liste du GET
    # critères de tests d'unicité avant enregistrement, suppression ou modification

    def crit_unic_to_get(self, item):
        return {
            'nom__iexact': getattr(item, "nom"),
            'code__iexact': getattr(item, "code"),
            'cloture__isnull': True,
        }  # champs de comparaison pour tester les éventuels doublons / test d'unicité

    def additional_def(self, request, item):
        config = tomlkit.loads(pathlib.Path("local/config.toml").read_text())
        lien_choice = request.POST.get("lien-select") or None
        fichier = request.POST.get("fichier") or None
        print(lien_choice)
        linkadd = tomlkit.table().indent(4)  # création d'une table toml vierge et indentation de la table
        if lien_choice:
            linkadd.add("structure", lien_choice)  # ajout d'un élément dans le .toml après l'ajout de l'élément.
            # autre ecriture possible : linkadd["structure"] = lien_choice
        else:
            linkadd.add("structure", 'OFF')
        linkadd["structure"].comment("exemple code pour ajout commentaire")
        linkadd["structure"].indent(8)  # ajout d'indentation sur la ligne (tabulation)
        linkadd.add(tomlkit.nl())  # ajout d'un saut de ligne dans le .toml après l'ajout de l'élément.
        config['LINK'][getattr(item, "prefix")] = linkadd  # création de la table toml dans le .toml (=commit false)
        linkfileadd = tomlkit.table().indent(4)
        if fichier:
            linkfileadd.add("structure", fichier)
        else:
            linkfileadd.add("structure", '')
        config['LINKED_FILES'][getattr(item, "prefix")] = linkfileadd
        linkfileadd["structure"].indent(8)
        linkfileadd.add(tomlkit.nl())
        print(config)
        with pathlib.Path('local/config.toml').open('w') as f:
            f.write(tomlkit.dumps(config))  # sauvegarde des modifs dans le .toml (=commit true)
        return

    '''Cas particulier mode Automatique CONNEXION :'''
    # éléments de base à renseigner pour la class "GmaoImportation" :
    bdd = 'GEF'  # Base de données à utiliser
    model_update = "Etablissement"  # fonction update à déclancher

    def parametre_connexion(self, kwargs):
        self.etabprefix = None
        config = TOMLFile('local/config.toml').read()
        self.lien = "OFF"
        self.model_bdd = config['BDD'][self.bdd]['model']
        self.version_bdd = config['BDD'][self.bdd]['version']
        self.app_bdd = self.model_bdd + "connect"
        self.fichier = None


class GestionStructure(GestionData):
    """Class maitresse utilisant GestionData"""

    # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['url'] = self.url
    #    etabid = kwargs['etabid']
    #    context['url'] = "../gestion_structure/"+str(etabid)
    #    return context

    # éléments de base à renseigner pour la class "GestionData" :
    ''' Paramètres de base '''
    # url = "/drachar-chuap/common/gestion_structure/1/"
    # TODO : régler le problème de l'URL
    def fonc_url(self, kwargs):
        url = "../gestion_structure/" + str(kwargs.get('etabid')) + "/"  # fonction création d'URL en fonction de l'entrée
        return url

    # nom du template à utiliser (template gestiondata.html par défaut et automatisé à conserver sauf exception
    template_name = 'common/gestionstructure.html'
    titre_template = "Liste de la Structure"  # titre de la page
    # TODO : voir comment gérer la partie structure dans sa globalité
    model = Uf  # model à utiliser
    form = UfForm  # formulaire à utiliser
    item_message = "element de la structure"  # %s pour les messages automatisés
    ordre_affichage = [
        'etablissement',
        'site',
        'pole',
        'centre_responsabilite',
        'service',
        'code',
        'nom',
        'cloture',
    ]  # ordre d'affichage de la liste de la fct GET : ajouter dans l'ordre d'autres filtres :['filter1', 'filter2',...]
    template_col_title = [
        'ETABLISSEMENT',
        'SITE',
        'POLE',
        'CENTRE RESPONSABILITE',
        'SERVICE',
        'N° UF',
        'NOM UF',
        'DATE CLOTURE',
    ]  # colonne à afficher dans le table
    template_lig_var = [
        'etablissement',
        'site',
        'pole',
        'centre_responsabilite',
        'service',
        'code',
        'nom',
        'cloture',
    ]  # champs correspondants aux colonnes dans le table
    template_additional = None
    formats = {
        "string": "",
        "string": "",
        "None": "",
        "None": "",
        "None": "",
        "None": "",
        "date": "Y",
    }
    nbcol = len(template_col_title)  # nombre de colonne du tableau

    # filtre de la liste du GET en fonction de l'URL
    def fonc_q_query(self, kwargs):
        q_query = [Q(etablissement=kwargs.get('etabid'))]
        return q_query

    # critères de tests d'unicité avant enregistrement, suppression ou modification
    def crit_unic_to_get(self, item):
        return {
            'nom__iexact': getattr(item, "nom"),
            'code__iexact': getattr(item, "code"),
            'cloture__isnull': True,
        }  # champs de comparaison pour tester les éventuels doublons / test d'unicité

    '''Cas particulier mode Automatique CONNEXION :'''
    bdd = 'GEF'  # Base de données à utiliser
    model_update = "structure"  # fonction update à déclancher
    # def configuration(self, kwargs):

    def parametre_connexion(self, kwargs):
        etabid = kwargs.get('etabid')
        print(etabid)
        config = TOMLFile('local/config.toml').read()
        if Etablissement.objects.get(id=kwargs.get('etabid')).prefix == "" or None:
            self.etabprefix = "DEFAUT"
            self.lien = config['LINK'][self.etabprefix][self.model_update]
        else:
            self.etabprefix = Etablissement.objects.get(id=kwargs.get('etabid')).prefix
            try:
                self.lien = config['LINK'][self.etabprefix][self.model_update]
            except Exception:
                self.lien = "ON"
                self.etabprefix = "DEFAUT2"
        self.model_bdd = config['BDD'][self.bdd]['model']
        self.version_bdd = config['BDD'][self.bdd]['version']
        self.app_bdd = self.model_bdd + "connect"
        if self.lien == "FILE":
            self.fichier = config['LINKED_FILES'][self.etabprefix][self.model_update]
        else:
            self.fichier = None


# ==================================================================================================================
# GESTION DES ALERTES
# ==================================================================================================================


class AlertsDocumentationView(BiomAidViewMixin, TemplateView):
    application = 'common'
    name = 'alerts-documentation'
    template_name = 'common/alerts-documentation.html'
    title = _("Alertes : Documentation")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for appname, application in self.biom_aid_applications.items():
            # print(appname, application['config'])
            cfg = application['config']
            if appname not in context['applications']:
                context['applications'][appname] = {}
            if hasattr(cfg, 'biom_aid_alert_categories'):
                # print("  ", cfg.biom_aid_alert_categories)
                context['applications'][appname]['alerts'] = cfg.biom_aid_alert_categories
        return context


class StructureView(BiomAidViewMixin, TemplateView):
    application = 'common'
    name = 'structure'
    template_name = 'common/structure21.html'
    title = _("Structures")

    def _role_expr(self, role_code):
        expr = Concat(
            Value('['),
            UserUfRole.objects.filter(
                (Q(uf__isnull=True) | Q(uf=OuterRef('pk')))
                & (Q(service__isnull=True) | Q(service=OuterRef('service')))
                & (Q(centre_responsabilite__isnull=True) | Q(centre_responsabilite=OuterRef('centre_responsabilite')))
                & (Q(pole__isnull=True) | Q(pole=OuterRef('pole')))
                & (Q(site__isnull=True) | Q(site=OuterRef('site')))
                & (Q(etablissement__isnull=True) | Q(etablissement=OuterRef('etablissement'))),
                role_code=role_code,
            )
            .order_by()
            .values('role_code')
            .annotate(
                record=StringAgg(
                    Cast(
                        JSONObject(
                            pk='pk',
                            code='role_code',
                            user='user',
                            username='user__username',
                            user_first_name='user__first_name',
                            user_last_name='user__last_name',
                        ),
                        output_field=TextField(),
                    ),
                    ',',
                    output_field=TextField(),
                )
            )
            .values('record'),
            Value(']'),
            output_field=TextField(),
        )
        return expr

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        field_names = {
            'code': 'Code',
            'nom': 'UF',
            'pole_name': _("Nom du pôle"),
            'etablissement_name': _("Etablissement"),
        }

        base_fields = ['code', 'nom']
        computed_fields = {
            'pole_name': F('pole__nom'),
            'etablissement_name': F('etablissement__nom'),
        }
        roles = [t[0].lower() for t in UserUfRole.NAME_CHOICES]
        field_names.update({t[0].lower(): t[1] for t in UserUfRole.NAME_CHOICES})

        fields = base_fields + list(computed_fields.keys()) + [role.lower() for role in roles]

        qs = Uf.objects.filter(cloture__isnull=True).annotate(**computed_fields)
        qs = qs.annotate(**{role.lower(): self._role_expr(role.upper()) for role in roles})

        html_table = '<table><tr>'
        html_table += (
            '<th>' + '</th><th>'.join(str(field_names.get(field, field.capitalize())) for field in fields) + '</th></tr><tr>'
        )
        for record in qs:
            html_table += (
                '<td>'
                + '</td><td>'.join(str(getattr(record, field)) for field in base_fields + list(computed_fields.keys()))
                + '</td>'
            )
            html_table += (
                '<td>'
                + '</td><td>'.join(
                    "<br>".join("{user_first_name} {user_last_name}".format(**role) for role in json.loads(getattr(record, field)))
                    for field in roles
                )
                + '</td></tr><tr>'
            )
        html_table += '</tr></table>'
        context['structure_table'] = html_table
        return context




class FournisseurPage(SmartPage):
    application = 'common'
    name = 'fournisseur'
    permissions = {'ADM'}
    smart_view_class = FournisseurSmartView
    title = "Fournisseurs"

# ==================================================================================================================
# GESTION DES Fournisseurs
# ==================================================================================================================

#class GestionFournisseurs(GestionData):
#    """Class maitresse utilisant GestionData"""
#
#    # éléments de base à renseigner pour la class "GestionData" :
#    ''' Paramètres de base '''
#    url = "../gestion_fournisseurs/"
#    # nom du template à utiliser (template gestiondata.html par défaut et automatisé à conserver sauf exception
#    template_name = 'common/gestiondata.html'
#    titre_template = 'Liste des Fournisseurs "génériques"'  # titre de la page
#    model = Fournisseur  # model à utiliser
#    form = FournisseurForm  # formulaire à utiliser
#    item_message = "Fournisseur"  # %s pour les messages automatisés
#    ordre_affichage = [
#        'exercice',
#        'lettre_budgetaire',
#        'discipline',
#        'code',
#        'nom',
#        'budget_montant',
#    ]  # ordre d'affichage de la liste de la fct GET : ajouter dans l'ordre d'autres filtres :['filter1', 'filter2',...]
#    template_col_title = [
#        'EXERCICE',
#        'BUDGET',
#        'CODE',
#        'NOM',
#        'DISCIPLINE',
#        'budget_montant',
#    ]  # colonne à afficher dans le table
#    template_lig_var = [
#        'exercice',
#        'lettre_budgetaire',
#        'code',
#        'nom',
#        'discipline',
#        'budget_montant',
#    ]  # champs correspondants aux colonnes dans le table
#    template_additional = None
#    formats = {
#        "date": "Y",
#        "string": "",
#        "None": "",
#        "None": "",
#        "None": "",
#        "None": "",
#    }
#    nbcol = len(template_col_title)  # nombre de colonne du tableau
#    q_query = [Q(cloture__isnull=True)]  # filtre de la liste du GET
#
#    # critères de tests d'unicité avant enregistrement, suppression ou modification
#    def crit_unic_to_get(self, item):
#        return {
#            'lettre_budgetaire__iexact': getattr(item, "lettre_budgetaire"),
#            'code__iexact': getattr(item, "code"),
#            'cloture__isnull': True,
#        }  # champs de comparaison pour tester les éventuels doublons / test d'unicité
#
#    '''Cas particulier mode Automatique CONNEXION :'''
#    bdd = 'GEF'  # Base de données à utiliser
#    model_update = "Compte"  # fonction update à déclancher
#
#    def parametre_connexion(self, kwargs):
#        # TODoO : passer en TOML
#        self.lien = common.config.settings.LIEN_GEF['link_compte']
#        self.model_bdd = common.config.settings.GEFTYPE['model_gef']
#        self.version_bdd = common.config.settings.GEFTYPE['version_gef']
#        self.app_bdd = common.config.settings.GEFTYPE['app_gef']
#        self.fichier = common.config.settings.LIEN_GEF['file_compte']

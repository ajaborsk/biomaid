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
from distutils.log import warn
import json
import logging
import urllib.parse
from copy import deepcopy
from inspect import ismodule

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Q, Value
from django.db.models.functions import Concat
from django.http import HttpRequest
from django.template import Context, Template
from django.urls import reverse, path
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import UserPassesTestMixin

from common import config
from common.models import Alert, Programme, UserUfRole
from common.user_settings import UserSettings
from common.utils import url_prefix_parse
from dem.models import Campagne
from dem.utils import user_campagnes

logger = logging.getLogger(__name__)


def dem_campagnes(view_params: dict, tvx=False):
    if tvx is True:
        url_name = 'dem:tvx-demande-create'
    else:
        url_name = 'dem:request-create'
    return [
        {
            'url_name': url_name,
            # 'url_kwargs': {'campagne_code': campagne.code},
            'url_parameters_string': '?'
            + urllib.parse.urlencode(
                {
                    'choices': json.dumps(
                        dict(
                            {
                                'calendrier': [campagne.pk],
                            },
                            **({'nature': campagne.natures} if campagne.natures else {}),
                        )
                    )
                }
            ),
            'label': campagne.nom,
        }
        for campagne in user_campagnes(view_params, tvx=tvx)
    ]


class BiomAidViewMixinMetaclass(type):
    def __new__(mcls: type, name: str, bases: tuple, attrs: dict):
        if name == 'BiomAidViewMixin':
            # Only execute on the Mixin itsef (not on derived classes)
            # print('BiomAidView metaclass...')
            applications = {}
            for app_id, app in apps.app_configs.items():
                # print('app:', app, app_id)
                if hasattr(app, 'biom_aid'):
                    applications[app_id] = {
                        'config': app,
                        'verbose_name': app.verbose_name,
                        'roles': set(app.biom_aid_roles),
                    }
            attrs['biom_aid_applications'] = dict(applications)
            # print(attrs['biom_aid_applications'])

        new_class = super().__new__(mcls, name, bases, attrs)
        return new_class


class BiomAidViewMixin(UserPassesTestMixin, metaclass=BiomAidViewMixinMetaclass):
    """
    Mixin destiné à être utilisé pour toutes les vues de BiomAid et qui va notamment permettre de configurer le thème
    en fonction de l'URL, la gestion de l'aide, etc.
    L'utilisation d'un Mixin permet de l'utiliser aussi
    pour les vues qui n'héritent pas de BiomAidView (comme les vues d'authentification).

    Fonctionnalité de ce Mixin :

    - Récupération de données 'de base' (version, utilisateur, date de dernière visite...)
    - Gestion du url_prefix
        - Analyse de l'URL & calcul du thème
        - Création des menus (utilisateur, site, applications...)
    - Cestion des préférences de l'utilisateur connecté
    - Gestion des rôles effectifs sur la vue (page)
    - Methode de 'déparamétrisation' (= calcul d'une fonction qui prend view_params comme paramètre unique)

    - Attributs :
        - view_params
        - user_roles
        - last_seen_date
        -

    """

    # Default permissions = None !
    permissions: set[str] = set()
    footer_text = ""

    def __init__(self, *args, **kwargs):
        self.widgets = {}
        self.main_widget = None
        super().__init__(*args, **kwargs)

    def reverse(self, viewname, urlconf=None, args=None, kwargs=None, current_app=None):
        kwargs = kwargs or {}
        return reverse(
            viewname,
            urlconf,
            args,
            dict(kwargs, url_prefix=self.url_prefix),
            current_app,
        )

    def unparametrize(self, data):
        """
        Cette fonction 'déparamètre' un objet, éventuellement paramétrique, comme un filtre ou un titre, ou une liste de choix...
        Il faut l'appeler avec un objet potentiellement paramétrique (il y en a beaucoup dans BIOM_AID)
        Elle retourne soit l'objet original (s'il n'était pas paramétrique), soit l'objet paramétré.
        Typiquement, les paramètres sont :
        - now : datetime du moment de l'appel
        - user : l'objet utilisateur courant (une instance de User)
        - user_roles : la liste des rôles de l'utilisateur courant
        - theme_name : le nom du thème courant
        - user_preference : Un dictionnaire des préférences de l'utilisateur
        - args : liste des arguments passés à la vue
        + les arguments nommés passés à la vue

        Ce mixin BiomAidViewMixin crée ce params au setup() de chaque vue et le stocke dans l'attribut
        view_params
        """
        if callable(data):
            ns = {
                k: apps.all_models[v.split('.')[0]][v.split('.')[1]] for k, v in data.__annotations__.items() if isinstance(v, str)
            }
            data = data(self.view_params, **ns)
        if isinstance(data, str):
            data = data.format(**dict(self.view_params))
        return data

    def get_user_roles(self, request):
        """
        Les rôles d'un utilisateur sont tous les rôles pour lesquels l'utilisateur a ce rôle sur au moins un objet associé
        Par exemple, un utilisateur est un arbitre s'il est arbitre sur au moins un programme, il est expert s'il est expert sur
        au moins un domaine, chef de pôle s'il est chef d'au moins un pôle, etc.
        TODO: distribuer ce calcul sur toutes les applications, de façon à intégrer automatiquement des nouveaux rôles créés par
            une application
        """
        roles = []

        if request.user.is_superuser:
            roles.append('ADM')
        if request.user.is_staff:
            roles.append('MAN')
        if isinstance(request.user, get_user_model()):
            if Programme.objects.filter(arbitre=request.user).exists():
                roles.append('ARB')
                roles.append('P-ARB')
            if Campagne.objects.filter(dispatcher=request.user).exists():
                roles.append('DIS')
                roles.append('P-DIS')
            roles += list(UserUfRole.active_objects.filter(user=request.user).values_list('role_code', flat=True).distinct())
            roles += list(
                UserUfRole.active_objects.filter(user=request.user)
                .annotate(p_role=Concat(Value('P-'), F('role_code')))
                .values_list('p_role', flat=True)
                .distinct()
            )

            # Get last time the use viewed a page on this site (if any)
            if request.user.last_seen:
                self._last_seen = request.user.last_seen

        return set(roles)

    def _portal_menu_entry_to_menu_entry(self, entry):
        # print("Entry =>", repr(entry))
        if 'permissions' in entry:
            if not (set(entry['permissions']) & set(self._user_roles)):
                if entry.get('show-only-if-allowed', False):
                    return []
                else:
                    entry.pop('url', None)
                    entry.pop('url_name', None)
                    entry.pop('entries', None)
                    entry['icon'] = 'lock'
                    entry['classes'] = entry.get('classes', []) + ['inactive']
                    return [entry]

        if 'engine' in entry:  # This is en entries generator
            entries_definition = entry
            entries = []
            if entries_definition.get('engine') == 'queryset':
                app_label, modelname = entries_definition.get('model').split('.')
                # print(app_label, modelname)
                model = ContentType.objects.get(app_label=app_label, model=modelname).model_class()
                # kwargs = dict({'now': timezone.now()})
                filters = self.unparametrize(entries_definition.get('filters', {}))
                annotations = self.unparametrize(entries_definition.get('annotations', {}))
                aggregates = self.unparametrize(entries_definition.get('aggregates', {}))
                agg_filters = self.unparametrize(entries_definition.get('agg_filters', {}))
                sort = self.unparametrize(entries_definition.get('sort', []))
                mapping = self.unparametrize(entries_definition.get('mapping', {}))
                if isinstance(filters, dict):
                    filters = Q(**filters)
                if isinstance(agg_filters, dict):
                    agg_filters = Q(**agg_filters)
                queryset = (
                    model.objects.order_by()
                    .annotate(**annotations)
                    .filter(filters)
                    .annotate(**aggregates)
                    .filter(agg_filters)
                    .order_by(*sort)
                    .values(**mapping)
                    .distinct()
                )
                entries = list(queryset)
                # raise RuntimeError()
            elif entries_definition.get('engine') == 'campagnes':
                entries = list(dem_campagnes({'user': self.request.user, 'now': timezone.now()}))
            elif entries_definition.get('engine') == 'campagnes_tvx':
                entries = list(dem_campagnes({'user': self.request.user, 'now': timezone.now()}, tvx=True))
            else:
                raise RuntimeWarning(_("Unknown entries engine: '{engine}'").format(**entries_definition))
            return sum(
                [self._portal_menu_entry_to_menu_entry(sub_entry) for sub_entry in entries],
                [],
            )
        elif 'entries' in entry:  # This is a submenu
            if isinstance(entry['entries'], dict):  # Single generator
                entry.update({'entries': self._portal_menu_entry_to_menu_entry(entry['entries'])})
                return [entry]
            elif isinstance(entry['entries'], list) or isinstance(entry['entries'], tuple):
                entry.update(
                    {
                        'entries': sum(
                            [self._portal_menu_entry_to_menu_entry(sub_entry) for sub_entry in entry['entries']],
                            [],
                        )
                    }
                )
                return [entry]
            else:
                raise RuntimeWarning(
                    _(
                        "Submenu entries must be tuple, list or dict ; not {} ({})".format(
                            type(entry['entries']), repr(entry['entries'])
                        )
                    )
                )
        return [entry]

    def test_func(self):
        "Teste si l'utilisateur a le droit d'accéder à cette vue"
        # L'utilisateur est dans self.request.user
        # self.permissions est soit '__PUBLIC__', soit '__LOGIN__' soit un ensemble avec les rôles ayant accès à la page
        # il suffit d'avoir ce rôle sur un seul élément de la base pour pouvoir accéder à la page
        # print("AJA: Checking permissions:", repr(self.permissions))

        if self.permissions == '__PUBLIC__':
            return True
        if self.permissions == '__LOGIN__' and isinstance(self.request.user, get_user_model()):
            return True

        if self._user_roles & set(self.permissions):
            return True
        else:
            return False

    def setup(self, request: HttpRequest, *args: list, **kwargs: dict):
        super().setup(request, *args, **kwargs)

        self.url_prefix, self.portal, self.config, self.prefix_theme, self.theme = url_prefix_parse(kwargs, request)

        # Détermine les roles principaux de l'utilisateur et les stocke dans l'instance. Cela servira...
        self._user_roles = self.get_user_roles(request)

        self.my_app_name = self.__module__.split('.')[0]

        self._user_settings = UserSettings(request.user)

        # self.theme_name = self.prefix_theme_name or self.portal.get('theme-name', self.config.get('default-theme', None))

        # A collection of parameters,
        self.view_params = dict(
            {
                'user': request.user,
                'request': request,
                'request_get': request.GET,
                'request_post': request.POST,
                'now': timezone.now(),
                # 'theme_name': self.theme_name,
                'user_roles': self._user_roles,
                'user_preferences': self._user_settings,
                'args': args,
            },
            **kwargs,
        )

    def dispatch(self, request, *args, **kwargs):
        # print("mixin before view...")
        # if self.portal_name == '__NOT_FOUND__':
        #     return redirect('/geqip-chuap/not_found')

        response = super().dispatch(request, *args, **kwargs)
        # print("mixin after view...")

        # Save user settings (if needed)
        self._user_settings._save_settings()

        return response

    def main_tour_steps(self, context):
        return []

    def get_login_url(self):
        return self.reverse(config.settings.LOGIN_URL_NAME)

    def tour_process(self, tour_name, context, steps):
        step_idx = 1
        tour_steps = []
        for step in steps:
            tour_steps.append(
                {
                    'step': step_idx,
                    'selector': step.get('selector', None),
                    'title': step.get('title', ''),
                    'content': step.get('content', ''),
                    'image': step.get('image', None),
                }
            )
            step_idx += 1
        context[tour_name + '_steps'] = tour_steps
        return context

    def get(self, request, *args, **kwargs):
        if 'widget_id' in request.GET:
            if request.GET['widget_id'] in self.widgets:
                return self.widgets[request.GET['widget_id']]._get(request, *args, **kwargs)
            else:
                warn("GET with widget_id='{}' but there is no widget with that id in this view...".format(request.GET['widget_id']))

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'widget_id' in request.POST:
            if request.POST['widget_id'] in self.widgets:
                return self.widgets[request.POST['widget_id']]._post(request, *args, **kwargs)
            else:
                warn(
                    "POST with widget_id='{}' but there is no widget with that id in this view...".format(request.POST['widget_id'])
                )

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # The main widget !
        context['main_widget'] = self.main_widget

        # Gestion éventuelle du préfixe d'RUL
        context['url_prefix'] = self.url_prefix

        context['base_template'] = self.config.get('base_template', 'common/base.html')

        # Mise à jour avec des données de configuration
        context.update(
            {
                "debug_mode": config.settings.DEBUG,
                "dem_version": config.settings.DEM_VERSION,
                "dem_version_date": config.settings.DEM_VERSION_DATE,
                # "biom_aid_config": self.config,
            }
        )

        # Les rôles de l'utilisateur (si on est dans une vue héritée de BiomAidView, aucun rôle sinon)
        if not hasattr(self, '_user_roles'):
            self._user_roles = ()
        context['user_roles'] = tuple(self._user_roles)

        if 'label' in self.portal:
            context['application_title'] = self.portal['label']

        context['main_name'] = self.portal.get('main-name', '')

        context['theme'] = self.theme

        context['theme_css'] = self.config.get('themes', {}).get(context['theme'], {}).get('css', None)

        # Menu des portails accessibles à l'utilisateur
        applications_menu = [{'icon': 'fa-solid fa-bars', 'label': None, 'entries': []}]
        for portal_name, portal in apps.app_configs['common'].portals.items():
            if set(portal['permissions']) & set(context['user_roles']):
                applications_menu[0]['entries'].append(
                    {
                        'label': portal['label'],
                        'url_name': portal.get('home', portal_name + ':home'),
                        'url_kwargs': {
                            'url_prefix': portal_name
                            + '-'
                            + self.config['name']
                            + ('' if self.prefix_theme is None else ('-' + self.prefix_theme))
                        },
                    }
                )
        context['applications_menu'] = applications_menu

        context['global_status_message'] = self.unparametrize(self.portal.get('global-status-message', ''))
        context['main_status_message'] = self.unparametrize(self.portal.get('main-status-message', ''))
        context['user_status_message'] = self.unparametrize(self.portal.get('user-status-message', ''))

        if 'external-menu' in self.portal:
            context['external_menu'] = []
            for entry in self.portal['external-menu']:
                if isinstance(entry, dict):
                    context['external_menu'].append(entry)
                elif isinstance(entry, str) and entry in self.config.get('external-links', {}):
                    context['external_menu'].append(self.config['external-links'][entry])
                else:
                    logger.warning(_("Entry '{}' in external menu portal configuration not recognized").format(entry))
        else:
            context['external_menu'] = ()

        if 'main-menu' in self.portal:
            # print("Computing portal menu...")
            context['main_menu'] = [
                {
                    # 'img': 'local/chu-amiens-logo-small.png',
                    'classes': ['no-hilight', 'menu-image'],
                    'url': self.reverse(self.portal['home']),
                }
            ] + sum(
                [self._portal_menu_entry_to_menu_entry(entry) for entry in deepcopy(self.portal['main-menu'])],
                [],
            )

        # Menu utilisateur :
        if isinstance(self.request.user, get_user_model()):
            current_alerts = Alert.objects.filter(destinataire=self.request.user, cloture__isnull=True)
            context['nb_alerts'] = current_alerts.count()
            context['nb_unread_alerts'] = current_alerts.filter(date_lecture__isnull=True).count()
            context['user_menu'] = (
                {
                    'label': self.request.user.first_name + " " + self.request.user.last_name,
                    'icon': 'fa-solid fa-user',
                    'badge': context['nb_unread_alerts'],
                    'right': True,
                    'entries': [
                        {
                            'icon': 'fa-solid fa-user-circle',
                            'label': _("Mon compte"),
                            'url_name': 'common:account',
                            'help_text': _(
                                "Tout ce qui concerne mon compte et mes accès"
                                " (nom de connexion, mot de passe, adresse email, rôles...)"
                            ),
                        },
                        {
                            'icon': 'fa-solid fa-triangle-exclamation',
                            'label': _("Mes alertes ({} en cours)").format(context['nb_alerts']),
                            'url_name': 'common:user-alerts',
                            'help_text': _("Liste des alertes / signalements qui me concernent"),
                            'badge': context['nb_unread_alerts'],
                        },
                        {
                            'icon': 'fa-solid fa-vcard',
                            'label': _("Mes informations personnelles"),
                            'url_name': 'common:profile',
                        },
                        {
                            'icon': 'fa-solid fa-sliders',
                            'label': _("Mes préférences"),
                            'url_name': 'common:preferences',
                        },
                    ],
                },
            )
            if 'ADM' in context['user_roles']:
                context['user_menu'][0]['icon'] = 'fa-solid fa-gears'
                context['user_menu'][0]['entries'].append(
                    {
                        'icon': 'fa-solid fa-gear',
                        'label': _("Administration"),
                        'url_name': 'common:admin-home',
                    }
                )
            context['user_menu'][0]['entries'].append(
                {
                    'icon': 'fa-solid fa-sign-out',
                    'label': _("Se déconnecter"),
                    'url_name': 'logout',
                }
            )
        else:
            context['user_menu'] = (
                {
                    'label': _("Non connecté"),
                    'right': True,
                    'entries': (
                        {
                            'icon': 'fa-solid fa-sign-in',
                            'label': _("Se connecter ou s'inscrire"),
                            'url_name': 'common:sign',
                        },
                    ),
                },
            )

        # Aide
        context['help_menu'] = (
            {
                'icon': 'fa-solid fa-question',
                'label': None,
                'right': True,
                'entries': (
                    {
                        'label': _("A propos de BiomAid"),
                        'url_name': 'common:about',
                    },
                    {
                        'label': _("Visite guidée générale"),
                        'classes': ('main-tour-launch',),
                    },
                    {
                        'label': _("Visite guidée de cette page"),
                        'classes': ('page-tour-launch',),
                    },
                    {
                        'label': _("Page de l'aide (texte)"),
                        'url_name': 'dem:aide',
                    },
                ),
            },
        )

        # Ajoute ce qui concerne le guide interactif
        context = self.tour_process('main_tour', context, self.main_tour_steps(context))

        # Titre de la page/vue
        context['title'] = getattr(self, 'title', getattr(self, 'label', getattr(self, 'name', "")))

        # Footer help text
        if 'persistent_help_stmpl' in self.config:
            tmpl = Template(self.config['persistent_help_stmpl'])
            context['footer_text'] = tmpl.render(Context(context))

        return context


def views_from_module(module, already_done):
    # print("from: ", module, already_done)
    package = module.__package__
    views = []
    already_done.add(module.__name__)
    for obj in module.__dict__.values():
        # print(obj, obj.__module__)
        if isinstance(obj, type) and issubclass(obj, BiomAidViewMixin) and hasattr(obj, 'name'):
            views.append(obj)
            # print("appending", obj)
        elif ismodule(obj) and obj.__package__ == package:
            if obj.__name__ not in already_done:
                # print("Diving into", obj)
                already_done.add(obj.__name__)
                lviews, done = views_from_module(obj, already_done)
                views += lviews
                already_done |= done
    return views, already_done


def get_view_url_patterns(view):
    urlpatterns = []

    if hasattr(view, 'get_url_patterns') and callable(view.get_url_patterns):
        urlpatterns.extend(view.get_url_patterns())
    else:
        urlpatterns.append(path(view.name + '/', view.as_view(), name=view.name))

    return urlpatterns


def views_to_url_patterns(module):
    """
    Fonction qui récupère automatiquement les vues sous forme de classes d'un module (passé en paramètre) et crée
    automatiquement les urls correpondantes, pour les insérer dans la liste des urls gérées par Django.
    """
    urlpatterns = []
    # print("AJA getting views from", module)
    for view in module.__dict__.values():
        if isinstance(view, type) and issubclass(view, BiomAidViewMixin) and hasattr(view, 'name'):
            urlpatterns.extend(get_view_url_patterns(view))

    return urlpatterns

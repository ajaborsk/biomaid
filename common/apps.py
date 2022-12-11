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
import time
from copy import deepcopy
from warnings import warn

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, Div, Button
from django.apps import AppConfig, apps
from django.db.models import Q
from django.db.models import Lookup
from django.db.models.fields import Field
from django.forms import Form
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.forms import BooleanField, ChoiceField, CharField, Textarea, IntegerField

from common import config
from smart_view.layout import SmartLayoutFieldset, SmartLayoutField
from smart_view.smart_form import BaseSmartForm

logger = logging.getLogger(__name__)


@Field.register_lookup
class Like(Lookup):
    lookup_name = 'like'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s LIKE %s' % (lhs, rhs), params


def user_settings_level(level_id, categories, user_settings):
    ret = []
    got_user_settings = []
    if level_id:
        level = len(level_id.split('.')) + 1
        level_path = level_id.split('.')
    else:
        level = 1
        level_path = []

    for c_key, category in categories.items():
        c_path = c_key.split('.')
        c_contents = []

        if c_path[: len(level_path)] == level_path and len(c_path) - len(level_path) == 1:
            # Settings which are exactly in this category
            for s_key, setting in user_settings.items():
                s_path = s_key.split('.')
                if s_path[: len(c_path)] == c_path and len(s_path) - len(c_path) == 1:
                    attr_us = s_key.replace('.', '__').replace('-', '_')
                    c_contents.append(
                        SmartLayoutField(
                            attr_us,
                            data_user_setting_path=s_key,
                            view_roles=setting.get('roles'),
                        )
                    )
                    got_user_settings.append(user_settings[s_key])

            # Subcategories
            sub, gus = user_settings_level(c_key, categories, user_settings)
            c_contents += sub

            # Orphan settings (in this category but not in a sub-category)
            ...

            if c_contents:
                ret.append(
                    SmartLayoutFieldset(
                        category.get('label', c_key.capitalize()),
                        *c_contents,
                        css_class='level-{:d}'.format(level + 1),
                        style='grid-column:1/last-column;',
                        help_text=category.get('help_text'),
                    )
                )

    return ret, got_user_settings


def user_settings_form_factory(name: str, base: type, categories: dict, user_settings: dict) -> Form:
    """
    Create a Django Form from user settings
    :param name: The form name
    :param base: The base class
    :param categories: Settings categories
    :param user_settings: User settings (as a dict)
    :return: A (Smart) Form
    """
    helper = FormHelper()
    helper.form_id = 'id-user-settings'
    helper.form_class = 'smart-view-form'
    helper.form_method = 'post'
    helper.template_pack = 'geqip'
    main_fieldset = Fieldset(
        '',
        *(user_settings_level('', categories, user_settings)[0]),
        css_class='level-1',
    )

    helper.layout = main_fieldset

    helper.layout.append(
        Div(
            Submit('submit', 'Enregistrer'),
            Button('reset', _("Réinitialiser"), onclick="window.location.href=\".\""),
            css_class="form-buttons-box",
        )
    )

    form_class_attrs = {}

    for k_us, user_setting in user_settings.items():
        attr_us = k_us.replace('.', '__').replace('-', '_')
        format = user_setting.get('format', 'string')
        if format == 'string':
            form_class_attrs[attr_us] = CharField(
                label=user_setting.get('label'),
                help_text=user_setting.get('help_text'),
                required=False,
            )
        elif format == 'text':
            form_class_attrs[attr_us] = CharField(
                label=user_setting.get('label'),
                help_text=user_setting.get('help_text'),
                widget=Textarea(),
                required=False,
            )
        elif format == 'boolean':
            form_class_attrs[attr_us] = BooleanField(
                label=user_setting.get('label'),
                help_text=user_setting.get('help_text'),
                required=False,
            )
        elif format == 'money':
            form_class_attrs[attr_us] = IntegerField(
                label=user_setting.get('label'),
                help_text=user_setting.get('help_text'),
                required=False,
            )
        elif format == 'choices':
            form_class_attrs[attr_us] = ChoiceField(
                label=user_setting.get('label'),
                help_text=user_setting.get('help_text'),
                choices=user_setting.get('choices', {}).items(),
                required=False,
            )
        else:
            raise RuntimeError(_("Type de préférence inconnue : '{}'").format(format))

    form_class_attrs['helper'] = helper
    return type(base)(name, (base,), form_class_attrs)


def _get_config(config_id):
    """Fonction (récursive) qui calcule une configuration complète en gérant l'héritage entre configurations
    basée sur l'attribut 'based_on'.
    Pour l'instant, le fonctionnement est similaire à ce qu'on pourrait faire avec de l'héritage simple :
    Chaque valeur est remplacée (surchargée). Il n'y a pas de possibilité de compléter ou de modifier les valeurs héritées"""
    r_config = config.settings.BIOM_AID_CONFIGS[config_id]
    if config_id is not None:
        if 'based_on' in r_config:
            pre_config = _get_config(r_config['based_on'])
        else:
            pre_config = {}
        r_config = dict(pre_config, **r_config)
    return r_config


def check_useless_role_entry(name, data):
    # faire un 'import' ici n'est pas très clean, mais c'est le seul moyen car il ne faut pas importer à l'ouverture du
    #  module (car Django n'est pas encore initialisé et on ne peut pas travailler sur les modèles) mais à l'exécution
    #  de la fonction (qui arrive à un moment où Django est initialisé)
    from common.models import UserUfRole
    from common.models import User

    timer1 = time.time()
    rsqs = UserUfRole.objects.raw(
        'SELECT u.id,'
        '  g.id AS "other",'
        '  u.user_id,'
        '  u.role_code,'
        '  common_etablissement.nom as group_etablissement'
        ' FROM common_userufrole u, common_userufrole g, common_uf, common_etablissement'
        ' WHERE u.role_code = g.role_code'
        '   AND u.user_id = g.user_id'
        '   AND u.uf_id = common_uf.id'
        '   AND (g.etablissement_id = common_uf.etablissement_id'
        '     OR g.service_id = common_uf.service_id'
        '     OR g.centre_responsabilite_id = common_uf.centre_responsabilite_id'
        '     OR g.pole_id = common_uf.pole_id'
        '     OR g.site_id = common_uf.site_id)'
        '   AND g.uf_id IS NULL'
        '   AND (g.cloture IS NULL OR g.cloture > %s)'
        '   AND (u.cloture IS NULL OR u.cloture > %s)'
        '   AND common_etablissement.id = g.etablissement_id',
        [now(), now()],
    )
    # print("Fast : ", len(list(rsqs)))
    alerts = [
        {
            'destinataire': User(pk=79),
            'categorie': name,
            'niveau': data['alert_level'],
            'donnees': json.dumps(
                {
                    'role_code': role_scope.role_code,
                    'user': role_scope.user_id,
                    'id': role_scope.pk,
                    'superset_id': role_scope.other,
                }
            ),
            'msg_data': {
                'code_uf': role_scope.uf.code,
                'username': role_scope.user_id,
                'superset_service': role_scope.user_id,
                'superset_centre_responsabilite': role_scope.user_id,
                'superset_pole': role_scope.user_id,
                'superset_site': role_scope.user_id,
                'superset_etablissement': role_scope.group_etablissement,
            },
            'date_activation': now(),
        }
        for role_scope in rsqs
    ]
    timer1 = time.time() - timer1

    # return alerts, {'categorie': name}

    timer2 = time.time()
    alerts = []
    user_uf_roles = UserUfRole.objects.filter(Q(cloture__isnull=True) | Q(cloture__gt=now()), uf__isnull=True)
    for user_uf_role in user_uf_roles:
        role_code = user_uf_role.role_code
        user = user_uf_role.user
        others = UserUfRole.objects.filter(
            Q(cloture__isnull=True) | Q(cloture__gt=now()),
            Q(uf__service=user_uf_role.service)
            | Q(uf__centre_responsabilite=user_uf_role.centre_responsabilite)
            | Q(uf__pole=user_uf_role.pole)
            | Q(uf__site=user_uf_role.site)
            | Q(uf__etablissement=user_uf_role.etablissement),
            uf__isnull=False,
            role_code=role_code,
            user=user,
        )
        for other in others:
            alerts.append(
                {
                    'destinataire': User(pk=79),
                    'categorie': name,
                    'niveau': data['alert_level'],
                    'donnees': json.dumps(
                        {
                            'role_code': user_uf_role.role_code,
                            'user': user.pk,
                            'id': other.pk,
                            'superset_id': user_uf_role.pk,
                        }
                    ),
                    'msg_data': {
                        'code_uf': other.uf.code,
                        'username': str(user),
                        'superset_service': str(user_uf_role.service),
                        'superset_centre_responsabilite': str(user_uf_role.centre_responsabilite),
                        'superset_pole': str(user_uf_role.pole),
                        'superset_site': str(user_uf_role.site),
                        'superset_etablissement': str(user_uf_role.etablissement),
                    },
                    'date_activation': now(),
                }
            )
    timer2 = time.time() - timer2

    logger.debug(f"Raw SQL : {timer1}, QS & Python: {timer2}")

    return alerts, {'categorie': name}


class CommonConfig(AppConfig):
    name = 'common'
    verbose_name = _("Gestion des équipements (commun)")
    biom_aid = {
        'portal': {
            'label': _("Outils du Manager"),
            'main-name': _("Common"),
            'permissions': ('ADM', 'MAN'),
            'home': 'common:manager-home',
            'main-menu': (
                {
                    'label': _("Accueil"),
                    'url_name': 'common:manager-home',
                },
                {
                    'label': _("Roles"),
                    'url_name': 'common:role',
                },
                {
                    'label': _("Campagnes"),
                    'url_name': 'common:calendrier',
                },
                {
                    'label': _("Programmes"),
                    'url_name': 'common:programme',
                },
            ),
        },
        'user-settings-categories': {
            'notifications': {'label': _("Notifications et alertes")},
        },
        'user-settings': {
            'notifications.alert-email': {
                'label': _("Email en cas d'alerte"),
                'help_text': _("Faut-il envoyer un email si des alertes sont détectées ?"),
                'format': 'choices',
                'choices': {
                    'never': _("Jamais"),
                    'only_new': _("En cas de nouvelle alerte"),
                    'always': _("Tant qu'il y a des alertes en cours"),
                },
                'default': 'never',
            },
            'notifications.alert-email-delay': {
                'label': _("Délai minimum entre les emails"),
                'help_text': _("Délai minimum entre deux emails d'alerte"),
                'format': 'choices',
                'choices': {
                    '6': _("6 heures"),
                    '12': _("12 heures"),
                    '24': _("1 journée"),
                    '48': _("2 jours"),
                    '72': _("3 jours"),
                },
                'default': '12',
            },
            'notifications.alert-email-group-size': {
                'label': _("Nombre limite d'alertes avant groupement"),
                'help_text': _(
                    "Lorsque le nombre d'alertes d'une même catégorie dépasse ce nombre, "
                    "elles sont groupées dans un seul message et plus listées individuellement."
                ),
                'format': 'choices',
                'choices': {
                    '0': _("Groupement désactivé"),
                    '100': _("100 alertes"),
                    '50': _("50 alertes"),
                    '10': _("10 alertes"),
                },
                'default': '100',
            },
        },
    }
    biom_aid_roles = '__ALL__'
    biom_aid_alert_categories = {
        'useless-role-entry': {
            'roles': {'ADM'},
            'label': _("Fiche de rôle inutile"),
            'help_text': _(
                "Notification adressée à un administrateur pour lui indiquer qu'une fiche de rôle"
                " est inutile car 'incluse' dans une autre"
            ),
            'hint': _("""Pour mettre fin à l'alerte il suffit de supprimer la fiche de rôle repérée"""),
            'message': _(
                "<span>La fiche de rôle {id} (rôle {role_code} pour l'utilisateur {username}"
                " sur l'uf {code_uf}) est inutile car elle est incluse dans la fiche {superset_id}"
                " (service={superset_service} centre_responsabilite={superset_centre_responsabilite}"
                " pole={superset_pole} site={superset_site} etablissement={superset_etablissement})"
                " </span>"
            ),
            'alert_level': 1,
            'groups': {'TODO', 'TEST'},
            'check_func': check_useless_role_entry,  # La fonction qui fait la détection d'alerte
        },
    }

    portals = {}
    configs = {}
    user_settings_categories = {}

    def ready(self):
        # Cette méthode est lancée une fois que Django est initialisé (ce qui permet d'utiliser toutes les fonctionnalités)
        #  mais une seule fois au lancement de Django
        # print('préparation BIOM_AID...')

        # Configs
        self.configs = {}
        for config_id in config.settings.BIOM_AID_CONFIGS.keys():
            self.configs[config_id] = _get_config(config_id)

        # Application portals
        for app_cfg in apps.get_app_configs():
            if hasattr(app_cfg, 'biom_aid'):
                if 'portal' in app_cfg.biom_aid:
                    self.portals[app_cfg.name] = app_cfg.biom_aid['portal']
                    # print("(AJA) Defined portals:", list(self.portals.keys()))

                # User settings (=preferences) categories
                if 'user-settings-categories' in app_cfg.biom_aid:
                    if set(app_cfg.biom_aid['user-settings-categories'].keys()) & set(self.user_settings_categories.keys()):
                        raise RuntimeError(
                            _("Error: Overwriting user settings category definitions: {}").format(
                                set(app_cfg.biom_aid['user-settings-categories'].keys()) & set(self.user_settings_categories.keys())
                            )
                        )
                    self.user_settings_categories.update(app_cfg.biom_aid['user-settings-categories'])
            if hasattr(app_cfg, 'biom_aid_alert_categories'):
                for key, category in app_cfg.biom_aid_alert_categories.items():
                    if 'user_settings' in category:
                        # print('d', key, category)
                        if 'notifications.' + app_cfg.name not in self.user_settings_categories:
                            # print('e', key, app_cfg.name)
                            self.user_settings_categories.update({'notifications.' + app_cfg.name: {'label': app_cfg.verbose_name}})
                        self.user_settings_categories.update(
                            {'notifications.' + app_cfg.name + '.' + key: {'label': category.get('label')}}
                        )
                        # pprint(self.user_settings_categories)

        # Local portals
        self.portals.update(
            {portal_id: config.settings.BIOM_AID_PORTALS[portal_id] for portal_id in config.settings.BIOM_AID_PORTALS.keys()}
        )

        # Check for portals conformity
        for portal_name, portal in self.portals.items():  # NOQA
            # Is there a permissions item ?
            if 'permissions' not in portal:
                raise RuntimeError(_("Portal '{}' must have a 'permissions' entry.").format(portal_name))
            # Is there a home page ?
            if 'home' not in portal or not isinstance(portal['home'], str):
                raise RuntimeError(_("Portal '{}' must have a str 'home' entry.").format(portal_name))
            # Is portal name correct
            if not portal_name.isidentifier():
                raise RuntimeError(_("Portal name must match a valid python identifier, not '{}'.").format(portal_name))
            if 'main-menu' in portal:
                for entry in portal['main-menu']:
                    if 'url_name' in entry:
                        try:
                            reverse(
                                entry['url_name'],
                                kwargs={'url_prefix': 'portal-config-theme'},
                            )
                        except Exception:
                            raise RuntimeError(
                                _("Portal '{}': main menu entry url_name '{}' does not exists.").format(
                                    portal_name, entry['url_name']
                                )
                            )
            else:
                warn(_("Portal '{}' doesn't have a main-menu entry.").format(portal_name))

        # Build user settings forms from user settings registry
        self.user_settings = {}
        for app in apps.get_app_configs():
            if hasattr(app, 'biom_aid'):
                for key, setting in app.biom_aid.get('user-settings', {}).items():
                    if key in self.user_settings:
                        raise RuntimeError(_("Impossible d'écraser une préférence existante : {}").format(key))
                    self.user_settings[key] = setting
            if hasattr(app, 'biom_aid_alert_categories'):
                for key, category in app.biom_aid_alert_categories.items():
                    if 'user_settings' in category:
                        for s_key, setting in category['user_settings'].items():
                            key = 'notifications.' + app.name + '.' + key + '.' + s_key
                            self.user_settings[key] = deepcopy(setting)

        self.user_settings_forms = {
            'main': user_settings_form_factory(
                'MainUserSettings',
                BaseSmartForm,
                self.user_settings_categories,
                self.user_settings,
            ),
        }

        # Initialize universal config object
        config._initialize()

        # Register analytics processors
        def user_alerts(user):
            from common.models import Alert

            return Alert.objects.filter(destinataire=user, cloture__isnull=True).count()

        def user_counter():
            from common.models import User

            return User.objects.filter(last_login__gt=now() - datetime.timedelta(days=7), is_active=True).count()

        apps.get_app_config('analytics').register_data_processor('user_alerts', user_alerts)
        apps.get_app_config('analytics').register_data_processor('user_counter', user_counter)

    # def server_ready(self):
    #     # Setup analytics (if needed)
    #     from analytics import data

    #     data.set_datasource(
    #         'common.users-count', processor=lambda: User.objects.filter(last_login__isnull=False, is_active=True).count()
    #     )
    #     data.set_datasource('common.users-count-lastweek', processor='user_counter')
    #     data.set_datasource('common.user-active-alerts', processor='user_alerts')

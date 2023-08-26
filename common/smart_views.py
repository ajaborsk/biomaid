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
from django.db.models import (
    Value,
    ExpressionWrapper,
    TextField,
    F,
    IntegerField,
    Subquery,
    Sum,
    OuterRef,
    Case,
    When,
    Q,
)
from django.db.models.functions import Concat
from django.utils.timezone import now
from django.utils.translation import gettext as _

from django.apps import apps

from common.db_utils import class_roles_expression, user_choices, user_lookup
from common.models import Fournisseur, FournisseurEtablissement, Programme, UserUfRole, Alert, Uf
from dem.models import Demande
from document.views import all_documents_json_partial
from drachar.models import Previsionnel
from generic_comment.views import all_comments_json_partial

from smart_view.smart_view import (
    SmartView,
    ComputedSmartField,
    ToolsSmartField,
    CommentsSmartField,
    DocumentsSmartField,
)


class RoleScopeSmartView(SmartView):
    class Meta:
        model = UserUfRole
        permissions = {
            'create': ('ADM',),
            'write': {
                None: {
                    'ADM': {
                        'role_code': True,
                        'user': True,
                        'uf': True,
                        'service': True,
                        'centre_responsabilite': True,
                        'pole': True,
                        'site': True,
                        'etablissement': True,
                        'discipline': True,
                        'domaine_prefix': True,
                    },
                },
                'EDITABLE': {
                    'ADM': {
                        'role_code': True,
                        'user': True,
                        'uf': True,
                        'service': True,
                        'centre_responsabilite': True,
                        'pole': True,
                        'site': True,
                        'etablissement': True,
                        'discipline': True,
                        'domaine_prefix': True,
                    },
                },
            },
            'delete': {
                'EDITABLE': ('ADM',),
            },
        }
        columns = (
            'role_code',
            'user',
            'uf',
            'service',
            'centre_responsabilite',
            'pole',
            'site',
            'etablissement',
            'discipline',
            'domaine_prefix',
            'id',
            'roles',
            'state_code',
            'tools',
        )
        settings = {
            'user': {
                'title': _("Utilisateur"),
                'editor': 'autocomplete',
                'lookup': user_lookup,
                'choices': user_choices,
                'autocomplete': True,
            },
            'role_code': {
                'title': _("Rôle"),
            },
            'pole': {
                'title': _("Pôle"),
            },
            'centre_responsabilite': {
                'title': _("Centre de responsabilité"),
                'editor': 'autocomplete',
            },
            'domaine_prefix': {
                'title': _("Domaine (préfixe)"),
            },
            'uf': {
                'title': _("UF"),
                'editor': 'autocomplete',
                'autocomplete': True,
            },
        }
        user_filters = {
            'role_code': {'type': 'select'},
            'user': {'type': 'select'},
            'uf': {
                'type': 'select',
                'choices': lambda view_params, base_filter_args, base_filter_kwargs, manager: [{'label': 'Tous', 'value': "{}"}]
                + [
                    {
                        'label': choice['label'],
                        'value': '{{":or":[{{"uf__code":"{codeuf}"}}, {{"etablissement__uf__code__in":["{codeuf}"]}},'
                        '{{"service__uf__code__in":["{codeuf}"]}}, {{"centre_responsabilite__uf__code__in":["{codeuf}"]}},'
                        '{{"pole__uf__code__in":["{codeuf}"]}}, {{"site__uf__code__in":["{codeuf}"]}}]}}'.format(
                            codeuf=choice['code']
                        ),
                    }
                    for choice in Uf.objects.all().values('code', label=Concat(F('code'), Value(' - '), F('nom')))
                ],
            },
            'service': {'type': 'select'},
            'centre_responsabilite': {'type': 'select'},
            'pole': {'type': 'select'},
            'site': {'type': 'select'},
            'etablissement': {'type': 'select'},
        }
        form_layout = """
            # Fiche de rôle {{pk}}
                <---user--> <---role_code-->
                # Structure
                    <---uf--->  <---service--->
                    <---centre_responsabilite--->   <---pole--->
                    <---site--->      <---etablissement--->
                # Spécialité
                    <--discipline-->  <--domaine_prefix-->
        """
        menu_left = (
            {
                'label': _("Ajouter une fiche"),
                'url_name': 'common:role-create',
            },
        )

    state_code = (
        ComputedSmartField,
        {
            'special': 'state',
            'data': lambda view_params: ExpressionWrapper(Value('EDITABLE'), output_field=TextField()),
        },
    )

    roles = (
        ComputedSmartField,
        {
            'special': 'roles',
            'data': class_roles_expression(UserUfRole),
        },
    )
    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'common:role-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir la fiche de rôle"),
                },
                {
                    'tool': 'copy',
                    'url_name': 'common:role-copy',
                    'url_args': ('${id}',),
                    'tooltip': _("Copier la fiche de rôle"),
                },
                {
                    'tool': 'delete',
                    'url_name': 'common:role-ask-delete',
                    'url_args': ('${id}',),
                    'tooltip': _("Supprimer la fiche de rôle"),
                },
            ],
        },
    )


class ProgrammeSmartView(SmartView):
    class Meta:
        model = Programme
        permissions = {
            'create': (
                'ADM',
                'ARB',
                'DIS',
            ),
            'write': {
                None: {
                    'ADM': {
                        'calendrier': True,
                        'code': True,
                        'anteriorite': True,
                        'etablissement': True,
                        'site': True,
                        'pole': True,
                        'uf': True,
                        'nom': True,
                        'enveloppe': True,
                        'limit': True,
                        'arbitre': True,
                        'discipline': True,
                        'description': True,
                        'comments_sf': True,
                    },
                },
                'OPEN': {
                    'ADM': {
                        'calendrier': True,
                        'code': True,
                        'anteriorite': True,
                        'etablissement': True,
                        'site': True,
                        'pole': True,
                        'uf': True,
                        'nom': True,
                        'enveloppe': True,
                        'limit': True,
                        'arbitre': True,
                        'discipline': True,
                        'description': True,
                        'comments_sf': True,
                        'cloture': True,
                    },
                },
                'CLOSED': {
                    'ADM': {
                        'cloture': True,
                    },
                },
            },
        }
        model_fields = '__all__'
        # exclude = (
        #     'date_creation',
        #     'date_modification',
        # )
        settings = {
            'id': {
                'special': 'id',
                'hidden': True,
            },
            'calendrier': {
                'title': _("Campagne"),
            },
            'nom': {
                'format': 'string',
            },
            'uf': {
                'autocomplete': True,
            },
            'enveloppe': {
                'title': _("Enveloppe"),
                'help_text': _("Enveloppe estimative (non contraignante)"),
                'format': 'money',
                'decimal_symbol': ',',
                'thousands_separator': ' ',
                'currency_symbol': ' €',
                'symbol_is_after': True,
                'precision': 0,
            },
            'limit': {
                'title': _("Limite"),
                'help_text': _("Limite d'affectation : Il sera impossible de valider des demandes au delà de cette limite."),
                'format': 'money',
                'decimal_symbol': ',',
                'thousands_separator': ' ',
                'currency_symbol': ' €',
                'symbol_is_after': True,
                'precision': 0,
            },
            'consumed': {
                'title': _("Consommé"),
                'help_text': _("Enveloppe consommée"),
                'format': 'money',
                'decimal_symbol': ',',
                'thousands_separator': ' ',
                'currency_symbol': ' €',
                'symbol_is_after': True,
                'precision': 0,
            },
            'anteriorite': {
                'title': "Code DRAV94",
            },
            'arbitre': {
                'autocomplete': True,
                # La SmartView peut détecter seule les choix à faire mais comme elle ne dispose pas d'expression
                # Django pour créer l'étiquette de ces choix (seulement la méthode __str__() du modèle User, qui est du pur python)
                # C'est beaucoup plus long car elle doit faire de multiples requêtes SQL.
                # En utilisant une fonction Django, tout se fait en une unique requête SQL,
                #  au lieu d'une par utilisateur de la table !
                # l'utilisation d'une méthode (au lieu d'une fonction lambda) rend le code un peu plus lisible
                'lookup': user_lookup,
                'choices': user_choices,
                # 'choices': lambda dummy=None: User.objects.all().values_list(
                #    'pk', Concat(F('first_name'), Value(' '), F('last_name'), Value(" ("), F('username'), Value(")"))
                # )
            },
        }
        columns = (
            'id',
            'roles',
            'state_code',
            'calendrier',
            'etablissement',
            'site',
            'pole',
            'uf',
            'code',
            'anteriorite',
            'nom',
            'enveloppe',
            'limit',
            'distribue',
            'previsionnel_total',
            'consumed',
            'arbitre',
            'discipline',
            'description',
            'date_creation',
            'date_modification',
            'cloture',
            'documents_sf',
            'comments_sf',
            'tools',
        )
        user_filters = {
            'discipline': {'type': 'select'},
            'campagne': {'fieldname': 'calendrier', 'type': 'select'},
            'etablissement': {'type': 'select'},
            'active': {
                'label': _("Actif"),
                'fieldname': 'cloture',
                'type': 'select',
                'choices': [
                    {'label': _("Tous"), 'value': '{}'},
                    {'label': _("Ouverts"), 'value': '{"cloture__isnull":true}'},
                    {'label': _("Fermés"), 'value': '{"cloture__isnull":false}'},
                ],
            },
        }
        menu_left = ({'label': 'Ajouter un programme', 'url_name': 'common:programme-create'},)
        form_layout = """
        #
            # Informations de base
                <code> <nom>
                <calendrier> 
                <etablissement> <site>
                <pole> <uf>
                <discipline> <arbitre>
                <enveloppe> <limit>
                <anteriorite> <cloture>
                <description+--->
            # Documents joints
                <documents_sf+--->
            # Commentaires
                <comments_sf+--->
        """

    distribue = (
        ComputedSmartField,
        {
            'title': _("Pré-distribué"),
            'format': 'money',
            'decimal_symbol': ',',
            'thousands_separator': ' ',
            'currency_symbol': ' €',
            'symbol_is_after': True,
            'precision': 0,
            'data': lambda view_params: ExpressionWrapper(
                Subquery(
                    Demande.objects.order_by()
                    .values('programme')
                    .filter(programme=OuterRef('pk'), arbitrage_commission__valeur=True)
                    .annotate(tot=Sum('enveloppe_allouee'))
                    .values('tot')
                ),
                output_field=IntegerField(),
            ),
        },
    )
    previsionnel_total = (
        ComputedSmartField,
        {
            'title': _("Prévisionnel"),
            'format': 'money',
            'decimal_symbol': ',',
            'thousands_separator': ' ',
            'currency_symbol': ' €',
            'symbol_is_after': True,
            'precision': 0,
            'data': lambda view_params: ExpressionWrapper(
                Subquery(
                    Previsionnel.objects.order_by()
                    .values('programme')
                    .filter(programme=OuterRef('pk'))
                    .annotate(total=Sum('budget'))
                    .values('total')
                ),
                output_field=IntegerField(),
            ),
        },
    )
    state_code = (
        ComputedSmartField,
        {
            'special': 'state',
            'data': lambda view_params: ExpressionWrapper(
                Case(
                    When(
                        Q(cloture__isnull=True) | Q(cloture__gt=now()),
                        then=Value('OPEN'),
                    ),
                    default=Value('CLOSED'),
                ),
                output_field=TextField(),
            ),
            'depends': [
                'cloture',
            ],
        },
    )

    roles = (
        ComputedSmartField,
        {
            'special': 'roles',
            'data': class_roles_expression(Programme),
        },
    )
    # Do not use 'comments' since this is a model fieldname
    comments_sf = (
        CommentsSmartField,
        {
            'title': 'Commentaires',
            'data': all_comments_json_partial(Meta.model),  # Hum... Sans doute possible de le configurer par défaut...
        },
    )

    documents_sf = (
        DocumentsSmartField,
        {
            'title': 'Documents joints',
            'data': all_documents_json_partial(Meta.model),  # Hum... Sans doute possible de le configurer par défaut...
        },
    )

    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'common:programme-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir le programme"),
                },
                {
                    'tool': 'copy',
                    'url_name': 'common:programme-copy',
                    'url_args': ('${id}',),
                    'tooltip': _("Copier le programme"),
                },
                {
                    'tool': 'delete',
                    'url_name': 'common:programme-ask-delete',
                    'url_args': ('${id}',),
                    'tooltip': _("Supprimer le programme"),
                },
            ],
        },
    )


def _get_alert_categories():
    categories = {}
    for cfg in apps.get_app_configs():
        if hasattr(cfg, 'biom_aid_alert_categories'):
            for category_name, category in cfg.biom_aid_alert_categories.items():
                categories[cfg.name + '.' + category_name] = category['label']
    return categories


class UserAlertsSmartView(SmartView):
    class Meta:
        model = Alert
        permissions = {
            'create': None,
            'delete': None,
            'write': {
                None: {
                    'OWN': {
                        'commentaire': True,
                    }
                },
            },
        }
        columns = (
            'niveau',
            'destinataire',
            'categorie',
            'intitule',
            'date_creation',
            'date_activation',
            'date_lecture',
            'cloture',
            'commentaire',
        )
        settings = {
            'intitule': {
                'footer_data': 'count',
                'format': 'html',
            },
            'categorie': {
                'format': 'choice',
                'editor': 'autocomplete',
                'choices': _get_alert_categories(),
            },
        }
        user_filters = {
            'niveau': {
                'type': 'select',
                'choices': {
                    'fieldname': 'niveau',
                    'label': F('niveau'),
                    'sort': F('niveau'),
                },
            },
            'categorie': {'type': 'select'},
            'destinataire': {
                'type': 'select',
                'choices': {
                    'fieldname': 'destinataire',
                    'label': Concat(
                        F('destinataire__first_name'),
                        Value(" "),
                        F('destinataire__last_name'),
                    ),
                    'sort': F('destinataire'),
                },
            },
            'cloture': {
                'label': _("En cours"),
                'type': 'select',
                'choices': (
                    {'label': _("Oui"), 'value': '{"cloture__isnull":true}'},
                    {'label': _("Non"), 'value': '{"cloture__isnull":false}'},
                    {'label': _("Tout"), 'value': '{}'},
                ),
            },
        }


class MyAlertsSmartView(UserAlertsSmartView):
    class Meta:
        columns__remove = ('destinataire',)
        user_filters__remove = ('destinataire',)

        def base_filter(self, view_params: dict):
            return ((), {'destinataire': view_params['user']})


class FournisseurSmartView(SmartView):
    class Meta:
        model = Fournisseur
        permissions = {
            'create': ('ADM',),
            'delete': ('ADM',),
            'write': {
                None: {
                    'ADM': {
                        'code': True,
                        'nom': True,
                    }
                },
                'EDITABLE': {
                    'ADM': {
                        'code': True,
                        'etablissement': True,
                        'fournisseur': True,
                    },
                },
            }
        }
        columns = (
            'id',
            'roles',
            'state_code',
            'code',
            'nom',
            'tools',
        )
        user_filters = {
            'contient': {
                'type': 'contains',
                'fields': ['code', 'nom'],
            },
        }
        menu_left = ({'label': 'Ajouter un fournisseur', 'url_name': 'common:fournisseur-create'},)
        form_layout = """
        #
            # Fournisseur
                <code> <nom>
        """
    roles = (
        ComputedSmartField,
        {
            'hidden': True,
            'special': 'roles',
            'data': class_roles_expression(Fournisseur),
        },
    )
    state_code = (
        ComputedSmartField,
        {
            'special': 'state',
            'hidden': True,
            'data': lambda vc: Value('EDITABLE'),
        },
    )
    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'common:fournisseur-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir la fiche de fourisseur générique"),
                },
                {
                    'tool': 'delete',
                    'url_name': 'common:fournisseur-ask-delete',
                    'url_args': ('${id}',),
                    'tooltip': _("Supprimer la fiche de fourisseur générique"),
                },
            ],
        },
    )

class FournisseurEtablissementSmartView(SmartView):
    class Meta:
        model = FournisseurEtablissement
        permissions = {
            'create': ('ADM', 'MAN'),
            'delete': ('ADM'),
            'write': {
                None: {
                    'ADM': {
                        'code': True,
                        'etablissement': True,
                        'fournisseur': True,
                    }
                },
                'EDITABLE': {
                    'ADM': {
                        'code': True,
                        'etablissement': True,
                        'fournisseur': True,
                    },
                },
            },
        }
        columns = (
            'id',
            'roles',
            'state_code',
            'code',
            'etablissement',
            'fournisseur',
            'tools',
        )
        user_filters = {
            'contient': {
                'type': 'contains',
                'fields': ['code', 'etablissement', 'fournisseur'],
            },
            'etablissement': {'type': 'select'},
            'fournisseur': {'type':'select'},
        }
        menu_left = ({'label': "Ajouter un fournisseur d'établissement", 'url_name': 'common:fournisseuretablissement-create'},)
        form_layout = """
        #
            # Fournisseur
                <code> <etablissement>
                <fournisseur>
        """
    roles = (
        ComputedSmartField,
        {
            'hidden': True,
            'special': 'roles',
            'data': class_roles_expression(FournisseurEtablissement),
        },
    )
    state_code = (
        ComputedSmartField,
        {
            'special': 'state',
            'hidden': True,
            'data': lambda vc: Value('EDITABLE'),
        },
    )
    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'common:fournisseuretablissement-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir la fiche de fourisseur établissement"),
                },
                {
                    'tool': 'delete',
                    'url_name': 'common:fournisseuretablissement-ask-delete',
                    'url_args': ('${id}',),
                    'tooltip': _("Supprimer la fiche de fournisseur établissement"),
                },
            ],
        },
    )
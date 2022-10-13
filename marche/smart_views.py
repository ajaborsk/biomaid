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
from django.apps import apps
from django.db.models import CharField, ExpressionWrapper, F, OuterRef, TextField, Value
from django.db.models.functions import Coalesce, Concat
from django.utils.translation import gettext as _

from generic_comment.views import all_comments_json_partial
from common.models import UserUfRole
from common.db_utils import class_roles_expression
from document.views import all_documents_json_partial
from smart_view.smart_view import (
    SmartView,
    ToolsSmartField,
    ComputedSmartField,
    CommentsSmartField,
    DocumentsSmartField,
)
from .models import ExceptionMarche, Marche


class MarcheSmartView(SmartView):
    class Meta:
        model = Marche
        permissions = {
            'create': ('ADM', 'ACH', 'EXP'),
            'delete': {
                'PREVU': (
                    'ACH',
                    'ADM',
                ),
                'EN_COURS': (
                    'ACH',
                    'ADM',
                ),
                'TERMINE': (
                    'ACH',
                    'ADM',
                ),
            },
            'write': {
                None: {
                    'ADM': {
                        'num_marche': True,
                        'intitule': True,
                        'type_procedure': True,
                        'date_debut': True,
                        'date_notif': True,
                        'expert_metier': True,
                        'commentaire': True,
                        'comments_sf': True,
                    },
                },
                'PREVU': {
                    'ACH': {
                        'intitule': True,
                        'commentaire': True,
                        'expert_metier': True,
                        'comments_sf': True,
                        'date_debut': True,
                        'date_notif': True,
                    },
                },
                'EN_COURS': {
                    'ACH': {
                        'intitule': True,
                    },
                    'ADM': {
                        'intitule': True,
                        'expert_metier': True,
                        'commentaire': True,
                        'comments_sf': True,
                        'date_debut': True,
                        'date_notif': True,
                    },
                },
                'TERMINE': {
                    'ACH': {
                        'expert_metier': True,
                        'intitule': True,
                    },
                },
            },
        }
        settings = {
            'id': {
                'hidden': True,
            },
            'num_marche': {
                'title': _("Numéro du marché"),
                'help_text': _("Numéro donné par le pouvoir adjudicateur"),
            },
            'intitule': {
                'format': 'string',
            },
            'date_debut': {
                'format': 'date',
            },
            'date_notif': {
                'format': 'date',
            },
            'acheteur': {
                'format': 'choice',
                'editor': 'autocomplete',
                'choices': lambda view_params: tuple(
                    UserUfRole.objects.order_by()
                    .filter(role_code='ACH')
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
            # Limitons le choix pour l'expert métier aux personnes qui ont au moins un rôle d'expert
            # L'utilisation d'une fonction (ici une fonction lambda) permet de faire cette évaluation à chaque instanciation
            # (ouverture de la page) et non pas seulement au lancement de Django
            'expert_metier': {
                'format': 'choice',
                'editor': 'autocomplete',
                'choices': lambda view_params: tuple(
                    UserUfRole.objects.order_by()
                    .filter(role_code='EXP')
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
        }
        menu_left = ({'label': 'Ajouter un marché', 'url_name': 'marche:marches-create'},)
        columns = (
            'id',
            'num_marche',
            'intitule',
            'type_procedure',
            'date_notif',
            'date_debut',
            'duree',
            'acheteur',
            'expert_metier',
            'commentaire',
            'cloture',
            'documents_sf',
            'comments_sf',
            'tools',
            'roles',
            'state',
        )
        selectable_columns = (
            'num_marche',
            'intitule',
            'type_procedure',
            'date_notif',
            'date_debut',
            'duree',
            'acheteur',
            'expert_metier',
            'commentaire',
            'cloture',
            'documents_sf',
            'comments_sf',
        )
        user_filters = {
            'acheteur': {'type': 'select'},
            'expert_metier': {'type': 'select'},
        }
        form_layout = """
            #
                # Identification
                    <--num_marche--> <--intitule-->
                    §Simple HTML rendu comme template : Numéro marché = {{ instance.num_marche }}
                # Autres renseignements
                    <--date_notif-->  <-date_debut->
                    <type_procedure>  <---duree-->
                    <commentaire----+------------>
                    <---acheteur--->  <expert_metier>
                    $marche/subform_template.html
                # Documents joints
                    <--documents_sf-+--+--+->
                # Commentaires
                    <--comments_sf-+--+--+->
        """

    #                    <--comments_sf-+---------->

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
                    'url_name': 'marche:marches-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir le marché"),
                },
                {
                    'tool': 'copy',
                    'url_name': 'marche:marches-copy',
                    'url_args': ('${id}',),
                    'tooltip': _("Copier le marché"),
                },
                {
                    'tool': 'delete',
                    'url_name': 'marche:marches-ask-delete',
                    'url_args': ('${id}',),
                    'tooltip': _("Supprimer le marché"),
                },
            ],
        },
    )
    roles = (
        ComputedSmartField,
        {
            'special': 'roles',
            'data': class_roles_expression(),
        },
    )
    state = (
        ComputedSmartField,
        {
            'special': 'state',
            'data': Value('EN_COURS', output_field=TextField()),
        },
    )


def fournisseur_weak_link(view_params):
    try:
        fournisseur_model = apps.get_model('extable', 'ExtFournisseur', True)
    except LookupError:
        # No extable 'ExtFournisseur' model
        return Value("----")

    return Coalesce(
        fournisseur_model.objects.filter(no_fournisseur_fr=OuterRef('code_fournisseur')).values('intitule_fournisseur_fr'),
        Value('- #ref ? -'),
        output_field=CharField(),
    )


class ExceptionMarcheSmartView(SmartView):
    class Meta:
        model = ExceptionMarche
        permissions = {
            'create': (
                'ADM',
                'P-ACH',
            ),
            'write': {
                None: {
                    'P-ACH': {
                        'code_fournisseur': True,
                        'prefixe_compte': True,
                        'code_hm': True,
                        'description': True,
                        'date_debut': True,
                        'date_fin': True,
                        'no_marche': True,
                        'comments_sf': True,
                    },
                },
                'PREVU': {
                    'P-ACH': {
                        'code_fournisseur': True,
                        'prefixe_compte': True,
                        'code_hm': True,
                        'description': True,
                        'date_debut': True,
                        'date_fin': True,
                        'no_marche': True,
                        'comments_sf': True,
                    },
                },
                'EN_COURS': {
                    'P-ACH': {
                        'code_fournisseur': True,
                        'prefixe_compte': True,
                        'code_hm': True,
                        'description': True,
                        'date_debut': True,
                        'date_fin': True,
                        'no_marche': True,
                        'comments_sf': True,
                    },
                },
                'JUSTE_TERMINE': {
                    'P-ACH': {
                        'code_fournisseur': True,
                        'prefixe_compte': True,
                        'code_hm': True,
                        'description': True,
                        'date_debut': True,
                        'date_fin': True,
                        'no_marche': True,
                        'comments_sf': True,
                    },
                },
                'ARCHIVE': {
                    'P-ACH': {
                        'code_fournisseur': True,
                        'prefixe_compte': True,
                        'code_hm': True,
                        'description': True,
                        'date_debut': True,
                        'date_fin': True,
                        'no_marche': True,
                        'comments_sf': True,
                    },
                },
            },
            'delete': {
                'OWN': True,
            },
        }

        columns = (
            'id',
            'state',
            'roles',
            'code_fournisseur',
            'nom_fournisseur',
            'prefixe_compte',
            'code_hm',
            'description',
            'date_debut',
            'date_fin',
            'no_marche',
            'comments_sf',
            'tools',
        )

        settings = {
            'date_debut': {
                'format': 'date',
            },
            'date_fin': {
                'format': 'date',
            },
        }

        form_layout = """
        # Autorisation Hors-Marché interne
            #
                <code_fournisseur> <prefixe_compte>
                <code_hm> <description--+-->
                <date_debut> <date_fin>
                <no_marche>
            # Commentaires
                <comments_sf>
        """
        menu_left = ({'label': 'Ajouter une autorisation', 'url_name': 'marche:exception_marche-create'},)
        exports = {
            'xlsx': {
                'engine': 'xlsx',
                'label': 'Microsoft Excel 2003+',
                'filename': 'Exceptions_marché.xlsx',
            }
        }

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
                    'url_name': 'marche:exception_marche-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir l'autorisation'"),
                },
                {
                    'tool': 'copy',
                    'url_name': 'marche:exception_marche-copy',
                    'url_args': ('${id}',),
                    'tooltip': _("Copier l'autorisation"),
                },
                {
                    'tool': 'delete',
                    'url_name': 'marche:exception_marche-ask-delete',
                    'url_args': ('${id}',),
                    'tooltip': _("Supprimer l'autorisation"),
                },
            ],
        },
    )
    nom_fournisseur = (
        ComputedSmartField,
        {
            'title': _("Nom fournisseur"),
            'data': fournisseur_weak_link,
            'depends': ['code_fournisseur'],
        },
    )
    roles = (
        ComputedSmartField,
        {
            'special': 'roles',
            'data': class_roles_expression(),
        },
    )
    state = (
        ComputedSmartField,
        {
            'special': 'state',
            'data': Value('EN_COURS', output_field=TextField()),
            'depends': ['date_debut', 'date_fin'],
        },
    )

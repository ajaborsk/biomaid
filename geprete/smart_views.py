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
from geprete.models import Geprete, Gessaye

from django.db.models import F, TextField, Value
from django.db.models.functions import Concat
from django.utils.translation import gettext as _
from document.views import all_documents_json_partial
from generic_comment.views import all_comments_json_partial

from common.models import UserUfRole
from common.db_utils import class_roles_expression

from smart_view.smart_view import (
    SmartView,
    ToolsSmartField,
    ComputedSmartField,
    CommentsSmartField,
    DocumentsSmartField,
)


class GepreteSmartView(SmartView):
    class Meta:
        model = Geprete
        permissions = {
            'create': ('ADM', 'ACH', 'EXP'),
            'delete': {'0': ('ADM', 'ACH', 'EXP')},
            'write': {
                None: {
                    'ADM': {
                        'marque': True,
                        'type': True,
                        'num_inv': True,
                        'uf_preteur': True,
                        'contact_preteur': True,
                        'uf_receveur': True,
                        'contact_receveur': True,
                        'date_demande': True,
                        'debut_pret': True,
                        'fin_pret': True,
                        'duree_pret': True,
                        'unite': True,
                        'documents': True,
                        'comments': True,
                    },
                },
                '0': {
                    'ADM': {
                        'marque': True,
                        'type': True,
                        'num_inv': True,
                        'uf_preteur': True,
                        'contact_preteur': True,
                        'uf_receveur': True,
                        'contact_receveur': True,
                        'date_demande': True,
                        'debut_pret': True,
                        'fin_pret': True,
                        'duree_pret': True,
                        'unite': True,
                        'documents': True,
                        'comments': True,
                    },
                },
            },
        }
        settings = {
            'num_inv': {
                'title': _("N° d'inventaire"),
            },
            'marque': {'title': _("Marque")},
            'type': {'title': _("Type d'appareil")},
            'uf_preteur': {
                'title': _("Uf du prêteur"),
                'autocomplete': True,
            },
            'contact_preteur': {'title': _("Contact du prêteur")},
            'uf_receveur': {
                'title': _("Uf du receveur"),
                'autocomplete': True,
            },
            'contact_receveur': {'title': _("Contact du receveur")},
            'date_demande': {'title': _("Date de demande du prêt")},
            'debut_pret': {'title': _("Début du prêt")},
            'unite': {'title': _("en")},
            'fin_pret': {'title': _("Fin du prêt")},
            'duree_pret': {'title': _("Durée estimée du prêt")},
            'document_pret': {'title': _("Documents joints")},
        }
        menu_left = ({'label': 'Ajouter un prêt', 'url_name': 'geprete:listegeprete-create'},)
        columns = (
            'id',
            'num_inv',
            'marque',
            'type',
            'uf_preteur',
            'uf_receveur',
            'contact_preteur',
            'contact_receveur',
            'date_demande',
            'debut_pret',
            'unite',
            'fin_pret',
            'duree_pret',
            'comment_pret',
            'document_pret',
            'tools',
            'roles',
            'state',
        )
        selectable_columns = (
            'num_inv',
            'marque',
            'type',
            'uf_preteur',
            'uf_receveur',
            'contact_preteur',
            'contact_receveur',
            'date_demande',
            'debut_pret',
            'unite',
            'fin_pret',
            'duree_pret',
            'comment_pret',
            'document_pret',
        )

        user_filters = {
            'uf_preteur': {'type': 'select'},
            'uf_receveur': {'type': 'select'},
        }
        form_layout = """
            #
                # Informations principales
                    <--num_inv--> <--uf_receveur-->
                    <--contact_receveur-->
                    <--debut_pret--> <--fin_pret-->
                # Autres informations
                    <--marque--> <--type-->
                    <--uf_preteur--> <--contact_preteur-->
                    <--date_demande-->
                    <--duree_pret--> <--unite-->
                # Documents joints
                    <--document_pret-+--+--+->
                # Commentaires
                    <--comment_pret-+--+--+->
            """

    document_pret = (
        DocumentsSmartField,
        {'title': 'Document joint', 'data': all_documents_json_partial(Meta.model)},
    )

    comment_pret = (
        CommentsSmartField,
        {
            'title': 'Commentaires',
            'data': all_comments_json_partial(Meta.model),
        },
    )

    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'geprete:listegeprete-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir le prêt"),
                },
                {
                    'tool': 'copy',
                    'url_name': 'geprete:listegeprete-copy',
                    'url_args': ('${id}',),
                    'tooltip': _("Copier le prêt"),
                },
                {
                    'tool': 'delete',
                    'url_name': 'geprete:listegeprete-ask-delete',
                    'url_args': ('${id}',),
                    'tooltip': _("Supprimer le prêt"),
                },
            ],
        },
    )

    roles = (
        ComputedSmartField,
        {
            'special': 'roles',
            'data': class_roles_expression(Geprete),
        },
    )
    state = (
        ComputedSmartField,
        {
            'special': 'state',
            'data': Value('0', output_field=TextField()),
        },
    )


# TODO : marque et type se remplissent tout seul àpdu n° d'inventaire
# TODO : Uf du prêteur se remplisse tout seul auss


class GessayeSmartView(SmartView):
    class Meta:
        def choix_inge(view_params):
            return (
                UserUfRole.records.filter(role_code='EXP')
                .annotate(fullname=Concat(F('user__first_name'), Value(" "), F('user__last_name')))
                .values_list('user', 'fullname')
                .distinct()
            )

        model = Gessaye
        permissions = {
            'create': ('ADM', 'ACH', 'EXP'),
            'delete': {'0': ('ADM', 'ACH', 'EXP')},
            'write': {
                None: {
                    'ADM': {
                        'numero_de_serie': True,
                        'marque': True,
                        'unite_duree': True,
                        'quantite': True,
                        'type': True,
                        'accessoires': True,
                        'descriptif': True,
                        'num_ce': True,
                        'debut': True,
                        'fin': True,
                        'duree': True,
                        'reprise': True,
                        'ingenieur_responsable': True,
                        'unite_fonctionnelle': True,
                        'nom_emprunteur': True,
                        'fournisseur': True,
                        'contact_fournisseur': True,
                        'coord_fournisseur': True,
                        'commentaire': True,
                        'document_essai': True,
                        'comment_essai': True,
                    },
                },
                '0': {
                    'ADM': {
                        'numero_de_serie': True,
                        'marque': True,
                        'unite_duree': True,
                        'quantite': True,
                        'type': True,
                        'accessoires': True,
                        'descriptif': True,
                        'num_ce': True,
                        'debut': True,
                        'fin': True,
                        'duree': True,
                        'reprise': True,
                        'ingenieur_responsable': True,
                        'unite_fonctionnelle': True,
                        'nom_emprunteur': True,
                        'fournisseur': True,
                        'contact_fournisseur': True,
                        'coord_fournisseur': True,
                        'commentaire': True,
                        'document_essai': True,
                        'comment_essai': True,
                    },
                },
            },
        }
        settings = {
            'id': {
                'hidden': True,
            },
            'numero_de_serie': {'title': _("N° de série")},
            'quantite': {'title': _("Quantité")},
            'type': {'title': _("Type")},
            'marque': {'title': _("Marque")},
            'accessoires': {'title': _("Accessoires")},
            'descriptif': {'title': _("Descriptif")},
            'num_ce': {'title': _("N° de marquage CE")},
            'debut': {'title': _("Début de l'essai")},
            'fin': {'title': _("Fin de l'essai")},
            'reprise': {'title': _("Date de reprise")},
            'duree': {'title': _("Durée de l'essai")},
            'unite_duree': {'title': _("en")},
            'ingenieur_responsable': {
                'title': _("Ingénieur(e)"),
                'autocomplete': True,
                'choices': choix_inge,
            },
            'unite_fonctionnelle': {
                'title': _("Unité fonctionnelle"),
                'autocomplete': True,
            },
            'nom_emprunteur': {'title': _("Nom du demandeur de l'essai")},
            'fournisseur': {'title': _("Fournisseur")},
            'contact_fournisseur': {'title': _("Contact chez le fournisseur")},
            'coord_fournisseur': {'title': _("Cordonnées du fournisseur")},
            'commentaire': {'title': _("Commentaire")},
        }
        menu_left = ({'label': 'Ajouter un essai', 'url_name': 'geprete:listeessai-create'},)
        menu_right = (
            {
                'label': 'Télecharger',
                'entries': (
                    {
                        'label': "Fiche d'évaluation clinique",
                        'url': '/static/geprete/fiche_evaluation_clinique.doc',
                    },
                    {
                        'label': "Fiche d'évaluation technique",
                        'url': '/static/geprete/fiche_evaluation_technique.doc',
                    },
                ),
            },
        )
        columns = (
            'id',
            'numero_de_serie',
            'quantite',
            'type',
            'marque',
            'accessoires',
            'descriptif',
            'num_ce',
            'debut',
            'fin',
            'reprise',
            'duree',
            'unite_duree',
            'ingenieur_responsable',
            'unite_fonctionnelle',
            'nom_emprunteur',
            'fournisseur',
            'contact_fournisseur',
            'coord_fournisseur',
            'document_essai',
            'comment_essai',
            'tools',
            'roles',
            'state',
        )
        selectable_columns = (
            'numero_de_serie',
            'quantite',
            'type',
            'marque',
            'accessoires',
            'descriptif',
            'num_ce',
            'debut',
            'fin',
            'reprise',
            'duree',
            'unite_duree',
            'ingenieur_responsable',
            'unite_fonctionnelle',
            'nom_emprunteur',
            'fournisseur',
            'contact_fournisseur',
            'coord_fournisseur',
            'comment_essai',
            'document_essai',
        )
        user_filters = {  # a n'utiliser que sur des FOREIGNKEY, sinon ce type de filtre ne fonctionne pas
            'ingenieur_responsable': {'type': 'select'},
            'unite_fonctionnelle': {'type': 'select'},
        }

        form_layout = """
            #
                # Identification
                    <--numero_de_serie--> <--quantite-->
                    <--type--> <--marque-->
                    <--accessoires--> <--descriptif-->
                    <--num_ce-->
                # Autres informations
                    <--debut--> <--fin-->
                    <--reprise--> <--duree--> <--unite_duree-->
                    <--ingenieur_responsable-->
                    <--fournisseur--> <--contact_fournisseur--> <--coord_fournisseur-->
                    <--unite_fonctionnelle--> <--nom_emprunteur-->
                # Documents joints
                    <--document_essai-->
                # Commentaires
                    <--comment_essai-->
                """

    document_essai = (
        DocumentsSmartField,
        {'title': 'Autre document', 'data': all_documents_json_partial(Meta.model)},
    )

    comment_essai = (
        CommentsSmartField,
        {
            'title': 'Commentaires',
            'data': all_comments_json_partial(Meta.model),
        },
    )

    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'geprete:listeessai-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir l'essai"),
                },
                {
                    'tool': 'copy',
                    'url_name': 'geprete:listeessai-copy',
                    'url_args': ('${id}',),
                    'tooltip': _("Copier l'essai"),
                },
                {
                    'tool': 'delete',
                    'url_name': 'geprete:listeessai-ask-delete',
                    'url_args': ('${id}',),
                    'tooltip': _("Supprimer l'essai'"),
                },
            ],
        },
    )

    roles = (
        ComputedSmartField,
        {
            'special': 'roles',
            'data': class_roles_expression(Gessaye),
        },
    )
    state = (
        ComputedSmartField,
        {
            'special': 'state',
            'data': Value('0', output_field=TextField()),
        },
    )

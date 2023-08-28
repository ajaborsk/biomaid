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
from decimal import Decimal
from django.db.models import F, ExpressionWrapper, Value, TextField, Case, When, Q
from django.db.models.functions import Concat, Coalesce, Greatest
from django.utils.timezone import now
from django.utils.translation import gettext as _

from common.models import Discipline, UserUfRole, Fournisseur
from common.db_utils import AgeDays, class_roles_expression, filter_choices_from_column_values
from dem.apps import DRACHAR_DELAI_DEMANDE_TERMINEE
from dem.utils import roles_demandes_possibles
from smart_view.smart_fields import ConditionnalSmartField, ToolsSmartField
from smart_view.smart_view import SmartView, ComputedSmartField
from .models import Previsionnel, Dossier, LigneCommande, Dra, ContactLivraison


class DossierSmartView(SmartView):
    class Meta:
        model = Dossier
        columns = (
            'num_dossier',
            'nom_dossier',
            'proprietaire',
            'deadline',
            'commentaire',
        )


class NouvelleDraSmartView(SmartView):
    class Meta:
        model = LigneCommande
        permissions = {}
        columns = (
            'num_ligne',
            'num_previsionnel',
            'famille_achat',
            'num_compte',
            'a_inventorier',
            'num_dra',
            'classe',
            'cneh',
            'modele',
            'marque',
            'reference',
            'descriptif',
            'prix_unitaire_ht',
            'tva',
            'ref_mut',
            'eqpt_recup',
            'pv_reforme',
            'garantie',
            'date_reception',
            'date_mes',
        )
        selectable_columns = (
            'num_ligne',
            'num_previsionnel',
            'famille_achat',
            'num_compte',
            'a_inventorier',
            'num_ligne',
            'classe',
            'cneh',
            'modele',
            'marque',
            'reference',
            'descriptif',
            'prix_unitaire_ht',
            'tva',
            'ref_mut',
            'eqpt_recup',
            'pv_reforme',
            'garantie',
            'date_reception',
            'date_mes',
        )
        settings = {
            'num_dra': {
                'hidden': True,
            },
            'date_reception': {
                'editor': 'dateEditor',
                'datetime_format': '%d%m/%Y',
            },
            'date_mes': {
                'editor': 'dateEditor',
                'datetime_format': '%d%m/%Y',
            },
        }
        '''a faire filtre sur num de la DRA'''
        # user_filters = (
        #     {
        #         'name': 'num_dra',
        #         'type': 'select',
        #         'choices': filter_choices_from_column_values(Previsionnel, 'num_dmd__uf__code'),
        #     },
        # )
        exports = {
            'xlsx': {
                'engine': 'xlsx',
                'label': 'Microsoft Excel 2003+',
                'filename': "Demandes en cours.xlsx",
            }
        }


class PrevisionnelSmartView(SmartView):
    class Media(SmartView.Media):
        js = SmartView.Media.js + ('drachar/js/suivi-format.js',)

    class Meta:
        model = Previsionnel
        base_filter = ~Q(programme__discipline__code='TX')
        permissions = {
            # La creation des fiches prévivionnelles se fait exclusivement par le script dédié
            # et jamais par un utilisateur
            'create': (),
            'write': {
                # L'état est la fermeture de la ligne du prévisionnel, donc False signifie qu'on peut modifier...
                False: {
                    'OWN': {
                        'commentaire': True,
                        'commentaire_public': True,
                        'date_debut': True,
                        'suivi_besoin': True,
                        'suivi_achat': True,
                        'suivi_offre': True,
                        'suivi_appro': True,
                        'suivi_mes': True,
                        'montant_estime': True,
                        'montant_commande': True,
                        'solder_ligne': True,
                        'date_estimative_mes': True,
                    },
                    'DIS': {
                        'programme': True,
                        'solder_ligne': True,
                        'expert': True,
                        # Temporaire ? ou définitif ??
                        'commentaire': True,
                        'commentaire_public': True,
                        'date_debut': True,
                        'suivi_besoin': True,
                        'suivi_achat': True,
                        'suivi_offre': True,
                        'suivi_appro': True,
                        'suivi_mes': True,
                        'montant_estime': True,
                        'montant_commande': True,
                        'date_estimative_mes': True,
                    },
                    'RESPD': {
                        'programme': True,
                        'solder_ligne': True,
                        'expert': True,
                        # Temporaire ? ou définitif ??
                        'commentaire': True,
                        'commentaire_public': True,
                        'date_debut': True,
                        'suivi_besoin': True,
                        'suivi_achat': True,
                        'suivi_offre': True,
                        'suivi_appro': True,
                        'suivi_mes': True,
                        'montant_estime': True,
                        'montant_commande': True,
                        'date_estimative_mes': True,
                    },
                    'ARB': {
                        'uf': True,
                        'budget': True,
                        'commentaire': True,
                        'commentaire_public': True,
                    },
                    'EXP': {
                        'commentaire': True,
                        'commentaire_public': True,
                        # 'solder_ligne': True,
                        'date_debut': True,
                        'suivi_besoin': True,
                        'suivi_achat': True,
                        'suivi_offre': True,
                        'suivi_appro': True,
                        'suivi_mes': True,
                        'montant_estime': True,
                        'montant_commande': True,
                        'date_estimative_mes': True,
                    },
                },
                True: {
                    'DIS': {
                        'solder_ligne': True,
                    },
                    'RESPD': {
                        'solder_ligne': True,
                    },
                    'ARB': {
                        'solder_ligne': True,
                    },
                    'OWN': {
                        'suivi_mes': True,
                        'solder_ligne': True,  # Le propriétaire peut "désolder" un prévisionnel
                        'date_estimative_mes': True,
                        'commentaire': True,
                        'commentaire_public': True,
                    },
                },
            },
        }
        current_row_manager = True
        columns = (
            'num',
            'num_dmd',
            'demande_code',
            'discipline',
            'discipline_dmd',
            'programme',
            'uf',
            'nom_pole',
            'dmd_quantite',
            'dmd_libelle',
            'domaine',
            'budget',
            'commentaire_arbitre',
            'expert',
            'date_debut',
            'programme_dra',
            'ligne_dra',
            'best_amount',
            'suivi_besoin',
            'suivi_achat',
            'suivi_offre',
            'suivi_appro',
            'suivi_mes',
            'montant_commande',
            'ordered_amount',
            'amount_conditional',
            'solder_ligne',
            'commentaire_public',
            'date_estimative_mes',
            'commentaire',
            'interface',
            'roles',
        )
        selectable_columns = (
            # 'num',
            'discipline',
            'programme',
            'uf',
            'nom_pole',
            'dmd_quantite',
            'dmd_libelle',
            'domaine',
            'budget',
            'commentaire_arbitre',
            'expert',
            'date_debut',
            'programme_dra',
            'ligne_dra',
            'best_amount',
            'suivi_besoin',
            'suivi_achat',
            'suivi_offre',
            'suivi_appro',
            'suivi_mes',
            'amount_conditional',
            'solder_ligne',
            'commentaire_public',
            'date_estimative_mes',
            'commentaire',
            'interface',
        )
        settings = {
            'num': {
                'hidden': True,
            },
            'num_dmd': {
                'hidden': True,
            },
            'uf': {
                'editor': 'autocomplete',
            },
            'budget': {
                'title': _("Enveloppe"),
                'format': 'money',
                'decimal_symbol': ",",
                'thousands_separator': " ",
                'currency_symbol': " €",
                'symbol_is_after': True,
                'precision': 0,
                'max_width': 95,
                'footer_data': "sum",
            },
            'best_amount': {
                'title': _("Meilleur Montant estimé"),
                'format': 'money',
                'decimal_symbol': ",",
                'thousands_separator': " ",
                'currency_symbol': " €",
                'symbol_is_after': True,
                'precision': 0,
                'max_width': 95,
                'footer_data': "sum",
            },
            'montant_commande': {
                'title': _("Montant commandé"),
                'hidden': True,
                'format': 'money',
                'decimal_symbol': ",",
                'thousands_separator': " ",
                'currency_symbol': " €",
                'symbol_is_after': True,
                'precision': 0,
                'max_width': 95,
                'footer_data': "sum",
            },
            'expert': {
                'title': _("Chargé opération"),
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
            'suivi_besoin': {
                'formatter': "'suivi'",
            },
            'suivi_achat': {
                'formatter': "'suivi'",
            },
            'suivi_offre': {
                'formatter': "'suivi'",
            },
            'suivi_appro': {
                'formatter': "'suivi_commande'",
            },
            'suivi_mes': {
                'formatter': "'suivi'",
            },
            'date_debut': {
                'editor': 'dateEditor',
                'datetime_format': '%d/%m/%Y',
            },
            'date_estimative_mes': {
                'editor': 'dateEditor',
                'datetime_format': '%m/%Y',
            },
            'solder_ligne': {
                'title': _("Soldé"),
                'special': 'state',
                'hidden': False,
            },
            'interface': {
                'format': 'html',
            },
            'montant_engage': {
                'title': _("Montant engagé"),
                'format': 'money',
                'decimal_symbol': ",",
                'thousands_separator': " ",
                'currency_symbol': " €",
                'symbol_is_after': True,
                'precision': 0,
                'max_width': 95,
                'footer_data': "sum",
            },
            'montant_liquide': {
                'title': _("Montant liquidé"),
                'format': 'money',
                'decimal_symbol': ",",
                'thousands_separator': " ",
                'currency_symbol': " €",
                'symbol_is_after': True,
                'precision': 0,
                'max_width': 95,
                'footer_data': "sum",
            },
            'valeur_inventaire': {
                'title': _("Valeur dans l'inventaire"),
                'format': 'money',
                'decimal_symbol': ",",
                'thousands_separator': " ",
                'currency_symbol': " €",
                'symbol_is_after': True,
                'precision': 0,
                'max_width': 95,
                'footer_data': "sum",
            },
        }
        user_filters = {
            'expert': {
                'type': 'select',
                'choices': filter_choices_from_column_values(
                    Previsionnel,
                    'expert',
                    label_expr=Concat(F('expert__first_name'), Value(' '), F('expert__last_name')),
                    order_by='expert__last_name',
                ),
            },
            'discipline': {
                'type': 'select',
                'choices': filter_choices_from_column_values(Previsionnel, 'programme__discipline__nom'),
            },
            'campaign': {
                'label': _("Campagne"),
                'type': 'select',
                'choices': filter_choices_from_column_values(
                    Previsionnel,
                    'num_dmd__calendrier__code',
                    label_expr=Concat(F('num_dmd__calendrier__code'), Value(' - '), F('num_dmd__calendrier__nom')),
                    order_by='num_dmd__calendrier__code',
                ),
            },
            'programme': {
                'label': _("Programme"),
                'type': 'select',
                'choices': filter_choices_from_column_values(
                    Previsionnel,
                    'programme',
                    label_expr=Concat(F('programme__code'), Value(' - '), F('programme__nom')),
                    order_by='programme__code',
                ),
            },
            'nom_pole': {
                'label': _("Pôle"),
                'type': 'select',
                'choices': filter_choices_from_column_values(Previsionnel, 'uf__pole__nom'),
            },
            'nom_uf': {
                'label': _("UF"),
                'type': 'select',
                'choices': filter_choices_from_column_values(
                    Previsionnel,
                    'uf',
                    label_expr=Concat(F('uf__code'), Value(' - '), F('uf__nom')),
                ),
            },
            'demande_contains': {
                'type': 'contains',
                'fieldnames': [
                    'num_dmd__libelle',
                    'num_dmd__nom_projet',
                    'num_dmd__description',
                    'num_dmd__commentaire_cadre_sup',
                    'num_dmd__decision_soumission',
                    'num_dmd__commentaire_biomed',
                    'num_dmd__commentaire_provisoire_commission',
                    'num_dmd__commentaire_definitif_commission',
                    'num_dmd__arg_commentaire_im',
                    'num_dmd__arg_commentaire_or',
                    'num_dmd__arg_commentaire_r',
                    'num_dmd__arg_commentaire_pcp',
                    'num_dmd__arg_commentaire_cp',
                    'num_dmd__arg_commentaire_pe',
                    'num_dmd__arg_commentaire_n',
                    'num_dmd__arg_commentaire_ir',
                    'num_dmd__arg_commentaire_gf',
                    'num_dmd__arg_commentaire_m',
                    'num_dmd__autre_argumentaire',
                ],
                'label': _("Demande contient"),
            },
            'solder_ligne': {
                'type': 'select',
                'label': _("Ligne soldée"),
            },
        }
        row_styler = {
            'fieldname': 'solder_ligne',
            'styles': {
                False: ("background:#fff", "Demande à faire ou en cours"),
                True: ("background:#ddd", "Demande Soldée"),
                '0': ('background:#aaa', _("Avancement : 0- Sans objet")),
                '1': ('background:#afa', _("Avancement : 1- Ok, terminé")),
                '2': ('background:#abf', _("Avancement : 2- En cours")),
                '3': ('background:#ffa', _("Avancement : 3- En attente")),
                '4': ('background:#faa', _("Avancement : 4- Bloqué")),
            },
        }
        exports = {
            'xlsx': {
                'engine': 'xlsx',
                'label': 'Microsoft Excel 2003+',
                'filename': "Demandes en cours.xlsx",
            }
        }

    age_previsionnel = (
        ComputedSmartField,
        {
            'title': _("Age (mois)"),
            'data': AgeDays('date_creation') / 30,
            'depends': [
                'date_creation',
            ],
        },
    )
    programme_dra = (
        ComputedSmartField,
        {
            'title': _("Programme DRA94"),
            'hoz_align': 'center',
            'data': F('programme__anteriorite'),
            'depends': [
                'programme',
            ],
        },
    )
    ligne_dra = (
        ComputedSmartField,
        {
            'title': _("Ligne DRA94"),
            'format': 'integer',
            'hoz_align': 'right',
            'data': F('num_dmd__num_dmd'),
            'depends': [
                'num_dmd',
            ],
        },
    )
    discipline = (
        ComputedSmartField,
        {
            'title': _("Discipline"),
            'hoz_align': 'center',
            'data': F('programme__discipline__nom'),
            'depends': [
                'programme',
            ],
        },
    )
    # Utilisée pour filtrer les demandes de travaux
    discipline_dmd = (
        ComputedSmartField,
        {
            'title': _("Discipline Demande"),
            'hoz_align': 'center',
            'data': F('num_dmd__discipline_dmd'),
            'hidden': True,
        },
    )
    domaine = (
        ComputedSmartField,
        {
            'title': _("Domaine"),
            'hoz_align': 'left',
            'data': F('num_dmd__domaine__code'),
            'depends': [
                'num_dmd',
            ],
        },
    )
    code_uf = (
        ComputedSmartField,
        {
            'title': _("Code UF"),
            'hoz_align': 'center',
            'data': F('uf__code'),
            'depends': [
                'num_dmd',
            ],
        },
    )
    nom_uf = (
        ComputedSmartField,
        {
            'title': _("UF"),
            'data': F('uf__nom'),
            'depends': [
                'num_dmd',
            ],
        },
    )
    nom_pole = (
        ComputedSmartField,
        {
            'title': _("Pôle"),
            'data': F('uf__pole__nom'),
            'depends': [
                'num_dmd',
            ],
        },
    )
    demande_code = (
        ComputedSmartField,
        {
            'title': 'N°',
            'data': F('num_dmd__code'),
            'footer_data': 'count',
        },
    )
    dmd_quantite = (
        ComputedSmartField,
        {
            'title': 'Qté',
            'format': 'integer',
            'data': Case(
                When(
                    num_dmd__quantite_validee__isnull=False,
                    then=F('num_dmd__quantite_validee'),
                ),
                default=F('num_dmd__quantite'),
            ),
            'depends': [
                'num_dmd',
            ],
        },
    )
    dmd_libelle = (
        ComputedSmartField,
        {
            'title': 'Libellé demande',
            'data': F('num_dmd__libelle'),
            'depends': [
                'num_dmd',
            ],
        },
    )
    commentaire_arbitre = (
        ComputedSmartField,
        {
            'title': _("Commentaire arbitre"),
            'data': F('num_dmd__commentaire_definitif_commission'),
            'depends': [
                'num_dmd',
            ],
        },
    )
    ordered_amount = (
        ComputedSmartField,
        {
            'title': _("Montant commandé"),
            'hidden': True,
            'verbose_name': _("Meilleure estimation possible du montant commandé sur cette ligne"),
            'data': Coalesce(F('montant_commande'), F('montant_liquide'), F('montant_engage'), Decimal(0.0)),
            'depends': ['budget', 'solder_ligne', 'montant_commande', 'montant_engage', 'montant_liquide'],
        },
    )
    best_amount = (
        ComputedSmartField,
        {
            'title': _("Meilleure estimation"),
            'verbose_name': _("Meilleure estimation possible de la consommation de crédits du programme"),
            'data': Case(
                When(
                    solder_ligne=False,
                    then=Greatest(F('budget'), F('ordered_amount')),
                ),
                default=F('ordered_amount'),
            ),
            'depends': ['budget', 'solder_ligne', 'montant_commande', 'montant_engage', 'montant_liquide'],
        },
    )
    amount_conditional = (
        ConditionnalSmartField,
        {
            'title': 'Montant commandé',
            'help_text': _(
                "Montant effectivement commandé sur la ligne du programme. Calculée automatiquement ou forcée manuellement."
            ),
            "format": "conditional_money",
            "decimal_symbol": ",",
            "thousands_separator": " ",
            "currency_symbol": " €",
            "symbol_is_after": True,
            "precision": 0,
            "max_width": 120,
            'fields': (
                'montant_commande',
                'ordered_amount',
            ),
        },
    )

    roles = (
        ComputedSmartField,
        {
            'special': 'roles',
            'title': _("Rôles"),
            'hidden': True,
            'data': class_roles_expression(
                Previsionnel,
                owner_field='expert',
                uf_field='uf',
                programme_field='programme',
                campagne_field='programme__calendrier',
                domaine_field='num_dmd__domaine',
            ),
            'depends': ['expert', 'programme', 'uf', 'num_dmd'],
        },
    )


class PrevisionnelSmartView21(PrevisionnelSmartView):
    class Meta:
        columns__add = (
            'age_previsionnel',
            'nombre_commandes',
            'nombre_lignes_commandes',
            'montant_engage',
            'montant_liquide',
            'nombre_equipements',
            'valeur_inventaire',
        )
        selectable_columns__add = (
            'age_previsionnel',
            'nombre_commandes',
            'nombre_lignes_commandes',
            'montant_engage',
            'montant_liquide',
            'nombre_equipements',
            'valeur_inventaire',
        )

        user_filters__update = {
            'domaine': {
                'type': 'select',
                'choices': filter_choices_from_column_values(
                    Previsionnel,
                    'num_dmd__domaine',
                    label_expr=Concat(
                        F('num_dmd__domaine__code'),
                        Value(' - '),
                        F('num_dmd__domaine__nom'),
                    ),
                    order_by='num_dmd__domaine__code',
                ),
            },
            'suivi_contains': {
                'type': 'contains',
                'fieldnames': [
                    'commentaire_arbitre',
                    'commentaire',
                    'commentaire_public',
                    'demande_code',
                    'dmd_libelle',
                    'uf__code',
                    'uf__nom',
                    'ligne_dra',
                    'suivi_achat',
                    'suivi_appro',
                    'suivi_autorisation',
                    'suivi_besoin',
                    'suivi_etude',
                    'suivi_execution',
                    'suivi_mes',
                    'suivi_offre',
                    'suivi_preparation',
                    'suivi_reception',
                ],
                'label': _('Suivi contient'),
            },
        }

        views = 'table'


class PrevisionnelUtilisateursSmartView(PrevisionnelSmartView):
    class Meta:
        columns = (
            'num_dmd_pk',
            'demande_code',
            'discipline_dmd',
            'code_uf',
            'nom_uf',
            'nom_pole',
            'dmd_quantite',
            'dmd_libelle',
            'budget',
            'expert',
            'suivi_besoin',
            'suivi_achat',
            'suivi_offre',
            'suivi_appro',
            'suivi_mes',
            'commentaire_public',
            'date_estimative_mes',
            'roles',
            'tools',
        )
        selectable_columns = (
            # 'num_dmd_pk',
            'code_uf',
            'nom_uf',
            'nom_pole',
            'dmd_quantite',
            'dmd_libelle',
            'budget',
            'expert',
            'suivi_besoin',
            'suivi_achat',
            'suivi_offre',
            'suivi_appro',
            'suivi_mes',
            'commentaire_public',
            'date_estimative_mes',
        )
        settings = {
            'commentaire_public': {
                'title': _("Commentaire"),
                'help_text': _("Commentaire du chargé d'opération"),
            },
            'suivi_besoin': {
                'help_text': _(
                    "Etape au cours de laquelle le chargé d'opération recueille auprès des utilisateurs les précisions "
                    "nécessaires pour permettre la rédaction d'une procédure de marché et/ou d'établir le devis "
                    "auprès du fournisseur."
                ),
                'formatter': "'suivi_couleur'",
            },
            'suivi_achat': {
                'help_text': _(
                    "Etape nécessaire pour disposer d'un marché public. Il peut s'agir d'un marché disponible"
                    " en centrale d'achat (UGAP, UniHA...) ou d'une procédure locale, au niveau du GHT."
                ),
                'formatter': "'suivi_couleur'",
            },
            'suivi_offre': {
                'help_text': _("Etape au cours de laquelle on récupère l'offre formelle du fournisseur (devis...)"),
                'formatter': "'suivi_couleur'",
            },
            'suivi_appro': {
                'help_text': _(
                    "Commande effective du matériel, dans le respect des procédures internes. L'étape se "
                    "termine avec l'envoi du bon de commande au fournisseur."
                ),
                'formatter': "'suivi_commande_couleur'",
            },
            'suivi_mes': {
                'help_text': _("Etape finale, qui s'achève avec la livraison et la mise en service du matériel."),
                'formatter': "'suivi_couleur'",
            },
            'date_estimative_mes': {
                'title': "Estimation date Mise en Service",
                'datetime_format': "%Q 'trim.' %Y",
            },
        }
        current_row_manager = None
        row_styler = None
        exports = ()
        help_text = _(
            "Vous trouverez dans ce tableau toutes les demandes qui ont été validées"
            " et pour lesquelles les équipements sont en cours d'acquisition "
            "(et jusqu'à trois mois après la mise en service). "
            "Pour chaque demande, vous pouvez voir qui est en charge de l'acquisition, "
            "l'état d'avancement des principales étapes"
            " et la date prévisionnelle de mise en service. <b>Attention, les quantités et "
            "les enveloppes validées par la commission ou l'arbitre"
            " peuvent être différentes de celles des demandes initiales.</b>"
        )

        # Filtre de base : Uniquement le prévisionnel associé aux demandes sur les UF pour lesquelles je peux faire une demande...
        def base_filter(self, view_params: dict):  # NOQA
            # Liste des rôles pour lesquels je peux faire une demande sur une UF (objet qui devrait être partagé sur l'ensemble
            #  de l'application _dem_
            tmp_scope = roles_demandes_possibles(view_params['user'])
            return (
                (
                    Q(num_dmd__uf__in=tmp_scope.values('uf'))
                    | Q(num_dmd__uf__service__in=tmp_scope.values('service'))
                    | Q(num_dmd__uf__centre_responsabilite__in=tmp_scope.values('centre_responsabilite'))
                    | Q(num_dmd__uf__pole__in=tmp_scope.values('pole'))
                    | Q(num_dmd__uf__site__in=tmp_scope.values('site'))
                    | Q(num_dmd__uf__etablissement__in=tmp_scope.values('etablissement'))
                )
                & (
                    # Hack pour ne pas voir les demandes de travaux
                    Q(discipline_dmd__isnull=True)
                    | ~Q(discipline_dmd=Discipline.objects.values_list('pk', flat=True).filter(code='TX')[0])
                    # Uniquement les demandes qui ne sont pas terminées depuis 'longtemps'
                    & (
                        ~(Q(suivi_mes__startswith='1-') & Q(suivi_mes__startswith='0-'))
                        | Q(solder_ligne=False)
                        | Q(date_estimative_mes__gte=now() - DRACHAR_DELAI_DEMANDE_TERMINEE)
                    )
                ),
            )

    num_dmd_pk = (
        ComputedSmartField,
        {
            'title': 'Numéro',
            'data': F('num_dmd__pk'),
            'hidden': True,
        },
    )
    tools = (
        ToolsSmartField,
        {
            'title': _("Actions"),
            'tools': [
                {
                    'tool': 'open',
                    'url_name': 'dem:request-view',
                    'url_arg_fieldname': 'num_dmd_pk',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir la demande"),
                },
            ],
        },
    )


class PrevTvxSmartView(SmartView):
    class Media(SmartView.Media):
        js = SmartView.Media.js + ('drachar/js/suivi-format.js',)

    class Meta:
        model = Previsionnel
        base_filter = Q(programme__discipline__code='TX')
        permissions = {
            # La creation des fiches prévivionnelles se fait exclusivement par le script dédié
            #  et jamais par un utilisateur
            'create': (),
            'write': {
                # L'état est la fermeture de la ligne du prévisionnel, donc False signifie qu'on peut modifier...
                False: {
                    'OWN': {
                        'commentaire': True,
                        'commentaire_public': True,
                        'date_debut': True,
                        'suivi_besoin': True,
                        'suivi_etude': True,
                        'suivi_autorisation': True,
                        'suivi_preparation': True,
                        'suivi_execution': True,
                        'suivi_reception': True,
                        'suivi_mes': True,
                        'montant_estime': True,
                        'montant_commande': True,
                        'solder_ligne': True,
                        'date_estimative_mes': True,
                    },
                    'DIS': {
                        'programme': True,
                        'solder_ligne': True,
                        'expert': True,
                        # Temporaire ? ou définitif ??
                        'commentaire': True,
                        'commentaire_public': True,
                        'date_debut': True,
                        'suivi_besoin': True,
                        'suivi_etude': True,
                        'suivi_autorisation': True,
                        'suivi_preparation': True,
                        'suivi_execution': True,
                        'suivi_reception': True,
                        'suivi_mes': True,
                        'montant_estime': True,
                        'montant_commande': True,
                        'date_estimative_mes': True,
                    },
                    'RESPD': {
                        'programme': True,
                        'solder_ligne': True,
                        'expert': True,
                        # Temporaire ? ou définitif ??
                        'commentaire': True,
                        'commentaire_public': True,
                        'date_debut': True,
                        'suivi_besoin': True,
                        'suivi_etude': True,
                        'suivi_autorisation': True,
                        'suivi_preparation': True,
                        'suivi_execution': True,
                        'suivi_reception': True,
                        'suivi_mes': True,
                        'montant_estime': True,
                        'montant_commande': True,
                        'date_estimative_mes': True,
                    },
                    'EXP': {
                        'commentaire': True,
                        'commentaire_public': True,
                        # 'solder_ligne': True,
                        'date_debut': True,
                        'suivi_besoin': True,
                        'suivi_etude': True,
                        'suivi_autorisation': True,
                        'suivi_preparation': True,
                        'suivi_execution': True,
                        'suivi_reception': True,
                        'suivi_mes': True,
                        'montant_estime': True,
                        'montant_commande': True,
                        'date_estimative_mes': True,
                    },
                },
                True: {
                    'DIS': {
                        'solder_ligne': True,
                    },
                    'RESPD': {
                        'solder_ligne': True,
                    },
                    'OWN': {
                        'suivi_mes': True,
                        'solder_ligne': True,  # Le propriétaire peut "désolder" un prévisionnel
                        'date_estimative_mes': True,
                        'commentaire': True,
                        'commentaire_public': True,
                    },
                },
            },
        }
        current_row_manager = True
        columns = (
            'num',
            'num_dmd',
            'demande_code',
            'discipline',
            'discipline_dmd',
            'programme',
            'code_uf',
            'nom_uf',
            'nom_pole',
            'dmd_quantite',
            'dmd_libelle',
            'domaine',
            'budget',
            'commentaire_arbitre',
            'expert',
            # 'date_debut',
            # 'programme_dra',
            # 'ligne_dra',
            'best_amount',
            'suivi_besoin',
            'suivi_etude',
            'suivi_autorisation',
            'suivi_preparation',
            'suivi_execution',
            'suivi_reception',
            'suivi_mes',
            'montant_commande',
            'solder_ligne',
            'commentaire_public',
            'date_estimative_mes',
            'commentaire',
            # 'interface',
            'roles',
        )
        selectable_columns = (
            # 'num',
            'discipline',
            'programme',
            'code_uf',
            'nom_uf',
            'nom_pole',
            'dmd_quantite',
            'dmd_libelle',
            'domaine',
            'budget',
            'commentaire_arbitre',
            'expert',
            # 'date_debut',
            # 'programme_dra',
            # 'ligne_dra',
            'best_amount',
            'suivi_besoin',
            'suivi_etude',
            'suivi_autorisation',
            'suivi_preparation',
            'suivi_execution',
            'suivi_reception',
            'suivi_mes',
            'solder_ligne',
            'montant_commande',
            'commentaire_public',
            'date_estimative_mes',
            'commentaire',
            # 'interface',
        )
        settings = {
            'num': {
                'hidden': True,
            },
            'num_dmd': {
                'hidden': True,
            },
            'budget': {
                'title': _("Enveloppe"),
                'format': 'money',
                'decimal_symbol': ",",
                'thousands_separator': " ",
                'currency_symbol': " €",
                'symbol_is_after': True,
                'precision': 0,
                'max_width': 95,
                'footer_data': "sum",
            },
            'best_amount': {
                'title': _("Meilleur montant estimé"),
                'format': 'money',
                'decimal_symbol': ",",
                'thousands_separator': " ",
                'currency_symbol': " €",
                'symbol_is_after': True,
                'precision': 0,
                'max_width': 95,
                'footer_data': "sum",
            },
            'montant_commande': {
                'title': _("Montant commandé"),
                'format': 'money',
                'decimal_symbol': ",",
                'thousands_separator': " ",
                'currency_symbol': " €",
                'symbol_is_after': True,
                'precision': 0,
                'max_width': 95,
                'footer_data': "sum",
            },
            'expert': {
                'title': _("Chargé opération"),
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
            'suivi_besoin': {
                'title': _("Programme"),
                'formatter': "'suivi'",
            },
            'suivi_etude': {
                'formatter': "'suivi'",
            },
            'suivi_autorisation': {
                'formatter': "'suivi'",
            },
            'suivi_preparation': {
                'formatter': "'suivi'",
            },
            'suivi_execution': {
                'formatter': "'suivi'",
            },
            'suivi_reception': {
                'formatter': "'suivi'",
            },
            'suivi_achat': {
                'formatter': "'suivi'",
            },
            'suivi_offre': {
                'formatter': "'suivi'",
            },
            'suivi_appro': {
                'formatter': "'suivi_commande'",
            },
            'suivi_mes': {
                'formatter': "'suivi'",
            },
            'date_debut': {
                'editor': 'dateEditor',
                'datetime_format': '%d/%m/%Y',
            },
            'date_estimative_mes': {
                'editor': 'dateEditor',
                'datetime_format': '%m/%Y',
            },
            'solder_ligne': {
                'title': _("Soldé"),
                'special': 'state',
                'hidden': False,
            },
            # 'interface': {
            #     'format': 'html',
            # },
        }
        user_filters = {
            'expert': {
                'type': 'select',
                'choices': filter_choices_from_column_values(
                    Previsionnel,
                    'expert',
                    label_expr=Concat(F('expert__first_name'), Value(' '), F('expert__last_name')),
                    order_by='expert__last_name',
                ),
            },
            'discipline': {
                'type': 'select',
                'choices': filter_choices_from_column_values(Previsionnel, 'programme__discipline__nom'),
            },
            'programme': {
                'label': _("Programme"),
                'type': 'select',
                'choices': filter_choices_from_column_values(
                    Previsionnel,
                    'programme',
                    label_expr=Concat(F('programme__code'), Value(' - '), F('programme__nom')),
                    order_by='programme__code',
                ),
            },
            'nom_pole': {
                'type': 'select',
                'choices': filter_choices_from_column_values(Previsionnel, 'num_dmd__uf__pole__nom'),
            },
            'nom_uf': {
                'type': 'select',
                'choices': filter_choices_from_column_values(
                    Previsionnel,
                    'num_dmd__uf',
                    label_expr=Concat(F('num_dmd__uf__code'), Value(' - '), F('num_dmd__uf__nom')),
                ),
            },
            'dmd_libelle': {'type': 'contains'},
            'solder_ligne': {'type': 'select'},
        }
        row_styler = {
            'fieldname': 'solder_ligne',
            'styles': {
                False: ("background:#fff", "Demande à faire ou en cours"),
                True: ("background:#ddd", "Demande Soldée"),
                '0': ('background:#aaa', _("Avancement : 0- Sans objet")),
                '1': ('background:#afa', _("Avancement : 1- Ok, terminé")),
                '2': ('background:#abf', _("Avancement : 2- En cours")),
                '3': ('background:#ffa', _("Avancement : 3- En attente")),
                '4': ('background:#faa', _("Avancement : 4- Bloqué")),
            },
        }
        exports = {
            'xlsx': {
                'engine': 'xlsx',
                'label': 'Microsoft Excel 2003+',
                'filename': "Demandes en cours.xlsx",
            }
        }

    programme_dra = (
        ComputedSmartField,
        {
            'title': _("Programme DRA94"),
            'hoz_align': 'center',
            'data': F('programme__anteriorite'),
            'depends': [
                'programme',
            ],
        },
    )
    ligne_dra = (
        ComputedSmartField,
        {
            'title': _("Ligne DRA94"),
            'format': 'integer',
            'hoz_align': 'right',
            'data': F('num_dmd__num_dmd'),
            'depends': [
                'num_dmd',
            ],
        },
    )
    discipline = (
        ComputedSmartField,
        {
            'title': _("Discipline"),
            'hoz_align': 'center',
            'data': F('programme__discipline__nom'),
            'depends': [
                'programme',
            ],
        },
    )
    # Utilisée pour filtrer les demandes de travaux
    discipline_dmd = (
        ComputedSmartField,
        {
            'title': _("Discipline Demande"),
            'hoz_align': 'center',
            'data': F('num_dmd__discipline_dmd'),
            'hidden': True,
        },
    )
    domaine = (
        ComputedSmartField,
        {
            'title': _("Domaine"),
            'hoz_align': 'left',
            'data': F('num_dmd__domaine__code'),
            'depends': [
                'num_dmd',
            ],
        },
    )
    code_uf = (
        ComputedSmartField,
        {
            'title': _("Code UF"),
            'hoz_align': 'center',
            'data': F('num_dmd__uf__code'),
            'depends': [
                'num_dmd',
            ],
        },
    )
    nom_uf = (
        ComputedSmartField,
        {
            'title': _("UF"),
            'data': F('num_dmd__uf__nom'),
            'depends': [
                'num_dmd',
            ],
        },
    )
    nom_pole = (
        ComputedSmartField,
        {
            'title': _("Pôle"),
            'data': F('num_dmd__uf__pole__nom'),
            'depends': [
                'num_dmd',
            ],
        },
    )
    demande_code = (
        ComputedSmartField,
        {
            'title': 'N°',
            'data': F('num_dmd__code'),
            'footer_data': 'count',
        },
    )
    dmd_quantite = (
        ComputedSmartField,
        {
            'title': 'Qté',
            'format': 'integer',
            'data': Case(
                When(
                    num_dmd__quantite_validee__isnull=False,
                    then=F('num_dmd__quantite_validee'),
                ),
                default=F('num_dmd__quantite'),
            ),
            'depends': [
                'num_dmd',
            ],
        },
    )
    dmd_libelle = (
        ComputedSmartField,
        {
            'title': 'Libellé demande',
            'data': F('num_dmd__libelle'),
            'depends': [
                'num_dmd',
            ],
        },
    )
    commentaire_arbitre = (
        ComputedSmartField,
        {
            'title': _("Commentaire arbitre"),
            'data': F('num_dmd__commentaire_definitif_commission'),
            'depends': [
                'num_dmd',
            ],
        },
    )
    best_amount = (
        ComputedSmartField,
        {
            'title': _("Meilleure estimation"),
            'verbose_name': _("Meilleure estimation possible de la consommation de crédits du programme"),
            'data': Case(
                When(
                    solder_ligne=False,
                    then=Greatest(
                        F('budget'), Coalesce(F('montant_commande'), F('montant_liquide'), F('montant_engage'), Decimal(0.0))
                    ),
                ),
                default=Coalesce(F('montant_commande'), F('montant_liquide'), F('montant_engage'), Decimal(0.0)),
            ),
            'depends': ['budget', 'solder_ligne', 'montant_commande', 'montant_engage', 'montant_liquide'],
        },
    )
    roles = (
        ComputedSmartField,
        {
            'special': 'roles',
            'title': _("Rôles"),
            'hidden': True,
            'data': class_roles_expression(
                Previsionnel,
                owner_field='expert',
                uf_field='num_dmd__uf',
                programme_field='programme',
                campagne_field='programme__calendrier',
                domaine_field='num_dmd__domaine',
            ),
            'depends': ['expert', 'programme'],
        },
    )


class DraSmartView(SmartView):
    class Media(SmartView.Media):
        js = SmartView.Media.js + ('drachar/js/suivi-format.js',)

    class Meta:
        model = Dra
        current_row_manager = True
        columns = (
            'num_dra',
            'intitule',
            'fournisseur',
            'contact_fournisseur',
            'num_devis',
            'date_devis',
            'num_marche',
            'expert_metier',
            'num_bon_commande',
            'date_commande',
            'num_dossier',
            # 'documents',
            'contact_livraison',
        )
        selectable_columns = (
            'num_dra',
            'intitule',
            'fournisseur',
            'contact_fournisseur',
            'num_devis',
            'date_devis',
            'num_marche',
            'expert_metier',
            'num_bon_commande',
            'date_commande',
            'num_dossier',
            # 'documents',
            'contact_livraison',
        )
        user_filters = {
            'expert_metier': {'type': 'select'},
            'num_dra': {
                'type': 'contains',
            },
            'fournisseur': {
                'type': 'select',
                'choices': filter_choices_from_column_values(Fournisseur, 'nom'),
                # filter_choices_from_column_values(Fournisseur, 'code_four'),
            },
            'intitule': {
                'type': 'contains',
            },
        }
        exports = {
            'xlsx': {
                'engine': 'xlsx',
                'label': 'Microsoft Excel 2003+',
                'filename': "Demandes en cours.xlsx",
            }
        }

class ContactLivraisonSmartView(SmartView):
    class Meta:
        model = ContactLivraison
        permissions = {
            'create': ('ADM', 'MAN', 'EXP'),
            'delete': ('ADM', 'MAN', 'EXP'),
            'write': {
                None: {
                    'ADM': {
                        'code': False,
                        'nom': True,
                        'prenom': True,
                        'coordonnees': True,
                        'etablissement': True,
                    },
                    'MAN': {
                        'code': False,
                        'nom': True,
                        'prenom': True,
                        'coordonnees': True,
                        'etablissement': True,
                    },
                    'EXP': {
                        'code': False,
                        'nom': True,
                        'prenom': True,
                        'coordonnees': True,
                        'etablissement': True,
                    },
                },
                'EDITABLE': {
                    'ADM': {
                        'code': True,
                        'nom': True,
                        'prenom': True,
                        'coordonnees': True,
                        'etablissement': True,
                    },
                    'MAN': {
                        'code': False,
                        'nom': True,
                        'prenom': True,
                        'coordonnees': True,
                        'etablissement': True,
                    },
                    'EXP': {
                        'code': False,
                        'nom': True,
                        'prenom': True,
                        'coordonnees': True,
                        'etablissement': True,
                    },
                },
            },
        }
        columns = (
            'id',
            'roles',
            'state_code',
            'code',
            'nom',
            'prenom',
            'coordonnees',
            'etablissement',
        )
        user_filters = {
            'contient': {
                'type': 'contains',
                'fields': ['code', 'nom', 'prenom', 'coordonnees'],
            },
            'etablissement': {'type': 'select'},
        }
        menu_left = ({'label': "Ajouter un Contact de livraison", 'url_name': 'drachar:contactlivraison-create'},)
        form_layout = """
        #
            # Contact Livraison
                <code> <etablissement>
                <prenom> <nom>
                <coordonnees>
        """
    roles = (
        ComputedSmartField,
        {
            'hidden': True,
            'special': 'roles',
            'data': class_roles_expression(ContactLivraison),
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
                    'url_name': 'drachar:contactlivraison-update',
                    'url_args': ('${id}',),
                    'tooltip': _("Ouvrir la fiche de contact livraison"),
                },
                {
                    'tool': 'delete',
                    'url_name': 'drachar:contactlivraison-ask-delete',
                    'url_args': ('${id}',),
                    'tooltip': _("Supprimer la fiche de contact livraison"),
                },
            ],
        },
    )
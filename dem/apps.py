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
from decimal import Decimal

from django.apps import AppConfig, apps
from django.db.models import Value, F, Q, Count, CharField, Subquery, OuterRef
from django.db.models.functions import JSONObject, Concat, Coalesce
from django.db.models.aggregates import Sum
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save

from common import config

# Délai pendant lequel les demandes traitées (suivi_mes commence par '1-') sont considérées comme archivées
#  (date_modification du prévionnel antérieur à la date du jour moins ce delai)

DRACHAR_DELAI_DEMANDE_TERMINEE = datetime.timedelta(days=90)


def check_demande_a_dispatcher(name, data):
    # faire un 'import' ici n'est pas très clean, mais c'est le seul moyen car il ne faut pas importer à l'ouverture du
    #  module (car Django n'est pas encore initialisé et on ne peut pas travailler sur les modèles) mais à l'exécution
    #  de la fonction (qui arrive à un moment où Django est initialisé)
    from dem.models import Demande
    from common.user_settings import UserSettings

    alerts = []
    demandes_a_dispatcher = Demande.objects.filter(
        ~Q(discipline_dmd__code='TX')
        & (Q(programme__isnull=True) | Q(expert_metier__isnull=True) | Q(domaine__isnull=True))
        & (Q(gel=False) | Q(gel__isnull=True))
    )
    for demande in demandes_a_dispatcher:
        delay = datetime.timedelta(
            hours=int(UserSettings(demande.calendrier.dispatcher)['notifications.dem.demand-to-dispatch.delay'])
        )
        if now() - demande.date_modification > delay:
            alerts.append(
                {
                    'destinataire': demande.calendrier.dispatcher,
                    'categorie': name,
                    'niveau': data['alert_level'],
                    'donnees': json.dumps({'id': demande.pk, 'dmd_code': demande.code}),
                    'date_activation': now(),
                }
            )
    return alerts, {'categorie': name}


class DemConfig(AppConfig):
    name = 'dem'  # this is the name of the module (not the appname from urls.py)
    verbose_name = _("Gestion des demandes")

    biom_aid = {
        'portal': {
            'permissions': ('EXP', 'ACH', 'DIS', 'ARB', 'ADM'),
            'label': _("Gestion des demandes de matériel"),
            'main-name': _("DEM"),
            'home': 'dem:cockpit',
            'external-menu': ('ugap', 'intranet', 'annuaire', 'asset-web'),
            'main-menu': (
                {
                    'label': _("Cockpit"),
                    'url_name': 'dem:cockpit',
                },
                {
                    'label': _("Nouvelle demande"),
                    'help_text': _("Entrer une nouvelle demande"),
                    'permissions': config.settings.DEM_DEMANDE_CREATION_ROLES,
                    'entries': {
                        'engine': 'campagnes',
                    },
                },
                {
                    'label': _("Répartition"),
                    'permissions': ('DIS',),
                    'entries': {
                        'engine': 'queryset',
                        'model': 'dem.campagne',
                        'filters': lambda params: (
                            Q(dispatcher=params['user'])
                            & (Q(demande__gel=False) | Q(demande__gel__isnull=True))
                            & (
                                Q(demande__programme__isnull=True)
                                | Q(demande__expert_metier__isnull=True)
                                | Q(demande__domaine__isnull=True)
                            )
                        ),
                        'aggregates': lambda params: {'nba': Count('demande__pk')},
                        'agg_filters': Q(nba__gt=0),
                        'sort': ['code'],
                        'mapping': {
                            'label': Concat(
                                F('nom'),
                                Value(' ('),
                                F('nba'),
                                Value(')'),
                                output_field=CharField(),
                            ),
                            'url_name': Value('dem:repartition'),
                            'url_kwargs': JSONObject(campagne_code=F('code')),
                        },
                    },
                },
                {
                    'label': _("Expertise"),
                    'permissions': ('EXP',),
                    'url_name': 'dem:expertise',
                },
                {
                    'label': _("Arbitrage"),
                    'right': True,
                    'permissions': ('ARB',),
                    'entries': {
                        'engine': 'queryset',
                        'model': 'common.programme',
                        'filters': lambda params: (
                            Q(arbitre=params['user']) & (Q(demande__gel=False) | Q(demande__gel__isnull=True))
                        ),
                        'aggregates': lambda params: {'nba': Count('demande__pk')},
                        'agg_filters': Q(nba__gt=0),
                        'sort': ['code'],
                        'mapping': {
                            'label': Concat(
                                F('nom'),
                                Value(' ('),
                                F('nba'),
                                Value(')'),
                                output_field=CharField(),
                            ),
                            'url_name': Value('dem:arbitrage'),
                            'url_kwargs': JSONObject(programme_code=F('code')),
                        },
                    },
                },
                {
                    'label': _("Demandes en cours"),
                    'url_name': 'dem:demandes-en-cours-exp',
                },
                {
                    'label': _("Demandes archivées"),
                    'url_name': 'dem:demandes-archivees-expert',
                },
                {
                    'label': _("Synthèses"),
                    # 'url_name': 'dem:demandes-archivees-expert',
                    'permissions': (
                        'P-ARB',
                        'P-EXP',
                    ),
                    'show-only-if-allowed': True,
                    'entries': [
                        {
                            'label': _("Parc"),
                            'url_name': 'dem:all-assets-view',
                        },
                        {
                            'label': _("Historique validées"),
                            'url_name': 'dem:history-view',
                        },
                        {
                            'label': _("Demandes en cours"),
                            'url_name': 'dem:current-requests-view',
                        },
                        {
                            'label': _("Aides à l'arbitrage"),
                            'url_name': 'dem:arbitration-help-view',
                        },
                        {
                            'label': _("Synthèse arbitrage : programme"),
                            'url_name': 'dem:vue-filtre-synthese',
                        },
                    ],
                },
            ),
        },
        'user-settings-categories': {
            'dem_eq': {
                'label': _("Gestion des demandes d'équipement"),
            },
            'dem_eq.autovalidation': {
                'label': _("Validation des demandes"),
            },
        },
        'user-settings': {
            'dem_eq.autovalidation.auto_amount': {
                'roles': ('CHP', 'DIR'),
                'label': _("Montant sous lequel la validation est automatique"),
                'format': 'money',
            },
            'dem_eq.autovalidation.auto_amount_csp': {
                'roles': ('CHP',),
                'label': _("Montant sous lequel l'avis favorable du Cadre Supérieur du Pôle vaut validation"),
                'format': 'money',
            },
        },
    }
    biom_aid_roles = (
        'CAD',
        'ACH',
        'EXP',
        'TECH',
    )
    biom_aid_alert_categories = {
        'demand-to-dispatch': {
            'roles': {'DIS'},
            'label': _("Demande à répartir"),
            'help_text': _("Notification adressée au dispatcheur lorsqu'une nouvelle demande est saisie"),
            'hint': _(
                """Pour mettre fin à l'alerte il faut
                 préciser le programme, le nom de l'expert métier
             et le domaine de la demande."""
            ),
            'user_settings': {
                'delay': {
                    'label': _("Délai avant création d'une alerte"),
                    'roles': ('DIS',),
                    'help_text': _(
                        "Si une nouvelle demande est créée dans une campagne pour laquelle vous "
                        " êtes répartiteur (dispatcheur), c'est le délai avant la"
                        " création de l'alerte correspondante."
                    ),
                    'format': 'choices',
                    'choices': {
                        0: 'Pas de délai, immédiat',
                        24: '1 journée',
                        48: '2 jours',
                        168: '1 semaine',
                    },
                    'default': 24,
                },
            },
            'message': _("<span>La demande {dmd_code} doit être 'dispatchée' " "</span>"),
            # 'link_url_name': 'dem:repartition',
            'alert_level': 1,
            'groups': {'TODO', 'TEST'},
            'check_func': check_demande_a_dispatcher,  # La fonction qui fait la détection d'alerte
        },
        'campaign-redirect': {
            'label': _("Changement de campagne de recensement"),
            'roles': ('CAD',),  # Unused ?
            'help_text': _(
                "Cette alerte se déclenche pour informer un utilisateur que sa demande a été transférée "
                "à une autre campagne de recensement. C'est en général dû à une erreur "
                "lors de la demande initiale ou à des circuits très spécifiques pour certaines demandes."
            ),
            'hint': _("Cette alerte s'inactivera automatiquement dans quelques jours"),
            'user_settings': {},
            'message': _(
                "<span>La demande {dmd_code} a été transférée de la campagne"
                " « {src_campaign} » vers la campagne « {dst_campaign} » "
                ": {dispatcher_note}<br>{campaign_message}</span>"
            ),
            'alert_level': 1,
            'groups': {
                'TEST',
            },
            'check_func': None,
            'timeout': 3600 * 7,  # timeout = 10s
        },
    }

    def ready(self) -> None:
        from dem.models import Demande
        from dem.smart_views import DemandeEqptSmartView

        # # This signal handler is called every time a 'demande' instance is saved
        # # its purpose is to update, if needed, the 'programme'
        # def dem_saved_hook(sender, **kwargs):
        #     print(f"Saved hook {sender=} {kwargs=}")

        #     if sender.programme is not None:
        #         if (
        #             kwargs['update_fields'] is None
        #             or 'programme' in kwargs['update_fields']
        #             or 'flag' in kwargs['update_fields']
        #             or 'prix_unitaire_expert' in kwargs['update_fields']
        #         ):
        #             print(f"Saved hook recompute program {sender.programme=} {kwargs=}")

        common_config = apps.get_app_config('common')
        # Calcul de l'expression qui calcule la consommation de l'enveloppe UNIQUEMENT pour les demandes
        # Toutes les demandes validées de façon définitives mais sans previsionnel associé (pas encore dans le plan)
        dem_qs = Demande.objects.filter(
            programme=OuterRef('pk'), gel=True, arbitrage_commission__valeur=True, previsionnel__isnull=True
        )
        # Ajoutons les champs calculés utiles (récupération depuis la SmartView)
        for anno in ['montant_qte_validee', 'enveloppe_finale']:
            dem_qs = dem_qs.annotate(**{anno: getattr(DemandeEqptSmartView, anno).expression})
        # On déclare l'expression finale qui calcule la consommation de l'enveloppe du programme, pour le
        # modèle des demandes
        common_config.register_program_consumer(
            Coalesce(
                Subquery(dem_qs.values('programme').annotate(sum1=Sum('enveloppe_finale')).values('sum1')), Value(Decimal(0.0))
            )
        )

        post_save.connect(
            common_config.program_update,
            sender=apps.get_model('dem.demande'),
            weak=False,
            dispatch_uid='dem_post_save',
        )

        return super().ready()

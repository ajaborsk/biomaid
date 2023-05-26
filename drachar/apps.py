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
from datetime import timedelta
from decimal import Decimal

from django.apps import AppConfig

# from django.urls import reverse_lazy
from django.db.models import Count, F, IntegerField, Sum, Value, OuterRef, Subquery
from django.db.models.functions import Cast, Concat, Coalesce
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save


def check_previsionnel_sans_date(name, data):
    # faire un 'import' ici n'est pas très clean, mais c'est le seul moyen car il ne faut pas importer à l'ouverture du
    #  module (car Django n'est pas encore initialisé et on ne peut pas travailler sur les modèles) mais à l'exécution
    #  de la fonction (qui arrive à un moment où Django est initialisé)
    from drachar.models import Previsionnel
    from common.user_settings import UserSettings

    alerts = []
    previsionnels_sans_date = Previsionnel.objects.filter(date_estimative_mes__isnull=True)
    for previsionnel in previsionnels_sans_date:
        try:
            delay_str = UserSettings(previsionnel.expert)['notifications.drachar.previsionnel-sans-date.delay']
            delay = timedelta(hours=int(delay_str))
        except ValueError:
            delay = timedelta(hours=0)
        if now() - previsionnel.date_modification > delay:
            alerts.append(
                {
                    'destinataire': previsionnel.expert,
                    'categorie': name,
                    'niveau': data['alert_level'],
                    'donnees': json.dumps({'id': previsionnel.pk, 'dmd_code': previsionnel.num_dmd.code}),
                    'date_activation': timezone.now(),
                }
            )
    return alerts, {'categorie': name}


class DracharConfig(AppConfig):
    # nom de l'application
    name = 'drachar'

    # Nom complet de l'application (affichée notamment dans les menus)
    verbose_name = _("Demandes Réalisation ACHAts (Reloaded)")
    # C'est une application biom_aid (avec son portail)
    biom_aid = {
        'portal': {
            'main-name': _("DRACHAR"),
            'permissions': ('ACH', 'EXP', 'DIS', 'ADM'),
            'label': _("Demandes Réalisation ACHAts (Reloaded)"),
            'home': 'drachar:home',
            'main-menu': (
                {'label': 'Accueil', 'url_name': 'drachar:home'},
                {'label': 'Suivi', 'url_name': 'drachar:previsionnel'},
                # {'label': 'Cockpit', 'url_name': 'drachar:cockpit'},
            ),
        },
        'user-settings-categories': {
            'notifications.drachar': {
                'label': _("Gestion des commandes"),
                'help_text': _("Section dédiée au module DRAchaR"),
            },
        },
    }
    # Seuls les utilisateurs avec ces rôles ont accès à l'application
    biom_aid_roles = (
        'ACH',
        'EXP',
        'DIS',
        'ADM',
    )

    # Alertes liées à cette application
    biom_aid_alert_categories = {
        'previsionnel-sans-date': {
            'alert_level': 1,
            'user_settings': {
                'delay': {
                    'label': _("Délai avant création d'une alerte"),
                    'roles': ('EXP',),
                    'help_text': _(
                        "Si une ligne de prévisionnel sur laquelle vous êtes chargé(e) d'opération"
                        " n'a pas de date prévisionnelle de mise en service, c'est le délai avant la"
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
                }
            },
            'check_func': check_previsionnel_sans_date,  # La fonction qui fait la détection d'alerte
            'label': _("Ligne de prévisionnel sans date estimée de mise en service"),
            'message': _(
                "<span>La <a href=\"{link_url}#{id}\">ligne de prévisionnel liée à la demande"
                " {dmd_code}</a> n'a pas de date estimée de mise en service</span>"
            ),
            'help_text': _(
                """Cette alerte est créée lorsqu'une ligne de prévisionnel n'a pas de date prévisionnelle de fin,
            c'est à dire de mise en service de l'équipement. Cette date est utilisée à la fois pour informer l'utilisateur et pour
            calculer les prévisions de décaissement. Elle n'a pas besoin d'être très précise (plus ou moins quelques semaines) mais
            elle doit être corrigée en cas de gros décalage."""
            ),
            'hint': _(
                """La seule façon de mettre fin à l'alerte est de préciser une date dans le champs correspondant
            (sur la page "Suivi du plan"). S'il s'agit d'un dossier déjà traité, le plus simple consiste à mettre
            la date de mise en service effective ou, à défaut, une date approximative
            (plus cette date est ancienne, moins elle a besoin d'être précise)."""
            ),
            'link_url_name': 'drachar:previsionnel',
            # TODO: Un moyen d'augmenter le niveau avec l'âge de l'alerte ?
            # TODO: Un champ pour indiquer si l'alerte peut être manuellement neutralisée (avec un commentaire) ?
            # TODO: Un moyen (hook) pour traiter en temps réel une correction (sans devoir tout recalculer) ?
        }
        # TODO: Une alerte lorsqu'un prévisionnel "arrive" chez un chargé d'opération
    }

    def ready(self):
        from django.apps import apps
        from drachar.models import Previsionnel
        from drachar.smart_views import PrevisionnelSmartView

        common_config = apps.get_app_config('common')
        # Calcul de l'expression qui calcule la consommation de l'enveloppe UNIQUEMENT pour le prévisionnel (plan)
        # Toutes les lignes du plan associées à de ce programme
        dem_qs = Previsionnel.objects.filter(programme=OuterRef('pk'))
        # Ajoutons les champs calculés utiles (récupération depuis la SmartView)
        for anno in ['ordered_amount', 'best_amount']:
            dem_qs = dem_qs.annotate(**{anno: getattr(PrevisionnelSmartView, anno).expression})
        # On déclare l'expression finale qui calcule la consommation de l'enveloppe du programme, pour le
        # modèle des demandes
        common_config.register_program_consumer(
            Coalesce(Subquery(dem_qs.values('programme').annotate(sum1=Sum('best_amount')).values('sum1')), Value(Decimal(0.0)))
        )

        post_save.connect(
            common_config.program_update,
            sender=apps.get_model('drachar.previsionnel'),
            weak=False,
            dispatch_uid='previsionnel_post_save',
        )

        def previsionnel_par_expert(discipline):
            return (
                Previsionnel.objects.order_by()
                .filter(solder_ligne=False, programme__discipline__code=discipline)
                .annotate(nom_expert=Concat(F('expert__first_name'), Value(' '), F('expert__last_name')))
                .values('expert', 'nom_expert')
                .annotate(nombre=Count('pk'))
                .values('expert', 'nom_expert', 'nombre')
            )

        def montant_previsionnel_par_expert(discipline):
            return (
                Previsionnel.objects.order_by()
                .filter(solder_ligne=False, programme__discipline__code=discipline)
                .annotate(nom_expert=Concat(F('expert__first_name'), Value(' '), F('expert__last_name')))
                .values('expert', 'nom_expert')
                .annotate(montant_total=Cast(Sum('budget'), output_field=IntegerField()))
                .values('expert', 'nom_expert', 'montant_total')
            )

        apps.get_app_config('analytics').register_data_processor('previsionnel_par_expert', previsionnel_par_expert)
        apps.get_app_config('analytics').register_data_processor('montant_previsionnel_par_expert', montant_previsionnel_par_expert)

    # def server_ready(self):
    #     from analytics.data import set_datasource

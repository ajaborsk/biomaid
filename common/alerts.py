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
from logging import warning
from typing import Optional

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import OutputWrapper
from django.db.models import Count, Q
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext as _

from common.models import Alert
from common import config
from common.user_settings import UserSettings
from common.utils import HTMLFilter


class AlertsManager:
    """Classe utilisée pour gérer les notification au système"""

    def __init__(self):
        self.alert_categories = {}

        # Parcourir toutes les applications...
        for app_name, app in apps.app_configs.items():
            # print(app_name, config['ENABLED_ALERTS'], app_name in config['ENABLED_ALERTS'])
            if hasattr(app, 'biom_aid_alert_categories'):
                # Ajouter les classes de notification à la liste globale
                for name, nt in app.biom_aid_alert_categories.items():
                    if (
                        app_name in config['ENABLED_ALERTS']
                        and name in config['ENABLED_ALERTS'][app_name]
                        and config['ENABLED_ALERTS'][app_name][name] is True
                    ):
                        self.alert_categories[app_name + '.' + name] = nt

    def alert_record(self, categorie, destinataire, donnees, date_activation, niveau, **kwargs):
        # récupère la classe de notification (dictionnaire pour l'instant)
        # TODO
        alert = None
        try:
            alert_type = self.alert_categories[categorie]
        except KeyError:
            warning(
                f"Alert type '{categorie}' not in alerts categories :"
                f" {list(self.alert_categories.keys())}. Alert will not be registred."
            )
            return None

        # Y a-t-il déjà une alerte pour l'utilisateur *en cours* de cette catégorie avec les mêmes paramètres ?
        alerts = Alert.records.filter(
            destinataire=destinataire,
            categorie=categorie,
            donnees=donnees,
            cloture__isnull=True,
        )
        if len(alerts) == 1:
            # Oui : Mets juste à jour l'alerte
            alert = alerts[0]
            alert.date_activation = date_activation
            alert.save()
        elif len(alerts) > 1:
            warning("Something is wrong...", alert)
        else:
            # Non : Enregistre la notification dans la base, dans une nouvelle alerte
            alert_kwargs = {
                'destinataire': destinataire,
                'categorie': categorie,
                'niveau': niveau,
                'donnees': donnees,
                'date_activation': date_activation,
            }
            alert = Alert(**alert_kwargs)
            alert.intitule = alert_type.get('message', "").format(
                link_url=config.settings.DEFAULT_DOMAIN
                + reverse(
                    alert_type.get('link_url_name', 'home'),
                    kwargs={'url_prefix': 'default'},
                ),
                **json.loads(donnees),
                **kwargs.get('msg_data', {}),
            )
            alert.save()

        return alert

    def send_alerts_messages(
        self,
        users: Optional[list] = None,
        verbosity: int = 0,
        stdout: OutputWrapper = None,
    ) -> None:
        """
        Envoie les messages (emails) avec les alertes en cours et met à jour la table des alertes
        avec la date d'envoi du dernier message.

        :param users: Liste des utilisateurs concernés (si None, valeur par défaut, tous les utilisateurs qui ont au moins une
            alerte en cours sont analysés.
        :param verbosity: verbosity level, from 0 to 4, as of command option (-v) verbosity level
        :param stdout: file-like output for messages (from BaseCommand.stdout). Optional.
        :return: None
        """

        # Queryset des utilisateurs qui ont au moins une alerte active
        if users is None:
            users = (
                get_user_model()
                .active_objects.all()
                .annotate(active_alerts=Count('alert', filter=Q(alert__cloture__isnull=True)))
                .filter(active_alerts__gt=0)
            )
        else:
            users = (
                get_user_model()
                .active_objects.filter(pk__in=users)
                .annotate(active_alerts=Count('alert', filter=Q(alert__cloture__isnull=True)))
                .filter(active_alerts__gt=0)
            )

        # Pour chaque utilisateur concerné :
        for user in users:
            if stdout and verbosity > 1:
                stdout.write("     Utilisateur: {}".format(user))
            preferences = UserSettings(user)

            email_policy = preferences['notifications.alert-email']
            if stdout and verbosity > 2:
                stdout.write("       Email policy: {}".format(email_policy))

            email_delay = int(preferences['notifications.alert-email-delay'])
            if stdout and verbosity > 2:
                stdout.write("       Email delay (h): {}".format(email_delay))

            if email_delay and user.last_email and (user.last_email + timedelta(hours=email_delay)) > now():
                break

            # contexte qui sera envoyé au template, le cas échéant
            context = {
                'user': user,
                'preferences': preferences,
                'categories': {},
                'group_size': preferences['notifications.alert-email-group-size'],
            }
            if stdout and verbosity > 2:
                stdout.write("       Email category group size: {}".format(context['group_size']))

            # Booléen pour savoir s'il faudra envoyer l'email à la fin du traitement
            # On récupère la préférence common.alerts_mail comme valeur de départ
            send_email = False

            # Cloture toutes les alertes en cours qui ne sont pas/plus dans une catégorie
            # active (par exemple désactivée dans le fichier de configuration)
            Alert.records.filter(~Q(categorie__in=alerts_manager.alert_categories.keys()), cloture__isnull=True,).update(  # noqa
                date_modification=now(),
                cloture=now(),
                commentaire=_("Catégorie d'alerte désactivée."),
            )

            # Types/catégories d'alarme qui ont au moins une alarme active à destination de cet utilisateur
            categories = (
                Alert.records.order_by()  # noqa
                .filter(cloture__isnull=True, destinataire=user)
                .values_list('categorie', flat=True)
                .distinct()
            )

            for category in categories:
                if stdout and verbosity > 2:
                    stdout.write("         Catégorie: {}".format(category), ending=': ')
                context['categories'][category] = {
                    'category': alerts_manager.alert_categories[category],
                    'alerts': [],
                }

                # category_email_delay = email_delay

                # Queryset de la liste des alarmes actives
                active_alerts = Alert.records.filter(cloture__isnull=True, destinataire=user, categorie=category)  # noqa
                count = 0
                for alert in active_alerts:
                    alert.intitule_txt = HTMLFilter.convert_html_to_text(alert.intitule)
                    context['categories'][category]['alerts'].append(alert)
                    if (
                        (email_policy == 'only_new' and alert.date_lecture is None and alert.dernier_email is None)
                        or (
                            email_policy == 'always'
                            and (
                                alert.dernier_email is None or (now() - alert.dernier_email).total_seconds() / 3600.0 > email_delay
                            )
                        )
                        # and (now() - alert.date_creation).total_seconds() / 3600.0 > category_email_delay
                    ):
                        send_email = True
                    count += 1
                context['categories'][category]['show_all_alerts'] = count < int(
                    preferences['notifications.alert-email-group-size']
                )
                if stdout and verbosity > 2:
                    stdout.write("{} alerte{}".format(count, "s" if count >= 2 else ""))

            if send_email and email_policy != 'never':
                if stdout and verbosity > 2:
                    stdout.write("      Sending email...")
                # Il y a quelque chose à envoyer, préparer le message
                text_content = render_to_string('common/email_alerts.txt', context)
                html_content = render_to_string('common/email_alerts.html', context)
                subject, from_email, to = (
                    _("Message de GÉQIP"),
                    'noreply@chu-amiens.fr',
                    user.email,
                )
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                for category in categories:
                    for alert in context['categories'][category]['alerts']:
                        alert.dernier_email = now()
                        alert.save(update_fields=['dernier_email', 'date_modification'])
                user.last_email = now()
                user.save(update_fields=['last_email', 'date_modification'])

    def notify(self):
        """Do the actual notification (messages, etc.)"""
        ...

    def user_alerts(self, user):
        """Get a user current alerts list"""
        ...
        return []

    def alerts_check(self):
        """Balaye tous les types d'alerte définis et exécute, s'il existe, la fonction de contrôle pour chacun de ces types
        puis enregistre toutes les alertes détectées dans le système
        """
        for alert_type_name, alert_type in self.alert_categories.items():
            # print('Checking...', alert_type_name)
            if 'check_func' in alert_type and callable(alert_type['check_func']):
                alerts, scope = alert_type['check_func'](alert_type_name, alert_type)
                detected = []
                for alert in alerts:
                    recorded = self.alert_record(**alert)
                    detected.append(recorded.pk)

                # Pour toutes les alertes du 'périmètre' (scope) qui sont dans la base, mais qui n'ont pas été détectées à nouveau
                # => les marquer comme terminées (cloture = maintenant)
                undetected_alerts = Alert.records.filter(cloture__isnull=True, **scope).exclude(pk__in=detected)
                undetected_alerts.update(cloture=timezone.now())

            # Deactivate alerts that are out of time
            if 'timeout' in alert_type:
                timeout = alert_type['timeout']
                alerts = Alert.records.filter(
                    cloture__isnull=True,
                    date_activation__lt=now() - timedelta(seconds=timeout),
                )
                alerts.update(cloture=timezone.now())


alerts_manager = AlertsManager()

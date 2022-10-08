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

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.timezone import now

from common.alerts import alerts_manager
from dem.models import Demande, Arbitrage


class Command(BaseCommand):
    help = """Balaye l'ensemble des demandes en cours, redirige éventuellement les demandes vers la bonne campagne et en
    informe le demandeur via une alerte 'éphémère'."""

    def handle(self, *args, **options):

        # Le traitement se fait en deux étapes :
        # - D'abord on modifie toutes les demandes pour lesquelles un changement de campagne a été acté par le dispatcher.
        #   L'alerte d'information de l'utilisateur est générée à cette étape.
        # - Puis on balaye toutes les demandes faites sur des campagnes virtuelles (sans dispatcher) et
        #   on les ferme avec une explication dans le commentaire.
        #
        # Faire deux balayages de la base est théoriquement inutile (puisqu'il n'est normalement pas possible
        # de saisir directement des demandes sur des campagnes virtuelles), mais cela permet de traiter plus proprement
        # tous les cas "limites", comme les éventuelles interruptions en cours de traitement, les changements de type de campagne
        # en cours de route (une campagne normale devenant virtuelle, etc.

        # 1 - Traite les redirections de campagnes
        qs = Demande.objects.filter(campagne_redirect__isnull=False)
        for demande in qs:
            print(
                "Demande {} ({}) à rediriger de {} vers {}".format(
                    demande.code,
                    demande.libelle,
                    demande.calendrier.code,
                    demande.campagne_redirect.code,
                )
            )

            # 1.1 - Génère l'alerte éphémère (qui entraînera l'envoi d'un message au demandeur)
            if alerts_manager.alert_record(
                categorie='dem.campaign-redirect',
                destinataire=demande.redacteur,
                donnees=json.dumps(
                    {
                        'dmd_code': demande.code,
                        'src_campaign': demande.calendrier.nom,
                        'dst_campaign': demande.campagne_redirect.nom,
                        'dispatcher_note': demande.dispatcher_note or '',
                        'campaign_message': demande.campagne_redirect.message
                        if demande.campagne_redirect.dispatcher is None
                        else '',
                    }
                ),
                niveau=1,
                date_activation=now(),
            ):

                # 1.2 - Modifie la campagne de la demande
                demande.calendrier = demande.campagne_redirect
                demande.campagne_redirect = None

                # 1.3 - Enregistrement de la demande modifiée
                demande.save(
                    update_fields=[
                        'calendrier',
                        'campagne_redirect',
                        'date_modification',
                    ]
                )

        # 2 - Ferme les demandes des campagnes virtuelles
        qs = Demande.objects.filter(Q(gel__isnull=True) | Q(gel=False), calendrier__dispatcher__isnull=True)
        for demande in qs:
            print(
                "Demande {} ({}) à fermer car la campagne {} est virtuelle".format(
                    demande.code, demande.libelle, demande.calendrier.code
                )
            )
            # 2.1 - S'il s'agit d'une campagne virtuelle, clos la demande avec un commentaire
            # Affecte à la demande le premier arbitrage de la liste qui ne valide pas la demande
            demande.arbitrage_commission = Arbitrage.objects.filter(valeur=False)[0]
            demande.commentaire_definitif_commission = demande.calendrier.message
            demande.gel = True

            # 2.2 - Enregistrement de la demande modifiée
            demande.save(
                update_fields=[
                    'arbitrage_commission',
                    'commentaire_definitif_commission',
                    'gel',
                    'date_modification',
                ]
            )

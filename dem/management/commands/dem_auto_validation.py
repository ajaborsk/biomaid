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
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.timezone import now
from django.utils.translation import gettext as _

from common.models import User, UserUfRole
from common.user_settings import UserSettings
from dem.models import Demande


class Command(BaseCommand):
    help = """Validation automatique des demandes remplissant certains critères :
        Demandes saisies par un utilisateur ayant le droit de validation et
        demandes d'un pôle pour lequel un chef donne délégation au cadre sup"""

    def handle(self, *args, **options):

        # Première partie : Donner un avis favorable CSP pour les demandes dont le rédacteur est aussi cadre superieur du pôle
        demandes = Demande.objects.filter(~Q(discipline_dmd__code='TX'), Q(state_code='NOUVELLE'))
        for demande in demandes:
            redacteur_roles = set(
                UserUfRole.objects.filter(
                    Q(uf=demande.uf)
                    | Q(service=demande.uf.service)
                    | Q(centre_responsabilite=demande.uf.centre_responsabilite)
                    | Q(pole=demande.uf.pole)
                    | Q(site=demande.uf.site)
                    | Q(etablissement=demande.uf.etablissement),
                    user=demande.redacteur,
                ).values_list('role_code', flat=True)
            )
            if 'CSP' in redacteur_roles:
                demande.avis_cadre_sup = True
                demande.commentaire_cadre_sup = (demande.commentaire_cadre_sup or '') + _(
                    "*** Avis favorable automatique le {:s} car le rédacteur a les droits pour donner cet avis ***"
                ).format(now().strftime(_("%d/%m/%Y")))
                demande.save(
                    update_fields=[
                        'date_modification',
                        'state_code',
                        'avis_cadre_sup',
                        'commentaire_cadre_sup',
                    ]
                )
                # print(demande.code, _("Avis favorable car le rédacteur est cadre sup."))

        # Seconde partie : valider les demandes dont le rédacteur est aussi chef de pôle ou directeur
        demandes = Demande.objects.filter(
            ~Q(discipline_dmd__code='TX'),
            Q(state_code='NOUVELLE') | Q(state_code='AVFAV_CSP'),
        )
        for demande in demandes:
            redacteur_roles = set(
                UserUfRole.objects.filter(
                    Q(uf=demande.uf)
                    | Q(service=demande.uf.service)
                    | Q(centre_responsabilite=demande.uf.centre_responsabilite)
                    | Q(pole=demande.uf.pole)
                    | Q(site=demande.uf.site)
                    | Q(etablissement=demande.uf.etablissement),
                    user=demande.redacteur,
                ).values_list('role_code', flat=True)
            )
            if {'CHP', 'DIR'} & redacteur_roles:
                demande.decision_validateur = True
                demande.decision_soumission = (demande.decision_soumission or '') + _(
                    "*** Demande validée automatiquement le {:s} car le rédacteur a les droits pour valider ***"
                ).format(now().strftime(_("%d/%m/%Y")))
                demande.save(
                    update_fields=[
                        'date_modification',
                        'state_code',
                        'decision_validateur',
                        'decision_soumission',
                    ]
                )
                # print(demande.code, _("validée car le rédacteur peut aussi valider."))

        # Troisième partie : valider les demandes dont la valeur, si elle existe, est inférieure au seuil défini par le chef de pôle
        demandes = Demande.objects.filter(
            ~Q(discipline_dmd__code='TX'),
            Q(state_code='NOUVELLE') | Q(state_code='AVFAV_CSP'),
        )
        for demande in demandes:
            if demande.montant_unitaire_expert_metier is not None:
                montant = demande.quantite * demande.montant_unitaire_expert_metier
            elif demande.prix_unitaire is not None:  # TODO: and demande.avis_biomed is True ?
                montant = demande.quantite * demande.prix_unitaire
            else:
                montant = None

            if montant is not None:
                validateurs = User.objects.filter(
                    pk__in=(
                        UserUfRole.objects.filter(
                            Q(uf=demande.uf)
                            | Q(service=demande.uf.service)
                            | Q(centre_responsabilite=demande.uf.centre_responsabilite)
                            | Q(pole=demande.uf.pole)
                            | Q(site=demande.uf.site)
                            | Q(etablissement=demande.uf.etablissement),
                            role_code__in=('DIR', 'CHP'),
                        )
                        .values_list('user', flat=True)
                        .distinct()
                    )
                )
                prefs = {}
                for validateur in validateurs:
                    if validateur not in prefs:
                        prefs[validateur] = UserSettings(validateur)
                    limite = prefs[validateur]['dem_eq.autovalidation.auto_amount']
                    if limite is not None and montant <= limite:
                        demande.decision_validateur = True
                        demande.decision_soumission = (demande.decision_soumission or '') + _(
                            "*** Demande validée automatiquement le {:s} car le montant est inférieur"
                            " au seuil ({:d} €) défini par le responsable du pôle ou de la direction fonctionnelle ***"
                        ).format(now().strftime(_("%d/%m/%Y")), limite)
                        demande.save(
                            update_fields=[
                                'date_modification',
                                'state_code',
                                'decision_validateur',
                                'decision_soumission',
                            ]
                        )
                        # print(demande, montant, validateur, limite)
                        break
                    else:
                        limite = prefs[validateur]['dem_eq.autovalidation.auto_amount_csp']
                        if limite is not None and montant <= limite and demande.avis_cadre_sup is True:
                            demande.decision_validateur = True
                            demande.decision_soumission = (demande.decision_soumission or '') + _(
                                "*** Demande validée automatiquement le {:s} car le montant est inférieur"
                                " au seuil ({:d} €) défini par le responsable du pôle ou de la direction"
                                " fonctionnelle avec un avis favorable du cadre supérieur de pôle***"
                            ).format(now().strftime(_("%d/%m/%Y")), limite)
                            demande.save(
                                update_fields=[
                                    'date_modification',
                                    'state_code',
                                    'decision_validateur',
                                    'decision_soumission',
                                ]
                            )
                            # print(demande, montant, validateur, limite)
                            break

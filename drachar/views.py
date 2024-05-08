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

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from common.base_views import BiomAidViewMixin
from drachar.forms import NouveauDossierForm  # ContactLivForm
from django.db.models import F, When, Case, DecimalField, IntegerField
from smart_view.smart_page import SmartPage
from drachar.smart_views import (
    ContactLivraisonSmartView,
)
from common.models import Programme


from drachar.models import Previsionnel
from dem.models import Demande


class GestionPrevisionnel(BiomAidViewMixin, TemplateView):
    permissions = {'EXP', 'ADM'}
    template_name = 'drachar/gestion_previsionnel.html'

    def __init__(self, *args, **kwargs):
        self.previsionnel = None
        self.demandesval = None
        self.message_error = ""
        super().__init__(*args, **kwargs)

    def setup(self, request, *args, programme, **kwargs):
        super().setup(request, *args, **kwargs)
        self.programme = programme

        if self.programme == "Tous":
            self.previsionnel = Previsionnel.objects.all()
            self.demandesval = Demande.objects.filter(arbitrage_commission__valeur=True, gel=True, previsionnel__isnull=True)
        else:
            self.demandesval = Demande.objects.filter(
                arbitrage_commission__valeur=True,
                programme=self.programme,
                gel=True,
                previsionnel__isnull=True,
            )
            self.previsionnel = Previsionnel.objects.filter(programme=self.programme)

        # Calcul de l'enveloppe validée pour chaque demande
        self.demandesval = (
            self.demandesval.annotate(
                qte_validee=Case(
                    When(quantite_validee__isnull=False, then=F('quantite_validee')),
                    default=F('quantite'),
                    output_field=IntegerField(),
                )
            )
            .annotate(
                pu=Case(
                    When(
                        montant_unitaire_expert_metier__isnull=False,
                        then=F('montant_unitaire_expert_metier'),
                    ),
                    default=F('prix_unitaire'),
                    output_field=DecimalField(),
                )
            )
            .annotate(
                enveloppe=Case(
                    When(enveloppe_allouee__isnull=False, then=F('enveloppe_allouee')),
                    default=F('pu') * F('qte_validee'),
                    output_field=DecimalField(),
                )
            )
        )

    def post(self, request, **kwargs):
        if 'importprevisionnel' in request.POST:
            print('importprevisionnel')
            stop = False
            message_error = ""
            for demande in self.demandesval:
                if demande.programme is None:
                    message_error1 = "le programme n'est pas renseigné pour la demande " + str(demande.code)
                    stop = True
                    message_error = message_error + message_error1 + ", "
                if demande.expert_metier is None:
                    message_error2 = "l'expert n'est pas renseigné pour la demande " + str(demande.code)
                    stop = True
                    message_error = message_error + message_error2 + ", "
                if demande.enveloppe is None or demande.enveloppe == 'NULL' or demande.enveloppe < 0:
                    message_error3 = "l'enveloppe n'est pas renseignée pour la demande " + str(demande.code)
                    stop = True
                    message_error = message_error + message_error3 + ", "
            if stop:
                print('Alerte : des Champs obligatoires sont vides, imports avorté :')
                print(message_error)
                self.message_error = "Alerte : des Champs obligatoires sont vides, imports avorté :" + message_error
            else:
                for demande in self.demandesval:
                    rise = 0
                    for prev in self.previsionnel:  # Test si la demande existe déjà dans le prévisionnel pour ne pas l'écraser
                        if demande.num_dmd == prev.num_dmd.pk:
                            rise = 1
                    if rise == 1:
                        print("ne rien faire, la demande " + str(demande.code) + " existe dejà")
                    else:
                        prog = Programme.objects.get(pk=demande.programme.id)
                        expert = get_user_model().objects.get(pk=demande.expert_metier.id)
                        enveloppe = demande.enveloppe
                        p = Previsionnel(
                            num_dmd=demande,
                            programme=prog,
                            budget=enveloppe,
                            expert=expert,
                            uf=demande.uf,
                        )
                        p.save()
                        print("copier la demande :" + str(demande.num_dmd))
                        print(str(p.num_dmd) + ' - ' + str(p.programme) + ' - ' + str(p.expert) + ' - ' + str(p.budget))

                # On relit la base pour mettre à jour la page

                if self.programme == "Tous":
                    self.previsionnel = Previsionnel.objects.all()
                    self.demandesval = Demande.objects.filter(
                        arbitrage_commission__valeur=True,
                        gel=True,
                        previsionnel__isnull=True,
                    )
                else:
                    self.demandesval = Demande.objects.filter(
                        arbitrage_commission__valeur=True,
                        programme=self.programme,
                        gel=True,
                        previsionnel__isnull=True,
                    )
                    self.previsionnel = Previsionnel.objects.filter(programme=self.programme)

                # Calcul de l'enveloppe validée pour chaque demande
                self.demandesval = (
                    self.demandesval.annotate(
                        qte_validee=Case(
                            When(
                                quantite_validee__isnull=False,
                                then=F('quantite_validee'),
                            ),
                            default=F('quantite'),
                            output_field=IntegerField(),
                        )
                    )
                    .annotate(
                        pu=Case(
                            When(
                                montant_unitaire_expert_metier__isnull=False,
                                then=F('montant_unitaire_expert_metier'),
                            ),
                            default=F('prix_unitaire'),
                            output_field=DecimalField(),
                        )
                    )
                    .annotate(
                        enveloppe=Case(
                            When(
                                enveloppe_allouee__isnull=False,
                                then=F('enveloppe_allouee'),
                            ),
                            default=F('pu') * F('qte_validee'),
                            output_field=DecimalField(),
                        )
                    )
                )
        else:
            print('rien')
        return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtre_programme'] = self.programme
        context['previsionnel'] = self.previsionnel
        context['demandesval'] = self.demandesval
        context['message_error'] = self.message_error
        return context


"""CREER UNE SMARTVIEW à la place appellée gestioncontactlivraison22"""


class GestionContactLivraison(BiomAidViewMixin, TemplateView):
    permissions = {'EXP', 'ADM'}
    template_name = 'drachar/gestion_contact_liv.html'

    def post(self, request, **kwargs):
        ...
        return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(title=_("GESTION DES CONTACTS DE LIVRAISON"))
        return context


class GestionContactLivraison22(SmartPage):
    application = 'common'
    name = 'contactlivraison'
    permissions = {'ADM', 'MAN', 'EXP'}
    smart_view_class = ContactLivraisonSmartView
    title = "Contact Livraison"


class NouveauDossier(BiomAidViewMixin, TemplateView):
    permissions = {'EXP', 'ADM'}
    template_name = 'drachar/nouveaudossier.html'

    def get_context_data(self, **kwargs):
        self.form_dossier = NouveauDossierForm(self.request.user, self.request.POST or None)

        context = super().get_context_data(**kwargs)
        context.update(form_dossier=self.form_dossier)
        return context

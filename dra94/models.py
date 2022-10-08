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
from django.db import models

# Create your models here.


class Dra94Prevision(models.Model):
    class Meta:
        ordering = ['record_no']

    record_no = models.IntegerField(
        null=True,
        blank=True,
    )
    programme = models.CharField(
        max_length=16,
        null=True,
        blank=True,
    )
    ligne = models.IntegerField(
        null=True,
        blank=True,
    )
    service = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
    code_famille = models.CharField(
        max_length=16,
        null=True,
        blank=True,
    )
    qte_demandee = models.IntegerField(
        null=True,
        blank=True,
    )
    intitule = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    qte_acquise = models.IntegerField(
        null=True,
        blank=True,
    )
    cout_francs = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        null=True,
        blank=True,
    )
    cout_euros = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        null=True,
        blank=True,
    )
    remarque = models.TextField(
        null=True,
        blank=True,
    )
    cellule = models.CharField(
        max_length=2,
        null=True,
        blank=True,
    )
    cout_realise = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        null=True,
        blank=True,
    )
    solde = models.BooleanField(
        null=True,
        blank=True,
    )
    code_uf = models.CharField(
        max_length=4,
        null=True,
        blank=True,
    )

    # Les champs ci-dessous ne font pas partie de la table originale de DRA94
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date de création',
        null=True,
    )

    def str(self):
        return "Prévisionnel n°{}".format(self.record_no)


class Dra94Dossier(models.Model):
    class Meta:
        pass

    record_no = models.IntegerField(
        null=True,
        blank=True,
    )
    programme = models.CharField(
        max_length=16,
        null=True,
        blank=True,
    )
    ligne = models.IntegerField(
        null=True,
        blank=True,
    )
    numero = models.IntegerField(
        null=True,
        blank=True,
    )
    date_dossier = models.DateTimeField(
        null=True,
        blank=True,
    )
    fournisseur = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    code_fournisseur = models.IntegerField(
        null=True,
        blank=True,
    )
    contact_fournisseur = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    numero_devis = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    date_devis = models.DateTimeField(
        null=True,
        blank=True,
    )
    montant = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        null=True,
        blank=True,
    )
    code_famille = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    contact = models.CharField(
        verbose_name="Contact interne CHU",
        max_length=128,
        null=True,
        blank=True,
    )
    contact_livraison = models.CharField(
        verbose_name="Contact interne CHU pour la livraison",
        max_length=128,
        null=True,
        blank=True,
    )
    point = models.IntegerField(
        null=True,
        blank=True,
    )
    numero_compte = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    ugap = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    divers = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    dsio = models.BooleanField(
        null=True,
        blank=True,
    )
    date_transmission = models.DateTimeField(
        null=True,
        blank=True,
    )
    no_commande = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    date_commande = models.DateTimeField(
        null=True,
        blank=True,
    )
    fin_dossier = models.BooleanField(
        null=True,
        blank=True,
    )
    cellule = models.CharField(
        max_length=2,
        null=True,
        blank=True,
    )
    no_marche = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    imprime = models.BooleanField(
        null=True,
        blank=True,
    )
    pieces_jointes = models.BooleanField(
        null=True,
        blank=True,
    )

    # Les champs ci-dessous ne font pas partie de la table originale de DRA94
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date de création',
        null=True,
    )

    def str(self):
        return "DRA{}".format(self.record_no)


class Dra94Ligne(models.Model):
    class Meta:
        pass

    record_no = models.IntegerField(
        null=True,
        blank=True,
    )
    departement = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    date_dossier = models.DateTimeField(
        verbose_name="Semble inutilisé",
        null=True,
        blank=True,
    )
    tri = models.CharField(
        verbose_name="tri ? Semble inutilisé.",
        max_length=128,
        null=True,
        blank=True,
    )
    numero_dossier = models.IntegerField(
        verbose_name="Clef vers le dossier",
        null=True,
        blank=True,
    )
    code_uf = models.CharField(
        max_length=8,
        null=True,
        blank=True,
    )
    cadre = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    designation = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    designation_cneh = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    code_cneh = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    specificite = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    type_modele = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    reference = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    quantite = models.IntegerField(
        null=True,
        blank=True,
    )
    access = models.CharField(
        verbose_name="???",
        max_length=1024,
        null=True,
        blank=True,
    )
    fournisseur = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    contact_fournisseur = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    equipement_a_recuperer = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    mutation_reforme = models.CharField(
        max_length=8,
        null=True,
        blank=True,
    )
    service = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    formation = models.BooleanField(
        null=True,
        blank=True,
    )
    visite_fin_garantie = models.BooleanField(
        null=True,
        blank=True,
    )
    pu_ttc = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        null=True,
        blank=True,
    )
    code_uf_mutation = models.CharField(
        max_length=4,
        null=True,
        blank=True,
    )
    service_mutation = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    sct_mutation = models.CharField(
        verbose_name="SCT ??",
        max_length=1024,
        null=True,
        blank=True,
    )
    montant = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        null=True,
        blank=True,
    )
    numero_reforme = models.CharField(
        verbose_name="Numéro de réforme",
        max_length=16,
        null=True,
        blank=True,
    )
    duree_garantie = models.IntegerField(
        verbose_name="Durée de la garantie en mois",
        null=True,
        blank=True,
    )
    jours_formation = models.IntegerField(
        verbose_name="Nombre de jours de formation",
        null=True,
        blank=True,
    )
    site = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    dsio = models.FloatField(
        verbose_name="??? C'est quoi ???",
        null=True,
        blank=True,
    )
    direction = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    rubrique = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    annee_rubrique = models.IntegerField(
        null=True,
        blank=True,
    )
    choix = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    cout_maintenance = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        null=True,
        blank=True,
    )
    supplementaire = models.BooleanField(
        verbose_name="Coût maintenance à prévoir dans l'EPRD ???",
        null=True,
        blank=True,
    )
    marque = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    remise = models.FloatField(
        verbose_name="Remise consentie en pourcent",
        null=True,
        blank=True,
    )
    pu_ht = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        null=True,
        blank=True,
    )
    gain_ht = models.DecimalField(
        verbose_name="Gain HT (unitaire ou total ???)",
        decimal_places=2,
        max_digits=12,
        null=True,
        blank=True,
    )
    date_reception = models.DateTimeField(
        null=True,
        blank=True,
    )
    date_mise_en_service = models.DateTimeField(
        null=True,
        blank=True,
    )
    recu = models.BooleanField(
        null=True,
        blank=True,
    )
    installe = models.BooleanField(
        null=True,
        blank=True,
    )
    taux_tva = models.FloatField(
        verbose_name="Taux de la TVA en pourcent",
        null=True,
        blank=True,
    )
    contrat = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    classe = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )

    # Les champs ci-dessous ne font pas partie de la table originale de DRA94
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date de création',
        null=True,
    )

    def str(self):
        return "Ligne DRA {}".format(self.record_no)

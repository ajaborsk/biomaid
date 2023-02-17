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
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 19:54:59 2018
@author: kligliro
"""
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.db.models import Q
from django.utils.timezone import now
from django.utils.translation import gettext as _

from document.models import GenericDocument
from generic_comment.models import GenericComment

from common import config

# les tables ci-dessous sont mise à jour par des scripts
# qui vont chercher dans ASSETPLUS les infos :
#   Cneh
#   Comptes
#   Etablissement
#
# dans MAGH2 :
#   fournisseurs
#
# dans CONVERGENCE :
#   Structure

# au niveau utilisateurs:
# les demandes renseignées par le chefs de pôles/services
# validées ensuite par les chefs de pôles .


class ActiveManager(models.Manager):
    """
    Un manager (d'ORM) qui ne retourne que les instances 'actives', c'est à dire qui peuvent être choisies, par exemple,
    lors de la création d'une instance d'un modèle avec une clé externe.
    """

    def get_queryset(self):
        return (
            super().get_queryset().filter(Q(**{self.END_FIELDNAME + '__isnull': True}) | Q(**{self.END_FIELDNAME + '__gt': now()}))
        )


class ActiveManagerCloture(ActiveManager):
    END_FIELDNAME = 'cloture'


class ActiveManagerUser(models.Manager):
    """
    A ORM manager that returns only active users. Works only for Django 'User' herited classes
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class User(AbstractUser):
    from_ldap: models.BooleanField = models.BooleanField(_("LDAP user"), editable=False, default=False)

    etablissement: models.ForeignKey = models.ForeignKey(
        'Etablissement',
        on_delete=models.PROTECT,
        null=True,
    )
    initiales: models.CharField = models.CharField(
        max_length=10,
        blank=True,
        null=False,
    )
    titre: models.CharField = models.CharField(
        verbose_name=_("Titre"),
        help_text=_("M. / Mme / Mlle / Dr / Pr ..."),
        max_length=32,
        null=True,
        blank=True,
    )
    intitule_fonction: models.CharField = models.CharField(
        verbose_name=_("Fonction (intitulé)"),
        max_length=256,
        null=True,
        blank=True,
    )
    tel_fixe: models.CharField = models.CharField(
        verbose_name=_("Tél. fixe"),
        max_length=17,
        blank=True,
        null=False,
    )
    tel_dect: models.CharField = models.CharField(
        verbose_name=_("Tél. DECT"),
        max_length=17,
        blank=True,
        null=False,
    )
    tel_mobile: models.CharField = models.CharField(
        verbose_name=_("Tél. mobile"),
        max_length=17,
        blank=True,
        null=False,
    )
    preferences: models.TextField = models.TextField(
        verbose_name=_("Préférences"),
        help_text=_("Préférences de l'utilisateur, stockées sous forme d'une chaine JSON"),
        null=False,
        blank=False,
        default="{}",
    )
    last_seen: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Dernière visite"),
        help_text=_("Date de la dernière visite sur le portail"),
        null=True,
        blank=True,
    )
    last_email: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Dernier message"),
        help_text=_("Date du dernier mail envoyé"),
        null=True,
        blank=True,
    )
    date_creation: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("date de création"),
    )
    date_modification: models.DateTimeField = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date de modification"),
    )

    objects = UserManager()  # The default manager.
    active_objects = ActiveManagerUser()  # The active_objects manager.

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.username)


class Uf(models.Model):
    class Meta:
        unique_together = (('etablissement', 'code', 'cloture'),)
        ordering = ['code']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['etablissement']),
            models.Index(fields=['site']),
            models.Index(fields=['pole']),
            models.Index(fields=['centre_responsabilite']),
            models.Index(fields=['service']),
            models.Index(fields=['cloture']),
        ]

    lettre_budget = models.CharField(max_length=1, verbose_name='Budget')
    code = models.CharField(max_length=8, verbose_name='Code UF')
    nom = models.CharField(max_length=50, verbose_name='Nom UF')
    intitule = models.CharField(
        verbose_name=_("Intitulé"),
        help_text=_("Nom complet de l'unité fonctionnelle"),
        max_length=256,
        null=True,
        blank=True,
    )

    etablissement = models.ForeignKey(
        'Etablissement',
        on_delete=models.CASCADE,
    )
    site = models.ForeignKey(
        'Site',
        on_delete=models.CASCADE,
    )
    pole = models.ForeignKey(
        'Pole',
        on_delete=models.CASCADE,
    )
    centre_responsabilite = models.ForeignKey(
        'CentreResponsabilite',
        on_delete=models.CASCADE,
    )
    service = models.ForeignKey(
        'Service',
        on_delete=models.PROTECT,
    )

    cloture = models.DateField(verbose_name=_("date de clôture de l'UF"), null=True, blank=True, default=None)

    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification')

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.

    def __str__(self):
        return "{0} - {1}".format(self.code, self.nom)


class Service(models.Model):
    class Meta:
        verbose_name = _("service")

    code = models.CharField(max_length=8)
    nom = models.CharField(max_length=50)
    intitule = models.CharField(
        verbose_name=_("Intitulé"),
        help_text=_("Nom complet du service"),
        max_length=256,
        null=True,
        blank=True,
    )
    cloture = models.DateField(
        verbose_name=_("date de clôture du service"),
        null=True,
        blank=True,
        default=None,
    )
    etablissement = models.ForeignKey(
        'Etablissement',
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification')

    def __str__(self):
        return "{0} - {1}".format(self.code, self.nom)


class CentreResponsabilite(models.Model):
    class Meta:
        verbose_name = _("centre de responsabilité")
        verbose_name_plural = _("centres de responsabilité")

    code = models.CharField(max_length=8)
    nom = models.CharField(max_length=50)
    intitule = models.CharField(
        verbose_name=_("Intitulé"),
        help_text=_("Nom complet du centre de responsabilité"),
        max_length=256,
        null=True,
        blank=True,
    )
    cloture = models.DateField(
        verbose_name='date de cloture du centre de responsabilité',
        null=True,
        blank=True,
        default=None,
    )
    etablissement = models.ForeignKey(
        'Etablissement',
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification')

    def __str__(self):
        return "{0} - {1}".format(self.code, self.nom)


class Pole(models.Model):
    class Meta:
        verbose_name = _("pôle")

    code = models.CharField(max_length=8)
    nom = models.CharField(max_length=50)

    intitule = models.CharField(
        verbose_name=_("Intitulé"),
        help_text=_("Nom complet du pôle"),
        max_length=256,
        null=True,
        blank=True,
    )
    # code_Site = models.ForeignKey('Site', on_delete=models.PROTECT)
    cloture = models.DateField(verbose_name=_("date de clôture du pole"), null=True, blank=True, default=None)
    etablissement = models.ForeignKey(
        'Etablissement',
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification')

    def __str__(self):
        return "{0} - {1}".format(self.code, self.nom)


class Site(models.Model):
    code = models.CharField(max_length=8)
    nom = models.CharField(max_length=50)
    intitule = models.CharField(
        verbose_name=_("Intitulé"),
        help_text=_("Nom complet du site"),
        max_length=256,
        null=True,
        blank=True,
    )
    # code_organisation = models.ForeignKey('Etablissement', on_delete=models.PROTECT)
    cloture = models.DateField(verbose_name=_("date de clôture du site"), null=True, blank=True, default=None)
    etablissement = models.ForeignKey(
        'Etablissement',
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification')

    def __str__(self):
        return "{0} - {1}".format(self.code, self.nom)


class Etablissement(models.Model):
    """terme employé dans AssetPlus pour désigner les Centres du GHT : CHD, CHUAP, CHAM, CHABB..."""

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['prefix'], name='etablissement_prefix_is_unique'),
        ]

    code = models.CharField(max_length=5, default='')
    code_gmao = models.DecimalField(max_digits=5, decimal_places=0)  # clé donnée par asset+
    prefix = models.CharField(max_length=4, blank=True)  # Lettre préfixe utilisée pour les codes (notamment dans Asset+)
    nom = models.CharField(max_length=50)  # Nom du Centre
    intitule = models.CharField(
        verbose_name=_("Intitulé"),
        help_text=_("Nom complet de l'établissement"),
        max_length=256,
        null=True,
        blank=True,
    )

    cloture = models.DateField(
        verbose_name=_("date de clôture de l' établissement"),
        null=True,
        blank=True,
        default=None,
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification')

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.

    def __str__(self):
        return "{0} - {1}".format(self.code, self.nom)


class Discipline(models.Model):
    """il s'agit d'un SERVICE ACHETEUR/EXPERT METIER et qui sera référent de la demande"""

    code = models.CharField(max_length=3)  # code du service concerné par la demande
    nom = models.CharField(max_length=30, null=True)  # nom du service concerné par la demande
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création', null=True)
    cloture = models.DateField(verbose_name='date de fin', null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification', null=True)

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.

    def __str__(self):
        return "{0} - {1}".format(self.code, self.nom)


# class ExpertMetier(models.Model):
# """acheteur/expert métier.

# """
# code = models.CharField(  # initiale expert
# max_length=5,
# default=None,
# blank=True,
# null=True)
# nom = models.CharField(max_length=30, primary_key=True)
# prenom = models.CharField(max_length=30)
# dect = models.CharField(max_length=30)
# user = models.ForeignKey(  # référence à la table des utilisateurs django
# User,
# on_delete=models.PROTECT,)
# date_creation = models.DateTimeField(
# auto_now_add=True,
# verbose_name='date de création')
# date_modification = models.DateTimeField(
# auto_now=True,
# verbose_name='date de modification')

# def __str__(self):
# return "{0} - {1}".format(self.code, self.nom)


class Domaine(models.Model):
    """Il s'agit d'une domaine technique : Imagerie, Endoscopie, Perfusion..."""

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code'], name='domaine_code_is_unique'),
        ]

    code = models.CharField(max_length=16, default=None, blank=True, null=True)  # code du domaine
    nom = models.CharField(max_length=64)  # Nom du domaine de l'équipement.
    # expert_metier = models.ForeignKey(  # code de l'acheteur/Expert métier concerné par le domaine
    #     'ExpertMetier',
    #     on_delete=models.PROTECT,)
    parent = models.ForeignKey(
        'Domaine',
        default=None,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    # expert = models.ForeignKey(ExtensionUser, null=True, blank=True, default=None, on_delete=models.CASCADE)
    discipline = models.ForeignKey(  # DISCIPLINE (Bio, ST, Travaux, DSN...
        'Discipline',
        default=None,
        on_delete=models.PROTECT,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        null=True,
        default=None,
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification')

    def __str__(self):
        return "{0} - {1}".format(self.code, self.nom)


class Programme(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code'], name='programme_code_is_unique'),
        ]

    code = models.CharField(max_length=16, null=False, blank=False)  # N° de programme
    nom = models.CharField(max_length=64, null=False, blank=False)  # Nom du programme
    description = models.TextField(null=True, blank=True, default=None)  # commentaires si nécessaire
    etablissement = models.ForeignKey(Etablissement, null=True, blank=True, on_delete=models.SET_NULL)
    pole = models.ForeignKey(Pole, null=True, blank=True, on_delete=models.SET_NULL)
    uf = models.ForeignKey(Uf, null=True, blank=True, on_delete=models.SET_NULL)
    enveloppe = models.DecimalField(max_digits=10, decimal_places=0, null=False, blank=False)  # enveloppe budgetaire prévisionnelle
    limit = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)  # enveloppe budgetaire limite (bloquante)
    arbitre = models.ForeignKey(
        config.settings.AUTH_USER_MODEL,
        db_column='arbitre_new',
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
    )
    debut_arbitrage = models.DateField(verbose_name="date de début d'arbitrage", null=True, blank=True)
    # arbitre_ext = models.ForeignKey(ExtensionUser, null=True, blank=True, default=None, on_delete=models.CASCADE)
    calendrier = models.ForeignKey('dem.Campagne', null=True, blank=True, default=None, on_delete=models.PROTECT)
    discipline = models.ForeignKey('Discipline', default=None, on_delete=models.PROTECT)  # discipline rattachée au programme
    anteriorite = models.CharField(  # N° de programme de DRA 94
        max_length=10,
        null=True,
        blank=True,
        default=None,
    )
    # Generic fields
    comments = GenericRelation(GenericComment, related_query_name='marche')
    documents = GenericRelation(GenericDocument, related_query_name='marche')

    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    cloture = models.DateField(verbose_name='date de fin', null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification')

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.

    def __str__(self):
        return "{0} - {1}".format(self.code, self.nom)


class Fournisseur(models.Model):
    """Table des fournisseurs de base dans BiomAid.
    Pour les établissements, il est nécessaire d'avoir une table supplémentaire FournisseurEtablissement
    qui fait le lien entre la codification propre de l'établissement (dans sa GEF) et cette table.
    """

    code: models.IntegerField = models.IntegerField(
        null=False,
        blank=False,
    )
    nom: models.CharField = models.CharField(
        max_length=256,
        null=False,
        blank=False,
    )

    # Il faudra ajouter ici tous les champs qui sont identiques pour un fournisseur quelque soit l'établissement :
    #   n°SIRET, adresse siège social, etc.

    date_creation: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    cloture: models.DateTimeField = models.DateTimeField(verbose_name='date de fin', null=True, blank=True)
    date_modification: models.DateTimeField = models.DateTimeField(auto_now=True, verbose_name='date de modification')

    objects: models.Manager = models.Manager()  # The default manager.
    active_objects: models.Manager = ActiveManagerCloture()  # The active_objects manager.

    def __str__(self):
        return "{0} - {1}".format(self.code, self.nom)


class FournisseurEtablissement:

    code: models.CharField = models.CharField(
        max_length=64,
        null=False,
        blank=False,
    )
    etablissement: models.ForeignKey = models.ForeignKey(
        Etablissement,
        on_delete=models.PROTECT,
    )
    fournisseur: models.ForeignKey = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT,
    )

    date_creation: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    date_modification: models.DateTimeField = models.DateTimeField(auto_now=True, verbose_name='date de modification')
    cloture: models.DateTimeField = models.DateTimeField(verbose_name='date de fin', null=True, blank=True)

    objects: models.Manager = models.Manager()  # The default manager.
    active_objects: models.Manager = ActiveManagerCloture()  # The active_objects manager.

    def __str__(self):
        return "{0} - {1} ({2})".format(self.code, self.fournisseur.nom, self.etablissement.nom)


class ContactFournisseur(models.Model):
    """ajouter class ContactFournisseur avec FK sur Fournisseur"""

    DIVISION = (
        ('COM', 'Commercial'),
        ('SPE', 'Specialiste'),
        ('MARK', 'Marketing'),
        ('SAV', 'Service Apres Vente'),
    )
    nom: models.CharField = models.CharField(max_length=300, verbose_name='Nom', null=True, blank=True)
    prenom: models.CharField = models.CharField(max_length=300, verbose_name='Prenom', null=True, blank=True)
    societe: models.ForeignKey = models.ForeignKey(
        'Fournisseur',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    # Lien entre le contact et les établissements. Si ce champ est NULL,
    # cela signifie que le contact est valable pour tous les établissements de la base
    etablissement: models.ForeignKey = models.ForeignKey(
        'Etablissement',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    division: models.CharField = models.CharField(
        choices=DIVISION,
        max_length=300,
        null=False,
        blank=False,
    )
    telephone1: models.CharField = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )
    telephone2: models.CharField = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )
    Fax: models.CharField = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )
    mail: models.CharField = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )
    adresse_contact: models.TextField = models.TextField(
        null=True,
        blank=True,
        default=None,
    )
    cp_contact: models.CharField = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        default=None,
    )
    ville_contact: models.CharField = models.CharField(
        max_length=60,
        null=True,
        blank=True,
        default=None,
    )
    commentaire: models.TextField = models.TextField(
        null=True,
        blank=True,
        default=None,
    )
    date_creation: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    cloture: models.DateTimeField = models.DateTimeField(verbose_name='date de fin', null=True, blank=True)
    date_modification: models.DateTimeField = models.DateTimeField(auto_now=True, verbose_name='date de modification')

    objects: models.Manager = models.Manager()  # The default manager.
    active_objects: models.Manager = ActiveManagerCloture()  # The active_objects manager.

    def __str__(self):
        return "{0} - {1} - {2}".format(self.nom, self.prenom, self.societe)


class DataFournisseurGEF(models.Model):  # quid du code vis a vis des différents établissements. comment les gérer
    code_gef = models.CharField(
        max_length=60,
        null=False,
        blank=False,
        default=None,
    )
    intitule_fournisseur = models.CharField(
        max_length=60,
        null=False,
        blank=False,
        default=None,
    )
    raison_sociale = models.CharField(
        max_length=60,
        null=False,
        blank=False,
        default=None,
    )
    adresse_1_fournisseur = models.TextField(
        null=True,
        blank=True,
        default=None,
    )
    cp_fournisseur = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        default=None,
    )
    ville_fournisseur = models.CharField(
        max_length=60,
        null=True,
        blank=True,
        default=None,
    )
    tel_fournisseur = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        default=None,
    )
    fax_fournisseur = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        default=None,
    )
    telex_fournisseur = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        default=None,
    )
    nu_siret = models.CharField(
        max_length=25,
        null=False,
        blank=False,
    )
    num_tva_intracommunautaire = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        default=None,
    )
    etablissement = models.ForeignKey(
        'Etablissement',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    code_recon = models.ForeignKey('Fournisseur', null=True, blank=False, on_delete=models.PROTECT)
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    cloture = models.DateField(verbose_name='date de fin', null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification')

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.

    def __str__(self):
        return "{0} - {1}".format(self.id, self.intitule_fournisseur)


class Compte(models.Model):
    LETTRE_BUDGETAIRE = (
        ('A', 'DOTATION NON AFFECTEE'),
        ('B', 'LONG SEJOUR'),
        ('C', 'ECOLES'),
        ('E', 'EHPAD'),
        ('G', 'GHT'),
        ('H', 'BUDGET PRINCIPAL'),
        ('P', 'CAMSP'),
        ('R', 'CENTRE RESSOURCE AUTISME'),
    )
    lettre_budgetaire = models.CharField(
        choices=LETTRE_BUDGETAIRE, max_length=300, null=False, blank=False, default='H'
    )  # champs convergence : CLB_CODE
    etablissement = models.ForeignKey(
        'Etablissement',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    code = models.CharField(max_length=25, null=False, blank=False)
    nom = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        default=None,
    )
    discipline = models.ForeignKey('Discipline', on_delete=models.PROTECT, null=True, blank=False)
    exercice = models.DateField(
        verbose_name=_("Exercice Budgétaire"),
        help_text=_("Exercice Budgétaire"),
        null=True,
        blank=True,
        default=None,
    )
    budget_montant = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, default='0')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    cloture = models.DateField(verbose_name='date de cloture', null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification')

    def __str__(self):
        return "{0} - {1} - {2}".format(self.lettre_budgetaire, self.code, self.nom)


class ClasseCode(models.Model):
    code = models.CharField(
        max_length=90,
        default=None,
        verbose_name="Code de la classe",
        blank=False,
        null=False,
    )
    nom = models.CharField(
        max_length=90,
        default=None,
        verbose_name='Nom de la classe',
        blank=False,
        null=False,
    )
    complement = models.CharField(
        max_length=300,
        default=None,
        verbose_name="Compléments d'information",
        blank=False,
        null=False,
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    cloture = models.DateField(verbose_name='Date de fin', null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True, verbose_name='Date de modification')
    id_gmao = models.CharField(max_length=300, null=True, blank=True, verbose_name='ID de la GMAO')

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.

    def __str__(self):
        return "{0} - {1}".format(self.code, self.nom)


class Marque(models.Model):
    nom = models.CharField(
        max_length=90,
        default=None,
        verbose_name='Nom de la marque',
        blank=False,
        null=False,
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    cloture = models.DateField(verbose_name='Date de fin', null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True, verbose_name='Date de modification')
    id_gmao = models.CharField(max_length=300, null=True, blank=True, verbose_name='ID de la GMAO')

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.

    def __str__(self):
        return "{0} - {1}".format(self.nom, self.cloture)

    # TODO : MAJ date lors du .save() pas fonctionnelle lors de l'essaiss

    # def save(self, *args, **kwargs):
    #    # do this only when created
    #    try:
    #        instance = LastUpdate.objects.get(table_in="Marque")
    #        instance.date_last_update = timezone.now()
    #    except LastUpdate.DoesNotExist:
    #        LastUpdate.objects.get_or_create(table_in="Marque", date_last_update=timezone.now())
    #    super().save(*args, **kwargs)


class Type(models.Model):
    CLASSE_CHOICES = (
        ('1', 'Classe 1'),
        ('2a', 'Classe 2a'),
        ('2b', 'Classe 2b'),
        ('3', 'Classe 3'),
    )
    type = models.TextField(default=None, verbose_name="Type/Modèle d'appareil", blank=False, null=False)
    complement = models.TextField(default=None, verbose_name="Compléments d'information", blank=False, null=False)
    marque = models.ForeignKey('Marque', on_delete=models.PROTECT, null=False, blank=False)
    discipline = models.ForeignKey(  # sera l'équivalent de la vocation fonctionnelle de Asset+ en cas de connexion
        'Discipline', on_delete=models.PROTECT, null=True, blank=True
    )
    cneh_code = models.ForeignKey('Cnehs', on_delete=models.PROTECT, null=True, blank=True)
    classe_code = models.ForeignKey(
        'ClasseCode',
        on_delete=models.PROTECT,
        verbose_name="Classification du DM",
        null=True,
        blank=True,
    )
    date_obsolescence = models.DateField(verbose_name="date d'obsolescence", null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    cloture = models.DateField(verbose_name='date de fin', null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification')
    id_gmao = models.CharField(max_length=300, null=True, blank=True, verbose_name='ID de la GMAO')

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.

    def __str__(self):
        return "{0} - {1}".format(self.type, self.marque)


class Cneh(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=90, default=None, verbose_name="Code CNEH", blank=False, null=False)
    intitule = models.CharField(max_length=90, default=None, verbose_name="Nom du CNEH", blank=False, null=False)
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    cloture = models.DateField(verbose_name='date de fin', null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification')

    def __str__(self):
        return "{0} - {1}".format(self.code, self.intitule)


class Cnehs(models.Model):  # Table pour complément des codes CNEH
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=90, default=None, blank=False, null=False)
    intitule = models.CharField(max_length=90, default=None, blank=False, null=False)
    code_cneh = models.ForeignKey('Cneh', default=None, blank=False, null=False, on_delete=models.PROTECT)
    # nomenclature_achat = models.ForeignKey( #  TODO: Voir si utile et pertinent de faire un lien ici
    #    'marché.nomenclature_achat',
    #    default=None,
    #    blank=True,
    #    null=True,
    #    on_delete=models.PROTECT)
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    cloture = models.DateField(verbose_name='date de fin', null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification')

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.

    def __str__(self):
        return "{0} - {1}".format(self.code, self.intitule)


class Role(models.Model):
    """
    Ce modèle décrit la liste des rôles utilisés dans cette instance de BIOM_AID.

    Cela comporte aussi bien les rôles "système" que les rôles applicatifs ou les rôles ad-hoc.
    """

    code = models.CharField(max_length=8)
    label = models.CharField(max_length=256, null=True, blank=True)
    note = models.TextField(null=True, blank=True)


class UserUfRole(models.Model):
    """
    Ce modèle sert à déterminer la portée d'un rôle pour un utilisateur (il pourrait donc s'intituler "UserRoleScope")

    Le principe, c'est qu'un utilisateur a, pour chacun des rôles qu'il exerce, une ou plusieurs instances de cette
    table pour définir quelle est la portée de ce rôle. C'est à dire, dans quels contextes ce rôle est valide.

    Ainsi, un chef de pôle n'aura ce rôle que dans son propre pôle (il ne pourra pas valider les demandes des autres pôles) et
    un expert peut n'être expert que dans un domaine ou une discipline et seulement sur un établissement. De la même façon,
    un arbitre peut n'être légitime que sur certains établissements / domaines / programmes.

    Dans certains cas, la portée d'un rôle est implicite et n'a pas besoin d'être représentée dans ce modèle :
    - Les administrateurs système 'ADM' (et plus généralement, tous les rôles qui ont une portée sur l'ensemble de l'application)
      sont définis dans Django directement
    - Le propriétaire d'une demande (rôle 'OWN') est le rédacteur de la demande.
    - L'arbitre pour un programme (rôle 'ARB') est défini dans le champs 'arbitre' de chaque programme.
    - Le dispatcher pour une campagne de recensement (rôle 'DIS') est défini dans le champs 'dispatcher' de chaque campagne

    Lorsqu'il y a plusieurs instances avec le même utilisateur et le même rôle, il faut considérer comme portée l'union
    (l'addition) des portées. Ainsi, un cadre qui est responsable de deux services aura deux fiches (chacune avec son service)
    et pourra créer des demandes dans l'application pour ces deux services.

    Dans cette version, la portée est définie sur 2 'axes', la structure et le domaine (technique) :
    - Pour la structure, il est possible de préciser pour chaque enregistrement :
      - l'UF *ou*
      - le service *ou*
      - le centre de responsabilité *ou*
      - le pôle *ou*
      - le site *ou*
      - l'établissement.
      Les champs non utilisés devant rester NULL.
      Si tous ces champs sont NULL, la portée sur cet axe couvre toutes les structures.
    - Pour le domaine technique, il est possible de préciser pour chaque enregistrement :
      - la discipline *ou*
      - le préfixe du domaine (plus précisement du code du domaine). Ainsi, si la valeur est '5', la portée du rôle
        (probablement de l'expertise) sera sur toute l'imagerie médicale (tous les codes qui commencent par '5'),
        alors que si c'est '506', cela ne sera valable que pour l'imagerie par ultrason.
      Si ces 2 champs sont NULL, la portée sur cet axe couvre tous les domaines.
    """

    class Meta:
        verbose_name = _("rôle")
        unique_together = (('user', 'uf', 'role_code'),)
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['uf']),
            models.Index(fields=['service']),
            models.Index(fields=['centre_responsabilite']),
            models.Index(fields=['pole']),
            models.Index(fields=['site']),
            models.Index(fields=['etablissement']),
            models.Index(fields=['discipline']),
            models.Index(fields=['domaine_prefix']),
            models.Index(fields=['role_code']),
        ]

    NAME_CHOICES = (
        ('CHP', _("Chef de pôle")),
        ('ADCP', _("Adjoint au chef de pôle")),
        ('CHS', _("Chef de service")),
        ('RUN', _("Responsable d'unité")),
        ('CSP', _("Cadre supérieur de pôle")),
        ('DRP', _("Directeur référent de pôle")),
        ('CAP', _("Cadre administratif de pôle")),
        ('AMAR', _("Assistant médico-administratif référent")),
        ('CADS', _("Cadre supérieur")),
        ('CAD', _("Cadre")),
        ('COP', _("Coordonateur de pôle")),
        ('DIR', _("Directeur adjoint")),
        ('RMA', _("Référent matériel")),
        ('ACH', _("Acheteur")),
        ('EXP', _("Expert métier")),
        ('RESPD', _("Responsable de domaine technique")),
        ('INGTX', _("Ingénieur travaux")),
        ('GES', _("Gestionnaire")),
        ('TECH', _("Technicien")),
    )

    # extension_user = models.ForeignKey(ExtensionUser, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    uf = models.ForeignKey(Uf, null=True, blank=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.CASCADE)
    centre_responsabilite = models.ForeignKey(CentreResponsabilite, null=True, blank=True, on_delete=models.CASCADE)
    pole = models.ForeignKey(Pole, null=True, blank=True, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.CASCADE)
    etablissement = models.ForeignKey(Etablissement, null=True, blank=True, on_delete=models.CASCADE)

    discipline = models.ForeignKey(Discipline, null=True, blank=True, on_delete=models.CASCADE)
    domaine_prefix = models.CharField(max_length=16, null=True, blank=True)

    role_code = models.CharField(max_length=8, choices=NAME_CHOICES)

    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("date de création"),
    )
    cloture = models.DateTimeField(
        verbose_name=_("date de fin"),
        null=True,
        blank=True,
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date de modification"),
    )

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.

    def __str__(self):
        return "{0}  est  {1}  pour  {2}".format(
            self.user,
            self.role_code,
            self.uf or self.service or self.centre_responsabilite or self.pole or self.site or self.etablissement,
        )


class LastUpdate(models.Model):

    id = models.AutoField(primary_key=True)
    table_in = models.CharField(
        verbose_name=_("Table BIOM_AID"),
        help_text=_("Table BIOM_AID impactée par l'update"),
        max_length=256,
        null=True,
        blank=True,
    )
    date_last_update = models.DateTimeField(
        verbose_name=_("date dernier update"),
        help_text=_("date de l'update"),
        null=True,
        blank=True,
    )

    def __str__(self):
        return "{0} - {1}".format(self.table_in, self.date_last_update)


class Alert(models.Model):
    class Meta:
        verbose_name = _("Alerte")

    id = models.AutoField(primary_key=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=64, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    niveau = models.IntegerField(
        null=False,
        blank=False,
    )
    intitule = models.CharField(
        verbose_name=_("Intitulé"),
        help_text=_("Description de l'alerte"),
        max_length=4096,
        null=True,
        blank=True,
    )
    categorie = models.CharField(
        verbose_name=_("Catégorie"),
        help_text=_("Catégorie de l'alerte"),
        max_length=256,
        null=True,
        blank=True,
    )
    donnees = models.TextField(
        null=True,
        blank=True,
        default=None,
    )  # données (paramètres) de l'arlerte, encodées en JSON
    lien = models.CharField(
        max_length=4096,
        null=True,
        blank=True,
        default=None,
    )  # lien vers la page permettant de traiter l'alerte
    # destinataire_ext = models.ForeignKey(
    #     ExtensionUser,
    #     default=79,  # Juste pour éviter de bloquer lors de la migration. Ne pas utiliser !
    #     on_delete=models.PROTECT,
    # )
    destinataire = models.ForeignKey(
        User,
        db_column='destinataire_new',
        default=79,  # Juste pour éviter de bloquer lors de la migration. Ne pas utiliser !
        on_delete=models.PROTECT,
    )
    commentaire = models.TextField(
        null=True,
        blank=True,
        default=None,
    )  # commentaires si nécessaire
    etat = models.CharField(
        verbose_name=_("Etat"),
        help_text=_("Etat de l'alerte"),
        max_length=256,
        null=True,
        blank=True,
    )
    historique = models.TextField(
        null=True,
        blank=True,
        default=None,
    )  # commentaires si nécessaire
    date_activation = models.DateTimeField(
        verbose_name=_("date de dernière activation"),
    )
    date_lecture = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("date de lecture"),
    )
    dernier_email = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("date d'envoi dernier email"),
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("date de création"),
    )
    cloture = models.DateTimeField(
        verbose_name=_("date de fin"),
        null=True,
        blank=True,
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date de modification"),
    )

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.


class GenericRole(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['cloture'], name='gen_role_end_idx'),
            models.Index(fields=['role_code'], name='gen_role_code_idx'),
            models.Index(fields=['content_type', 'object_id'], name='gen_role_ref_idx'),
        ]

    user: models.ForeignKey = models.ForeignKey(
        config.settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("User that benefit this specific role on linked object"),
    )

    creator: models.ForeignKey = models.ForeignKey(
        config.settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("User that created this link"),
        related_name='created_role',
        null=True,
    )

    creation_datetime: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    modification_datetime: models.DateTimeField = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))
    cloture: models.DateTimeField = models.DateTimeField(null=True, blank=True)

    content_type: models.ForeignKey = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id: models.CharField = models.CharField(max_length=64)
    content_object = GenericForeignKey('content_type', 'object_id')
    role_code: models.CharField = models.CharField(
        max_length=8,
        choices=tuple(
            list(UserUfRole.NAME_CHOICES)
            + [
                ('ADM', _("Administrateur")),
                ('OWN', _("Propriétaire")),
                ('MAN', _("Manager")),
                ('ARB', _("Arbitre")),
                ('DIS', _("Aiguilleur")),
            ]
        ),
    )

    objects = models.Manager()  # The default manager.
    active_objects = ActiveManagerCloture()  # The active_objects manager.

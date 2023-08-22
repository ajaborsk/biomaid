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
# import pytz
# from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext as _

from generic_comment.models import GenericComment
from document.models import GenericDocument


class Marche(models.Model):
    """
    Liste des marchés disponible
    """

    id = models.AutoField(primary_key=True)
    num_marche = models.CharField(
        unique=True,
        blank=True,
        null=True,
        max_length=200,
        help_text=_("Numéro du marché tel que défini par le pouvoir adjudicateur"),
    )
    intitule = models.TextField(
        verbose_name=_("Intitulé"),
        help_text=_("Intitulé du marché (généralement le titre de la procédure qui a conduit à ce marché)"),
    )
    type_procedure = models.ForeignKey(
        'TypeProcedure',
        on_delete=models.PROTECT,
        verbose_name=_("Type de procédure/marché"),
    )
    procedure = models.ForeignKey(
        'Procedure',
        on_delete=models.PROTECT,
        verbose_name=_("Procédure"),
        help_text=_("Procédure ayant conduit à ce marché"),
        null=True,
        blank=True,
        default=None,
    )
    date_notif = models.DateField(  # date de notification
        verbose_name=_("Notification"),
        help_text=_("Date de notification du marché"),
        null=True,
        blank=True,
        default=None,
    )
    date_debut = models.DateField(  # date de début
        verbose_name=_("Début"),
        help_text=_("Date de début d'exécution du marché"),
        null=True,
        blank=True,
        default=None,
    )
    duree = models.IntegerField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Durée en mois"),
    )  # durée du marche en mois
    lots = models.ManyToManyField(
        'Lot',
        blank=True,
        default=None,
    )
    acheteur = models.ForeignKey(  # acheteur en charge du dossier
        get_user_model(),
        related_name='acheteur',
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
    )
    expert_metier = models.ForeignKey(  # expert métier en charge du dossier
        get_user_model(),
        related_name='marche_comme_expert_metier',
        verbose_name=_("Expert métier"),
        help_text=_("Expert métier référent de l'exécution de ce marché"),
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
    )
    # expert_metier_ext = models.ForeignKey(  # expert métier en charge du dossier
    #     ExtensionUser,
    #     related_name='marche_comme_expert_metier_ext',
    #     verbose_name=_("Expert métier"),
    #     help_text=_("Expert métier référent de l'exécution de ce marché"),
    #     null=True,
    #     blank=True,
    #     default=None,
    #     on_delete=models.PROTECT,
    # )
    commentaire = models.TextField(
        null=True,
        blank=True,
        default=None,
    )
    cloture = models.DateField(
        null=True,
        blank=True,
    )

    # Generic fields
    comments = GenericRelation(GenericComment, related_query_name='marche')
    documents_generic = GenericRelation(GenericDocument, related_query_name='marche')

    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    date_modification = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))

    def __str__(self):
        return "{0} - {1}".format(self.num_marche, self.intitule)


# type de procédure disponible dans le CMP
class TypeProcedure(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200)  # 30-1-3, AO, MAPA, UGAP, UNIHA, RESAH...
    intitule = models.TextField(
        default=None,
        blank=False,
        null=False,
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    date_modification = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))
    date_suppression = models.DateTimeField(auto_now=True, verbose_name=_("date de suppression"))

    def __str__(self):
        return "{0} - {1}".format(self.code, self.intitule)


class Procedure(models.Model):
    """Procédure de marché public"""

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200)  # 30-1-3, AO, MAPA, UGAP, UNIHA, RESAH...
    intitule = models.TextField(
        default=None,
        blank=False,
        null=False,
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    date_modification = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))
    date_suppression = models.DateTimeField(auto_now=True, verbose_name=_("date de suppression"))

    def __str__(self):
        return "{0} - {1}".format(self.code, self.intitule)


class Lot(models.Model):
    RECONDUCTION_CHOICES = (
        ('Tacite', 'TACITE'),
        ('Expresse', 'EXPRESSE'),
    )
    FACTURATION_CHOICES = (
        ('Forfaitaire', 'FORFAITAIRE'),
        ('Unitaire', 'UNITAIRE'),
    )

    id = models.AutoField(primary_key=True)
    code = models.IntegerField()
    intitule = models.TextField()
    code_four = models.ForeignKey('common.Fournisseur', on_delete=models.PROTECT)
    commentaire = models.TextField()
    montant_mini = models.DecimalField(max_digits=20, decimal_places=0, default=None, blank=False, null=False)
    sans_mini = models.BooleanField()
    montant_maxi = models.DecimalField(max_digits=20, decimal_places=0, default=None, blank=False, null=False)
    sans_maxi = models.BooleanField()
    quantite_mini = models.DecimalField(max_digits=20, decimal_places=0, default=None, blank=False, null=False)
    quantite_maxi = models.DecimalField(max_digits=20, decimal_places=0, default=None, blank=False, null=False)
    # possibilités du marché
    acquisition = models.BooleanField()
    maintenance = models.BooleanField()
    accessoires = models.BooleanField()
    consommables = models.BooleanField()
    date_notif = models.DateField()  # date de notification du lot
    date_debut = models.DateField()  # date de début du lot
    duree = models.IntegerField()  # durée du lot en mois
    type_reconduction = models.CharField(choices=RECONDUCTION_CHOICES, max_length=200)
    type_facturation = models.CharField(choices=FACTURATION_CHOICES, max_length=200)
    cloture = models.DateField()
    etablissements = models.ManyToManyField(
        'common.Etablissement',
    )
    # documents = models.ManyToManyField('Document', blank=True, through="DocumentLink")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    date_modification = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))

    def __str__(self):
        return "{0} - {1}".format(self.code, self.intitule)


class FamilleAchat(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.IntegerField()

    def __str__(self):
        return "{0}".format(self.code)


class Suivi(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.IntegerField()

    def __str__(self):
        return "{0}".format(self.code)


"""
Code Type de HM
    - Description détaillée
    - Tâches à faire / vérifications
HM1	Procédure en cours
    - Une procédure (appel d’offres, recours à une centrale, etc.) est lancée (ie figure dans le tableau de la DAGHT)
     mais n’a pas encore abouti (pas de marché notifié à ce jour). Ce HM disparaîtra donc rapidement.
    - Eventuellement vérifier que la commande est bien dans le périmètre de la procédure en cours
     et/ou faire ajuster ce périmètre si c’est encore possible.
HM2	Procédure à prévoir
    - Il n’existe pas de marché ni de procédure en cours pour ce besoin mais cela semblerait
     pourtant pertinent (besoin récurrent et/ou montants suffisamment importants).
    - Préciser et faire faire un recensement des besoins (éventuellement au niveau du GHT)
     et préparer une procédure avec la DAGHT (à formaliser).
HM3	HM résiduel
    - Ce type de commande est, pour l’instant, jugé trop rare (même s’il peut être récurrent)
     et d’un montant trop faible pour justifier l’effort d’une procédure.
    - Surveiller le nombre et le montant de ces HM3 (par famille et par fournisseur)
HM4	HM ponctuel
    - Il s’agit d’une commande exceptionnelle (par exemple une offre commerciale)
     qui n’a pas vocation à se répéter dans les années à venir.
    - Surveiller le nombre et le montant de ces HM4 (par famille et par fournisseur)
HM5	Avenant en cours
    - Un avenant est en cours (ie figure dans le tableau de la DAGHT) mais n’a pas encore abouti. Ce HM disparaîtra donc rapidement
    - Eventuellement vérifier que la commande est bien dans le périmètre de l’avenant en cours
     et/ou faire ajuster ce périmètre si c’est encore possible.
HM6	Avenant à prévoir
    - Il existe un marché valide qui peut, par voie d’avenant, intégrer ce besoin.
    - Faire une demande d’avenant à la DAGHT pour intégrer ce besoin dans le marché existant. En profiter pour
      voir s’il est possible d’englober d’autres besoins (HM3, HM4 ou autres HM6)
"""


class ExceptionMarche(models.Model):

    CODE_HM_CHOICES = (
        ('HM1', 'HM1 - Procédure en cours'),
        ('HM2', 'HM2 - Procédure à prévoir'),
        ('HM3', 'HM3 - HM résiduel'),
        ('HM4', 'HM4 - HM ponctuel'),
        ('HM5', 'HM5 - Avenant en cours'),
        ('HM6', 'HM6 - Avenant à prévoir'),
    )

    code_hm = models.CharField(
        verbose_name=_("Code HM"),
        help_text=_("Code à saisir dans le champ 'objet de la dépense' de la commande"),
        choices=CODE_HM_CHOICES,
        max_length=8,
    )
    prefixe_compte = models.CharField(
        verbose_name=_("Préfixe compte"),
        help_text=_("Préfixe (sans la lettre) des comptes pour lesquels l'exception est valide"),
        max_length=12,
    )
    description = models.CharField(
        verbose_name=_("Description"),
        help_text=_("Description (facultative) de l'exception"),
        max_length=1024,
        blank=True,
        null=True,
    )
    code_fournisseur = models.IntegerField(
        verbose_name=_("Code fournisseur"), help_text=_("Code (magh2) du fournisseur pour lequel l'exception est valide")
    )

    date_debut = models.DateField(verbose_name=_("Date de début"), help_text=_("Date de début de validité de l'exception"))
    date_fin = models.DateField(
        verbose_name=_("Date de fin"), help_text=_("Date de fin de validité de l'exception (facultatif)"), null=True, blank=True
    )

    no_marche = models.CharField(
        max_length=12,
        verbose_name=_("N° de marché à utiliser"),
        help_text=_("Numéro de marché à utiliser après la fin de la validité de l'exception"),
        null=True,
        blank=True,
    )

    # Generic fields
    comments = GenericRelation(GenericComment, related_query_name='exception_marche')

    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    date_modification = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))

    def __str__(self):
        return "{0}".format(self.code)


# class Document(models.Model):
#
#     DOCS_CHOICES = (
#         ('DEVIS', 'Devis'),
#         ('DC1', 'DC1'),
#         ('DC2', 'DC2'),
#         ('CCTP', 'cahier des charges'),
#         ('CCAP', 'Cahier des Clauses Administratives particulière'),
#         ('AVENANT', 'Avenant'),
#         ('COURRIER', 'Courrier'),
#         ('RC', 'Réglement de Consultation'),
#         ('PLAN', 'Planning'),
#         ('BP', 'Business Plan'),
#         ('DI', 'Autre'),
#     )
#     code = models.CharField(  # type de document
#         max_length=10,
#         choices=DOCS_CHOICES,
#         blank=True,
#         verbose_name=_("Type"),
#         help_text=_("Choisissez le type du document à joindre"),
#     )
#     UNCpath = models.FileField(  # chemin d'enregistrement
#         max_length=255,
#         blank=True,
#         verbose_name=_("Fichier"),
#         help_text=_("Sélectionnez dans vos dossiers le fichier à ajouter"),
#     )
#     commentaire = models.CharField(  # commentaire laissé par l'utilisateur
#         max_length=120,
#         blank=True,
#         verbose_name=_("Note"),
#         help_text=_("Vous pouvez y intégrer un commentaire pour décrire le document"),
#     )
#     status = models.BooleanField(default=False)  # Status fichier utilisé ou non
#     createur = models.CharField(max_length=255, blank=True, null=True)
#     date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
#     date_modification = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))
#
#     class Meta:
#         verbose_name = _("document joint")
#         verbose_name_plural = _("documents joints")
#
#     def __str__(self):
#         return "{0} {1}".format(self.code, self.UNCpath)
#
#     def get_absolute_url(self):
#         return reverse('doc:document', kwargs={'UNCpath': self.UNCpath})
#
#
# class DocumentLink(models.Model):
#     class Meta:
#         indexes = [
#             models.Index(fields=['document']),
#             models.Index(fields=['lot']),
#         ]
#
#     document = models.ForeignKey(
#         "Document",
#         on_delete=models.PROTECT,
#     )
#     lot = models.ForeignKey(
#         "Lot",
#         on_delete=models.PROTECT,
#     )
#
#     def __str__(self):
#         return "{0} {1}".format(self.document, self.lot)

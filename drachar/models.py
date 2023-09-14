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
# Models pour l'execution du plan d'investissement et pour son suivi
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from common import config

# Create your models here.

# Models récupéré mas
# dans d'autres applications :
""" /common/Programme
    /common/Uf, Pole, (structure)
    /common/Fournisseurs # à compléter/finaliser
    /common/Compte
    /common/Modele_Type # a créer qui récupère les données sur la GMAO
    /common/Marque # a créer qui récupère les données sur la GMAO
    --------------
    /marche/marche # à créer
    /marche/FamilleAchat # à créer
    /marche/cneh # a créer qui récupère les données sur la GMAO
    --------------
    /dem/ = Script qui récupère le previsionnel
    --------------
"""

from overoly.base import OverolyModel as OModel


class Previsionnel(OModel):
    # id = models.AutoField()
    num = models.AutoField(primary_key=True)  # numero de demande validée
    uf = models.ForeignKey(
        'common.Uf',
        verbose_name=_("UF bénéficiaire"),
        null=False,
        on_delete=models.PROTECT,
    )
    programme = models.ForeignKey(  # numéro du programme d'affectation
        'common.Programme',
        verbose_name="Numéro de programme",
        default=None,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
    )
    num_dmd = models.ForeignKey(  # numéro de la demande correspondante
        'dem.Demande',
        verbose_name="Numéro de la demande",
        default=None,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
    )
    solder_ligne = models.BooleanField(  # solder la ligne prévisionnelle si demande honorée
        verbose_name="Solder la ligne du prévisionnel",
        help_text="cocher la case s'il n'y a pas d'autre achat sur cette ligne de demande.",
        default=False,
        null=False,
    )
    budget = models.DecimalField(
        verbose_name="Budget alloué à la demande",
        help_text="Budget alloué à la demande par la commission.",
        max_digits=9,
        decimal_places=0,
        default=None,
        blank=True,
        null=True,
    )
    expert = models.ForeignKey(
        get_user_model(),
        db_column='expert_user',
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
    )
    # expert_ext = models.ForeignKey(ExtensionUser, null=True, blank=True, default=None, on_delete=models.CASCADE)
    commentaire = models.TextField(
        verbose_name="Commentaire privé",
        help_text="Commentaire qui ne sera affiché qu'aux experts/acheteurs",
        blank=True,
        null=True,
    )
    # workflow =
    # ------------------------------------------------------------------------------------------------------------------
    # Cette partie (ci-dessous) est provisoire en attendant la fin de l'implémentation complète de DRACHAR
    # Elle permet le suivi du prévisionnel "à la main" comme dans la version Excel
    # ------------------------------------------------------------------------------------------------------------------

    # ligne_dra94 = models.IntegerField(
    #     verbose_name=_("Ligne"),
    #     help_text=_("Numéro de ligne dans DRA94 : Utilisé pour faire le lien automatique avec
    #                 DRA94 (suivi financier, notamment)"),
    #     null=True,
    #     blank=True,
    # )
    commentaire_public = models.TextField(
        verbose_name="Commentaire public",
        help_text="Commentaire qui sera affiché aussi à l'utilisateur / le demandeur",
        blank=True,
        null=True,
    )
    suivi_besoin = models.TextField(
        verbose_name=_("Définition du Besoin"),
        help_text=_("Idem case équivalente dans le tableau de suivi (notamment pour la gestion du préfixe)"),
        null=True,
        blank=True,
    )
    suivi_achat = models.TextField(
        verbose_name=_("Marché"),
        help_text=_("Idem case équivalente dans le tableau de suivi (notamment pour la gestion du préfixe)"),
        null=True,
        blank=True,
    )
    suivi_offre = models.TextField(
        verbose_name=_("Devis"),
        help_text=_("Idem case équivalente dans le tableau de suivi (notamment pour la gestion du préfixe)"),
        null=True,
        blank=True,
    )
    suivi_appro = models.TextField(
        verbose_name=_("Commande"),
        help_text=_("Idem case équivalente dans le tableau de suivi (notamment pour la gestion du préfixe)"),
        null=True,
        blank=True,
    )
    suivi_mes = models.TextField(
        verbose_name=_("Mise en service"),
        help_text=_("Idem case équivalente dans le tableau de suivi (notamment pour la gestion du préfixe)"),
        null=True,
        blank=True,
    )
    montant_estime = models.DecimalField(
        verbose_name="Montant estimé",
        help_text="Meilleure estimation du montant total : Soit l'enveloppe,"
        " soit une réévaluation de l'enveloppe après précision du besoin, soit montant total commandé",
        max_digits=9,
        decimal_places=0,
        default=None,
        blank=True,
        null=True,
    )
    montant_commande = models.DecimalField(
        verbose_name="Montant commandé",
        help_text="Montant total commandé sur cette ligne de prévisionnel",
        max_digits=11,
        decimal_places=2,
        default=None,
        blank=True,
        null=True,
    )
    date_debut = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Prise en charge"),
        help_text=_("Date de début du traitement du dossier"),
    )

    # -----------------------------------------------------------------------------------------------------------------------------
    #
    # Champs remplis automatiquement (il y a aussi le champs 'interface' plus haut)
    #
    # -----------------------------------------------------------------------------------------------------------------------------

    nombre_commandes = models.IntegerField(
        verbose_name="Nombre de commandes",
        help_text="Nombre de commandes sur cette ligne de prévisionnel (détecté automatiquement)",
        default=None,
        blank=True,
        null=True,
    )

    nombre_lignes_commandes = models.IntegerField(
        verbose_name="Nombre de lignes de commande",
        help_text="Nombre de lignes de commande sur cette ligne de prévisionnel (détecté automatiquement)",
        default=None,
        blank=True,
        null=True,
    )

    montant_engage = models.DecimalField(
        verbose_name="Montant engagé",
        help_text="Montant total engagé sur cette ligne de prévisionnel (détecté automatiquement)",
        max_digits=11,
        decimal_places=2,
        default=None,
        blank=True,
        null=True,
    )

    montant_liquide = models.DecimalField(
        verbose_name="Montant liquidé",
        help_text="Montant total liquidé sur cette ligne de prévisionnel (détecté automatiquement)",
        max_digits=11,
        decimal_places=2,
        default=None,
        blank=True,
        null=True,
    )

    nombre_equipements = models.IntegerField(
        verbose_name="Nombre équipements",
        help_text="Montant total des équipements inventoriés sur cette ligne de prévisionnel (détecté automatiquement)",
        default=None,
        blank=True,
        null=True,
    )

    valeur_inventaire = models.DecimalField(
        verbose_name="Montant inventaire",
        help_text="Montant total des équipements inventoriés sur cette ligne de prévisionnel (détecté automatiquement)",
        max_digits=11,
        decimal_places=2,
        default=None,
        blank=True,
        null=True,
    )

    interface = models.TextField(
        verbose_name=_("Interface avec les autres logiciels (DRA94, magh2, Asset+, ...)"),
        blank=True,
        null=True,
    )
    analyse = models.JSONField(
        verbose_name=_("Analyse technique du prévisionnel (détecté automatiquement)"),
        default=None,
        blank=True,
        null=True,
    )

    # -  Partie dédiée au suivi des travaux ---------------------------------------------------------------------------------------

    # programme = Utilise le champs "suivi_besoin" avec un autre titre

    # Etude du besoin/programme (plan, descriptif...)
    suivi_etude = models.TextField(
        verbose_name=_("Etude"),
        help_text=_("Idem case équivalente dans le tableau de suivi (notamment pour la gestion du préfixe)"),
        null=True,
        blank=True,
    )

    # Délai d'autorisation administrative (typiquement permis de construire, dossier d'aménagement...)
    suivi_autorisation = models.TextField(
        verbose_name=_("Autorisation"),
        help_text=_("Idem case équivalente dans le tableau de suivi (notamment pour la gestion du préfixe)"),
        null=True,
        blank=True,
    )

    # préparation  chantier /
    # L'opération est lancée mais des opérations préalables sont nécessaires et en cours
    suivi_preparation = models.TextField(
        verbose_name=_("Préparation"),
        help_text=_("Idem case équivalente dans le tableau de suivi (notamment pour la gestion du préfixe)"),
        null=True,
        blank=True,
    )

    #
    #
    # L'opération est en cours d'exécution (=livraison ou exécution des travaux)
    suivi_execution = models.TextField(
        verbose_name=_("Exécution"),
        help_text=_("Idem case équivalente dans le tableau de suivi (notamment pour la gestion du préfixe)"),
        null=True,
        blank=True,
    )

    # Suivi de la réception de l'opération (utilisé pour les travaux) : L'opération est techniquement terminée,
    #   mais vérifications en cours
    suivi_reception = models.TextField(
        verbose_name=_("Réception"),
        help_text=_("Idem case équivalente dans le tableau de suivi (notamment pour la gestion du préfixe)"),
        null=True,
        blank=True,
    )

    #
    # terminé => Utiliser le champ 'mes' en changeant l'étiquette

    # -----------------------------------------------------------------------------------------------------------------------------

    date_estimative_mes = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Estimation MES"),
        help_text=_("Date estimative de mise en service"),
    )

    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    date_modification = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))

    def __str__(self):
        return "{0} - {1}".format(self.num, self.num_dmd)


class Dra(OModel):
    num_dra = models.AutoField(primary_key=True)  # numero de la demande de réalisation d'achat
    intitule = models.TextField(
        default=None,
        blank=False,
        null=False,
    )
    fournisseur = models.ForeignKey(
        'common.Fournisseur',
        default=None,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
    )
    contact_fournisseur = models.ForeignKey(
        'common.ContactFournisseur',
        default=None,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    num_devis = models.CharField(
        max_length=120,
        default=None,
        blank=False,
        null=False,
        verbose_name='N° devis',
    )
    date_devis = models.DateField(blank=False, null=False, default=None, verbose_name='date du devis')
    num_marche = models.ForeignKey(
        'marche.Marche',
        default=0,  # #0 qui sera le Hors marché
        blank=False,
        null=False,
        verbose_name='Marché utilisé',
        on_delete=models.PROTECT,
    )
    expert_metier = models.ForeignKey(  # acheteur ou expert métier en charge de la dra
        get_user_model(),
        db_column='expert',
        related_name='dra_comme_expert',
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
    )
    # numero du marché utilisé
    # expert_metier_ext = models.ForeignKey(  # acheteur ou expert métier en charge de la dra
    #     ExtensionUser, db_column='expert_old',
    #           related_name='dra_comme_expert_ext', null=True, blank=True, default=None, on_delete=models.CASCADE
    # )
    num_bon_commande = models.CharField(  # numero de commande Magh2
        max_length=120,
        default=None,
        blank=True,
        null=True,
        verbose_name='N° commande',
    )
    num_dossier = models.ForeignKey(
        'Dossier',
        null=True,
        blank=True,
        verbose_name='Dossier de travail',
        on_delete=models.PROTECT,
    )
    # documents = models.ManyToManyField('dem.Document', blank=True, through="DocumentDracharLink")
    date_commande = models.DateField(  # date de commande Magh2
        null=True,
        blank=True,
        verbose_name='date de commande',
    )
    contact_livraison = models.ForeignKey(
        'ContactLivraison',
        null=False,
        blank=False,
        verbose_name='contact pour la livraison',
        on_delete=models.PROTECT,
    )
    # montant_dra = models.DecimalField()  # A garder ou à supprimer = somme des lignes...
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    date_modification = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))

    def __str__(self):
        return "{0} - {1}".format(self.num_dra, self.fournisseur)


# class DocumentDracharLink(Model):
#     class Meta:
#         indexes = [
#             models.Index(fields=['document']),
#             models.Index(fields=['dra']),
#         ]
#
#     document = models.ForeignKey(
#         "dem.Document",
#         on_delete=models.PROTECT,
#     )
#     dra = models.ForeignKey(
#         "Dra",
#         on_delete=models.PROTECT,
#     )
#
#     def __str__(self):
#         return "{0} {1}".format(self.document, self.dra)


class ContactLivraison(OModel):
    code = models.CharField(max_length=50, blank=True, null=True, help_text="Champs automatique")
    nom = models.CharField(
        verbose_name="Nom contact livraison",
        max_length=50,
        default=None,
        blank=False,
        null=False,
        help_text="Nom Contact pour la livraison",
    )
    prenom = models.CharField(
        verbose_name="Prénom contact livraison",
        max_length=50,
        default=None,
        blank=False,
        null=False,
        help_text="Prénom Contact pour la livraison",
    )
    coordonnees = models.DecimalField(
        verbose_name="Telephone du contact",
        help_text="Numéro à appeler si nécessaire pour la livraison",
        max_digits=10,
        decimal_places=0,
        default=None,
        blank=True,
        null=True,
    )
    etablissement = models.ForeignKey(
        'common.Etablissement',
        blank=False,
        null=False,
        verbose_name="Etablissement d'affiliation",
        on_delete=models.PROTECT,
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    date_modification = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))
    cloture = models.DateField(verbose_name='date de fin', null=True, blank=True)

    def __str__(self):
        return "{0} - {1} - {2}".format(self.code, self.nom, self.prenom)


class LigneCommande(OModel):
    CLASSE_EQT = (
        ('1', '1'),
        ('2A', '2A'),
        ('2B', '2B'),
        ('3', '3'),
    )
    TVA = (('20%', '0.2'),)
    REFORME_MUTATION = (
        ('NON', 'NON'),
        ('REFORME', 'REFORME'),
        ('MUTATION', 'MUTATION'),
    )

    num_ligne = models.AutoField(primary_key=True)
    num_previsionnel = models.ForeignKey(  # numero de la ligne de demande du previsionnel
        'Previsionnel',
        default=None,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
    )
    num_dra = models.ForeignKey(
        'Dra',
        default=None,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
    )
    famille_achat = models.ForeignKey(
        'marche.FamilleAchat',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    num_compte = models.ForeignKey(
        'common.Compte',
        verbose_name="Numéro de compte",
        default=None,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
    )
    a_inventorier = models.BooleanField(
        verbose_name="Appareil à inventorier ?",
        help_text="cocher la case s'il faut créer un inventaire pour les équipements de cette ligne.",
        null=True,
    )
    classe = models.CharField(
        max_length=90,
        choices=CLASSE_EQT,
    )
    cneh = models.ForeignKey(
        'common.Cnehs',
        verbose_name="code Cneh du produit commandé",
        on_delete=models.PROTECT,
    )
    modele = models.CharField(
        verbose_name="Type/Modèle",
        max_length=120,
        default=None,
        blank=True,
        null=True,
        help_text="Type/Modèle de l'appareil",
    )  # créer des FK vers table auto depuis GMAO
    marque = models.CharField(
        verbose_name="Marque",
        max_length=120,
        default=None,
        blank=True,
        null=True,
        help_text="Marque de l'appareil",
    )  # créer des FK vers table auto depuis GMAO
    reference = models.CharField(
        verbose_name="référence",
        max_length=90,
        default=None,
        blank=True,
        null=True,
        help_text="référence fournisseur",
    )
    descriptif = models.TextField(
        verbose_name="référence",
        default=None,
        blank=True,
        null=True,
        help_text="Descritif du produit",
    )
    prix_unitaire_ht = models.DecimalField(max_digits=15, decimal_places=2, default=None, blank=False, null=False)
    tva = models.CharField(
        choices=TVA,
        max_length=15,
        blank=False,
        null=False,
    )
    # prix_unitaire_ttc=models.DecimalField()  # à supprimer ?
    # gain_achat=models.DecimalField()  # mettre à supprimer ?
    ref_mut = models.CharField(
        choices=REFORME_MUTATION,
        max_length=15,
        blank=False,
        null=False,
    )
    eqpt_recup = models.CharField(  # numéro de l'équipement récupéré
        verbose_name="N° inventaire",
        max_length=90,
        default=None,
        blank=True,
        null=True,
        help_text="N° inventaire de l'équipemetn récupéré",
    )
    pv_reforme = models.CharField(  # numero du PV de réforme dans asset+
        verbose_name="N° PV de réforme",
        max_length=90,
        default=None,
        blank=True,
        null=True,
        help_text="N° PV de réforme",
    )
    # formation_tech = models.BooleanField()  # à conserver ?
    # visite_fin_garantie = models.BooleanField()  # à conserver ?
    garantie = models.DecimalField(  # durée en mois de la garantie
        max_digits=10,
        decimal_places=0,
        blank=False,
        null=False,
    )
    # garantie_onsite=models.BooleanField() #à conserver ?
    date_reception = models.DateField(  # date de livraison
        null=True,
        blank=True,
        verbose_name='date de livraison',
    )
    date_mes = models.DateField(  # date de la mise en service
        null=True,
        blank=True,
        verbose_name='date de mise en service',
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    date_modification = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))

    def __str__(self):
        return "{0} - {1}".format(self.num_ligne, self.num_previsionnel)


class Dossier(OModel):
    PRIO_CHOICES = (
        ('1', 'Haute'),
        ('2', 'Normale'),
        ('3', 'Basse'),
    )

    num_dossier = models.AutoField(primary_key=True)
    nom_dossier = models.TextField(
        default=None,
        blank=False,
        null=False,
    )
    proprietaire = models.ForeignKey(  # Chef de projet ?
        config.settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("Propriétaire"),
        related_name='possede_dossier',
    )
    # liste de participant multiple au dossier, auquel on affecter un rôle et des droits en fonction d'actions
    participants = models.ManyToManyField(
        get_user_model(),
        blank=True,
        through="AffiliationDossierParticipants",
        related_name='participe',
    )
    # document = models.ManyToManyField("dem.Document", blank=True, through="DocumentDossierLink")
    deadline = models.DateField(verbose_name='date butoir', null=True, blank=True)
    priorite_status = models.CharField(  # priorité haute, moyenne, basse, )
        verbose_name=_("Status de la Priorité"),
        max_length=3,
        choices=PRIO_CHOICES,
        default=2,
    )
    priorite_classement = models.PositiveIntegerField(  # classement des priorites dossier vis a vis des dossiers )
        verbose_name="Classement Priorité",
        help_text="classement de la priorité",
        default=None,
        blank=True,
        null=True,
    )

    commentaire = models.TextField(
        verbose_name=_("Commentaire"),
        help_text=_("Commentaire sur l'avancement du dossier"),
        null=True,
        blank=True,
        default=None,
    )

    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    date_modification = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))
    cloture = models.DateField(verbose_name='date de fin', null=True, blank=True)
    # date début du dossier ?

    def __str__(self):
        return "{0} - {1}".format(self.num_dossier, self.nom_dossier)


# class DocumentDossierLink(Model):
#     class Meta:
#         indexes = [
#             models.Index(fields=['document']),
#             models.Index(fields=['dossier']),
#         ]
#
#     document = models.ForeignKey(
#         "dem.Document",
#         on_delete=models.PROTECT,
#     )
#     dossier = models.ForeignKey(
#         "Dossier",
#         on_delete=models.PROTECT,
#     )
#
#     def __str__(self):
#         return "{0} {1}".format(self.document, self.dossier)


class AffiliationDossierParticipants(OModel):
    class Meta:
        indexes = [
            models.Index(fields=['dossier']),
            models.Index(fields=['participant']),
        ]

    dossier = models.ForeignKey(
        "Dossier",
        on_delete=models.PROTECT,
    )
    participant = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
    )
    # role = models.ForeignKey(
    #         common.Role,
    #         on_delete=models.PROTECT, )
    #
    # droit = models.ForeignKey(
    #         common.Droit,
    #         on_delete=models.PROTECT, )
    # action = models.ForeignKey(
    #         common.Action,
    #         on_delete=models.PROTECT, )
    # metier = models.ForeignKey(
    #         common.métier,  #  Chirurgien, manip, infirmière,...
    #         on_delete=models.PROTECT, )
    # discipline = models.ForeignKey(
    #         common.Discipline,
    #         on_delete=models.PROTECT, )

    def __str__(self):
        return "{0} {1}".format(self.dossier, self.participant)


class Execution(OModel):  # à remplacer par un outil de Workflow
    ID = (
        ('0', 'NA'),
        ('1', 'OK'),
        ('2', 'En cours'),
        ('3', 'En attente'),
        ('4', 'Bloqué'),
        ('5', 'Annulé'),
    )
    num_dmd = models.ForeignKey('dem.Demande', on_delete=models.PROTECT)  # ou a partir du prévisionnel ?
    commentaire_cache_acheteur = models.TextField(verbose_name="Remarque de l'acheteur")  # remarque visible uniquement des experts
    commentaire_visible_acheteur = models.TextField(verbose_name="Commentaire de l'acheteur")  # commentaire visible des demandeurs
    etape1_code = models.CharField(max_length=90, choices=ID)
    etape1_comment = models.TextField(verbose_name='Definition du Besoin')
    etape2_code = models.CharField(max_length=90, choices=ID)
    etape2_comment = models.TextField(verbose_name='Essais')
    etape3_code = models.CharField(max_length=90, choices=ID)
    etape3_comment = models.TextField(verbose_name='Devis')
    etape4_code = models.CharField(max_length=90, choices=ID)
    etape4_comment = models.TextField(verbose_name='Marché')
    etape5_code = models.CharField(max_length=90, choices=ID)
    etape5_comment = models.TextField(verbose_name='Commande')
    etape6_code = models.CharField(max_length=90, choices=ID)
    etape6_comment = models.TextField(verbose_name='Livraison')
    etape7_code = models.CharField(max_length=90, choices=ID)
    etape7_comment = models.TextField(verbose_name='Mise en service')
    etape8_code = models.CharField(max_length=90, choices=ID)
    etape8_comment = models.TextField(verbose_name='Réaffectation')

    def __str__(self):
        return "{0}".format(self.num_dmd)

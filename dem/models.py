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
import pytz
from datetime import datetime

from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from django_pandas.managers import DataFrameManager

from common.models import Discipline
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
from document.models import GenericDocument

# from generic_comment.models import GenericComment


def increment_code_number():
    """
    la présente fonction permet de générer le code personnalisée de la demande souforme sous la forme : DEM-YYYY-xxxxx
    En cas de changement d'année, en se basant sur le code de la dernière demande classée par id,
    le compteur se remet à 00000 (sécurisé par champs unique et non editable et par un blocage de la transaction SQL),
    """
    last_demande = Demande.objects.all().order_by('num_dmd').last()
    if not last_demande:  # initialisation condition zéro
        new_demande_id = 'DEM-' + str(timezone.now().strftime('%Y')) + '-00000'
    else:
        code_searched = last_demande.code
        code_searched_id = last_demande.code[9:]
        actual_year = str(timezone.now().strftime('%Y'))
        if code_searched.find(actual_year, 4, 8) == -1:  # année dans Code n'est pas l'année actuelle :
            new_demande_id = 'DEM-' + str(timezone.now().strftime('%Y')) + '-00000'
        else:  # increment du code car même année :
            new_demande_int = int(str(code_searched_id)) + 1
            new_demande_id = 'DEM-' + str(timezone.now().strftime('%Y-')) + str(new_demande_int).zfill(5)
    return new_demande_id


class Campagne(models.Model):
    class Meta:
        verbose_name = _('campagne recensement demandes')
        verbose_name_plural = _('campagne recensement demandes')
        constraints = [
            models.UniqueConstraint(fields=['code'], name='calendrier_code_is_unique'),
        ]
        # Les campagnes sans message (qui sont donc plutôt "normales", sans alerte) arrivent en premier
        #   dans les listes de choix
        ordering = ['message', 'code']

    code: models.CharField = models.CharField(max_length=16, null=True, blank=True)  # Code
    nom: models.CharField = models.CharField(max_length=64, null=True, blank=True)  # Nom du "calendrier"
    description = models.TextField(null=True, blank=True, default=None)  # commentaires si nécessaire
    message = models.TextField(null=True, blank=True, default=None)  # message à présenter à l'utilisateur (alerte ou explications)
    annee = models.IntegerField(
        default='2020',
        null=False,
        verbose_name=_('Annee du Recensement'),  # datetime.now(pytz.utc).year.__str__(),
    )
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.PROTECT,
        help_text=_("les demandes créées seront par défaut configurées pour cette discipline"),
    )
    dispatcher = models.ForeignKey(
        config.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Dispatcher"),
    )
    roles = models.TextField(
        verbose_name=_("Rôles concernés"),
        help_text=_("Liste des rôles (codes séparés par des virgules) ayant accès à cette campagne de rencensement"),
        null=True,
        blank=True,
        default=None,
    )
    natures = models.JSONField(
        verbose_name=_("Natures de demande autorisées"),
        help_text=_("liste des natures de demande autorisées pour cette camapagne de recensement"),
        null=False,
        blank=True,
        default=list,
    )
    debut_recensement = models.DateTimeField(
        null=False,
        # default='2020', #datetime.now(pytz.utc).year.__str__(), #attention ne marche pas
        verbose_name='date début des demandes',
    )
    fin_recensement = models.DateTimeField(null=False, verbose_name=_('date de fin des demandes'))

    def __str__(self):
        return "{0} - {1}".format(self.code, self.nom)


class Arbitrage(models.Model):
    class Meta:
        verbose_name = 'Arbitrage'
        verbose_name_plural = 'Arbitrages'

    code: models.CharField = models.CharField(max_length=8, default='')
    discipline = models.ForeignKey(
        'common.Discipline',
        on_delete=models.PROTECT,
        null=True,
    )
    valeur = models.BooleanField(
        verbose_name=_("Valeur de l'arbitrage"),
        help_text=_("Si 'Vrai', cela signifie que la demande avec cet arbitrage est acceptée."),
        null=False,
        default=False,
    )
    nom: models.CharField = models.CharField(max_length=30)
    commentaire = models.TextField(null=True, blank=True, default=None)
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création')
    cloture = models.DateField(verbose_name='date de fin', null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification')

    def __str__(self):
        return "{0} - {1}".format(self.code, self.nom)


class DemandeStateCodeField(models.CharField):
    """Champ spécial pour calculer l'état d'une demande à partir des différentes valeurs enregistrées
       Cela permet de simuler certaines fonctions d'un workflow (lignes colorées, etc.) sans véritable moteur.

         En fonction de la page (en cours, expertise, toutes)
         et des fonctions de l'utilisateur (chef de pôle, cadre, cadre sup,
       expert, arbitre...), la couleur des lignes pourra varier (cf. table à faire dans la doc)

    Etats calculés (Dans cet ordre !) :

    Phase 1 : Recensement
    ---------------------

    NOUVELLE  : Demande nouvelle, en cours de saisie (aucun avis)
               => Aucune condition

    AVFAV_CSP : Demande avec avis favorable CSP
               => avis_cadre_sup is True

    AVDEF_CSP : Demande avec avis défavorable CSP
               => avis_cadre_sup is False

    VALIDE_CP : Demande validée par le chef de pôle
               => decision_validateur is True

    NONVAL_CP : Demande refusée par le chef de pôle
               => decision_validateur is False

    Phase 2 : Instruction (Attention ! Une demande peut commencer à être instruite avant sa validation !)
    -----------------------------------------------------------------------------------------------------

    INSTRUCTION : Demande attribuée à un expert
    INSTR_OK : Demande avec un montant valide (soit en provenance de l'utilisateur, soit en provenance de l'expert)
    XXXXXXXX : Demande instruite avec avis favorable
    XXXXXXXX : Demande instruite avec avis défavorable
    XXXXXXXX : Demande incorrectement/incomplètement instruite : avis mais pas de montant valide
                (état amené à disparaître avec vrai moteur WF car impossible à atteindre)

    Phase 3 : Arbitrage
    XXXXXXXX : Demande validée par l'arbitre (sur le programme et avec le montant proposés)
    XXXXXXXX : Demande non validée par l'arbitre (cf. commentaire arbitre)
    """

    def pre_save(self, instance, add):
        state_code = 'NOUVELLE'

        # if instance.montant_total_expert_metier is not None:
        #     montant = float(instance.montant_total_expert_metier)
        # elif instance.montant_unitaire_expert_metier is not None:
        #     montant = int(instance.quantite) * float(instance.montant_unitaire_expert_metier)
        # elif instance.montant is not None:
        #     montant = float(instance.montant)
        if instance.prix_unitaire is not None:
            montant = int(instance.quantite) * float(instance.prix_unitaire)
        else:
            montant = None

        if instance.avis_cadre_sup is True:
            state_code = 'AVFAV_CSP'

        if instance.avis_cadre_sup is False:
            state_code = 'AVDEF_CSP'

        if instance.decision_validateur is True:
            state_code = 'VALIDE_CP'

        if instance.decision_validateur is False:
            state_code = 'NONVAL_CP'

        if instance.decision_validateur is False and instance.gel is True:
            state_code = 'NONVAL_CP_DEF'

        if instance.decision_validateur is True and instance.expert_metier is not None:
            state_code = 'INSTRUCTION'

        if instance.decision_validateur is True and instance.expert_metier is not None and montant is not None:
            state_code = 'INSTR_OK'

        if instance.decision_validateur is True and instance.avis_biomed is True:
            state_code = 'AVFAV_EXP'

        if instance.decision_validateur is True and instance.avis_biomed is False:
            state_code = 'AVDEF_EXP'

        if (
            instance.decision_validateur is True
            and instance.arbitrage_commission is not None
            and str(instance.arbitrage_commission.code) in ['1', '2', '5']
        ):
            state_code = 'VALIDE_ARB'

        if (
            instance.decision_validateur is True
            and instance.arbitrage_commission is not None
            and str(instance.arbitrage_commission.code) in ['3', '4', '6']
        ):
            state_code = 'NONVAL_ARB'

        if (
            instance.decision_validateur is True
            and instance.arbitrage_commission is not None
            and str(instance.arbitrage_commission.code) in ['1', '2', '5']
            and instance.gel is True
        ):
            state_code = 'VALIDE_DEF'

        if (
            instance.decision_validateur is True
            and instance.arbitrage_commission is not None
            and str(instance.arbitrage_commission.code) in ['3', '4', '6']
            and instance.gel is True
        ):
            state_code = 'NONVAL_DEF'

        return state_code


# Nature "globale" de la demande, qui permet de configurer le formulaire de départ
NATURE_CHOICES = (
    ('EQ', _("Equipement")),
    ('SW', _("Logiciel")),
    ('TX', _("Travaux")),
    ('PS', _("Prestation")),
    ('CA', _("Consommable / Accessoire")),
    ('AU', _("Autre")),
)


class Demande(models.Model):
    """table renseignée par les utilisateurs"""

    class Meta:
        ordering = ['num_dmd']
        indexes = [
            models.Index(fields=['num_dmd']),
            models.Index(fields=['redacteur']),
            models.Index(fields=['uf']),
            models.Index(fields=['programme']),
            models.Index(fields=['expert_metier']),
            models.Index(fields=['domaine']),
            models.Index(fields=['gel']),
            models.Index(fields=['arbitrage_commission']),
        ]

    PRIO_CHOICES = (
        ('1', 'Haute'),
        ('2', 'Normale'),
        ('3', 'Basse'),
    )

    CAUSE_CHOICES = (
        ('RE', 'Remplacement'),
        ('AQ', 'Augmentation de Quantité'),
        ('EV', 'Evolution'),
        ('TN', 'Technique Nouvelle'),
        ('RA', 'Rachat fin de marché'),
    )
    # numéro unique de la demande
    num_dmd = models.AutoField(
        primary_key=True,
    )
    calendrier = models.ForeignKey(
        'dem.Campagne',
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )

    campagne_redirect = models.ForeignKey(
        'dem.Campagne',
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
        related_name='demande_redirect',
    )

    nature: models.CharField = models.CharField(
        verbose_name=_("Nature"),
        max_length=2,
        choices=NATURE_CHOICES,
        default='EQ',
        help_text=_("Nature de la demande : Matériel, logiciel, travaux..."),
    )

    # Discipline au moment de la demande (ne sera pas nécessairement la discipline finale
    discipline_dmd = models.ForeignKey(
        'common.Discipline',
        on_delete=models.PROTECT,
        verbose_name=_("Discipline"),
    )
    # = Date de la demande (complète, finalement)
    date = models.DateField(
        verbose_name=_("Date de la demande"),
        default=timezone.now,
        blank=True,
        null=True,
    )
    # Titre du projet, si plusieurs demande sont liées
    nom_projet: models.CharField = models.CharField(
        verbose_name=_("Nom du Projet"),
        max_length=120,
        default=None,
        blank=False,
        null=False,
        help_text=_(
            "Si plusieurs demandes concernent un même projet, \
            donner le même nom de projet. Sinon, le projet est la demande en elle-même (rempli automatiquement).\
            Sauf exception, toutes les demandes d'un même projet seront validées (ou pas) simultanément."
        ),
    )
    target: models.CharField = models.CharField(
        verbose_name=_("Cible"),
        help_text=_(
            "'programme' ou 'année' cible de la demande. Si Null, la demande est immédiate."
            " Si c'est une année, c'est l'année pour laquelle la demande sera pertinente."
            " Ce champ sert à prévoir par anticipation des plans d'équipement,"
            " par exemple pour un gros projet ou pour le PPI."
        ),
        max_length=256,
        default=None,
        blank=True,
        null=True,
    )
    description = models.TextField(null=True, blank=True, default=None)  # commentaires si nécessaire
    localisation: models.CharField = models.CharField(max_length=128, default=None, blank=True, null=True)
    # décision OUI/NON/vide du cadre sup
    # Personne qui a rédigé la demande
    redacteur = models.ForeignKey(
        config.settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("Rédacteur"),
    )

    # nom du cadre sup ayant porté son avis // Should be a ForeignKey on Users
    nom_cadre_sup = models.ForeignKey(
        config.settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        related_name='demandes_avis_donne',
    )
    # décision OUI/NON/vide du cadre sup
    avis_cadre_sup = models.IntegerField(verbose_name=_("Avis cadre sup"), help_text="", blank=True, null=True)
    # commentaire du cadre sup
    commentaire_cadre_sup = models.TextField(default=None, blank=True, null=True)

    # personne qui a approuvé la demande (chef de pôle, directeur, etc.) // Should be a ForeignKey on Users
    validateur = models.ForeignKey(
        config.settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        related_name='demandes_approuvees',
    )
    # décision OUI/NON/vide de l'approbateur
    decision_validateur = models.IntegerField(verbose_name=_("Approbation"), help_text="", blank=True, null=True)
    # commentaire lors de l'approbation
    decision_soumission = models.TextField(default=None, blank=True, null=True)
    # date de l'approbation (ou non). Pour les demandes d'intéressement, il s'agit de la date de passage en bureau de pôle
    date_decision = models.DateField(verbose_name=_("date décision"), default=None, blank=True, null=True)

    uf = models.ForeignKey(
        'common.Uf',
        on_delete=models.PROTECT,
    )
    nom_organisation: models.CharField = models.CharField(max_length=50, null=True, blank=True)
    code_pole: models.CharField = models.CharField(max_length=8, default='0000', verbose_name=_("Code pôle"))
    nom_pole_court: models.CharField = models.CharField(max_length=50, null=True, blank=True)
    code_uf: models.CharField = models.CharField(
        verbose_name=_("Code UF"),
        help_text=_("Code de l'UF qui va bénéficier de ce matériel"),
        max_length=8,
        default='0000',
    )
    nom_uf_court: models.CharField = models.CharField(max_length=50, null=True, blank=True)
    # Personne du service à l'origine  de la demande
    referent: models.CharField = models.CharField(
        verbose_name=_("Référent"),
        help_text=(
            "Personne du service à l'origine  de la demande, \
            qui peut être contactée pendant l'instruction pour avoir des précisions."
        ),
        max_length=30,
        default=None,
        blank=False,
        null=True,
    )
    # personne avec qui l'acheteur prendra contact pour avoir des information
    # concernant la demande et pour re-définir le besoin
    contact = models.CharField(
        verbose_name=_("Contact"),
        help_text=_(
            "Nom de la personne qui sera contactée pour gérer l'acquisition et/ou représenter les utilisateurs"
            " lors de l'opération d'acquisition."
            " Le référent est utilisé par défaut."
        ),
        max_length=30,
        default=None,
        blank=True,
        null=True,
    )
    # DECT du contact
    dect_contact = models.CharField(
        verbose_name=_("Téléphone / DECT"),
        help_text=_("Coordonnées téléphoniques de la personne à contacter (si possible un numéro de DECT)"),
        max_length=30,
        default=None,
        blank=True,
        null=True,
    )

    # année de premiere demande automatiquement renseignée : lors de la \
    # première inscription dans le fichier ou lors de la récupération
    # d'une demande refusée antérieurement.
    date_premiere_demande = models.DateField(
        verbose_name=_("Première demande"),
        help_text=_("Année où la demande a été présentée la première fois à la Commission d'arbitrage"),
        default=datetime.now(pytz.utc).year.__str__() + '-' + '01' + '-' + '01',
        blank=True,
        null=True,
    )
    # priorité de la demande estimée par le rédacteur
    priorite = models.CharField(verbose_name=_("Priorité"), max_length=3, choices=PRIO_CHOICES, default=2)
    # nom court de la demande
    libelle = models.CharField(
        verbose_name=_("Objet de la demande"),
        help_text=_("Indiquez le nom (commun) du matériel demandé"),
        max_length=120,
        default=None,
        blank=False,
        null=False,
    )
    cause = models.CharField(
        verbose_name=_("Raison"),
        max_length=3,
        choices=CAUSE_CHOICES,
        default='AQ',
        help_text=_("C'est la raison pour laquelle cette demande est faite."),
    )
    # Materiel existant concerné ()
    materiel_existant = models.CharField(
        verbose_name=_("Matériel concerné"),
        help_text=_("Matériel existant concerné par la demande de remplacement ou d'évolution."),
        max_length=64,
        default=None,
        blank=True,
        null=True,
    )

    # quantité demandé par le service
    quantite = models.DecimalField(
        verbose_name=_("Quantité"),
        max_digits=3,
        decimal_places=0,
        default=1,
        blank=False,
        null=False,
        help_text=_("Quantité d'équipements souhaités"),
    )

    # prix unitaire renseigné par demandeur
    prix_unitaire = models.DecimalField(
        verbose_name=_("P.Unit. (TTC)"),
        help_text=_(
            "Indiquer ici une estimation du prix unitaire de l'équipement, \
            en euros TTC, de l'équipement demandé. S'il s'agit d'une technique  nouvelle, \
            il est indispensable de joindre un devis à la demande."
        ),
        max_digits=9,
        decimal_places=2,
        default=None,
        blank=True,
        null=True,
    )

    # existe-t-il des surcout en consommables, travaux, maintenance,
    # informatique... pour utiliser/installer l'appareil demandé
    couts_complementaires = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name=_("Coûts de fonctionnement"),
        help_text=_(
            "Existe-t-il des coûts de consommables, de maintenance, de travaux \
            ou d'autres coûts lié à l'achat ou l'utilisation de ce matériel ?"
        ),
    )

    # argumentation des utilisateurs
    autre_argumentaire = models.CharField(
        verbose_name=_("Autre justification"),
        max_length=3000,
        default=None,
        blank=True,
        help_text=_("Autre raison pour laquelle vous demandez ce matériel"),
    )

    # Calcul automatique du cout du projet sur 7 ans => voir comment intégrer
    # le résultat de calculs automatiques.
    # montant_bak = models.DecimalField(
    #     verbose_name=_("Montant de la demande (TTC)"),
    #     help_text=_("Par défaut, le montant est calculé à partir de la quantité et du prix unitaire."),
    #     max_digits=9,
    #     decimal_places=2,
    #     default=None,
    #     blank=True,
    #     null=True,
    # )

    # consommables éventuels
    consommables_eventuels = models.CharField(
        verbose_name=_("Consommables"),
        max_length=3000,
        default=None,
        blank=True,
        null=True,
        help_text=_(
            "Consommables éventuels (stériles ou non) associé à l'équipement demandé :"
            " Types, description, quantités annuelles..."
        ),
    )

    impact_travaux = models.BooleanField(
        default=None,
        blank=True,
        null=True,
        verbose_name=_("Impact travaux"),
        help_text=_("Ce projet nécessite-t-il de réaliser des travaux ?"),
    )

    impact_informatique = models.BooleanField(
        default=None,
        blank=True,
        null=True,
        verbose_name=_("Impact informatique"),
        help_text=_("Ce projet nécessite-t-il des ressources informatiques (logiciel, matériel, réseau...) ?"),
    )

    # code_expert_metier = models.ForeignKey(
    # 'common.ExpertMetier',
    # blank=True,
    # null=True,
    # on_delete=models.PROTECT)

    dispatcher_note = models.TextField(
        verbose_name=_("Note responsable campagne"),
        help_text=_(
            "Commentaire de la personne chargées de répartir" " la demande entre les programmes de la campagne de recensement"
        ),
        null=True,
        blank=True,
    )

    expert_metier = models.ForeignKey(
        config.settings.AUTH_USER_MODEL,
        db_column='expert_user',
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
        related_name='demande_comme_expert',
    )

    # montant unitaire estimé par l'expert/acheteur
    montant_unitaire_expert_metier = models.DecimalField(
        max_digits=9,
        verbose_name="Montant unitaire estimé par l'expert métier",
        decimal_places=0,
        default=None,
        blank=True,
        null=True,
        help_text=_("Montant unitaire estimé par l'expert métier en fonction du projet"),
    )

    # montant total estimé par l'expert/acheteur : = quantite x montant acheteur unitaire
    # montant_total_expert_metier_bak = models.DecimalField(
    #     max_digits=9,
    #     verbose_name="Montant Total estimé par l'expert métier",
    #     decimal_places=0,
    #     default=None,
    #     blank=True,
    #     null=True,
    #     help_text=_("Montant Total estimé par l'expert métier en fonction du projet et des quantités souhaitées"),
    # )

    # acquisition possible annee N
    acquisition_possible = models.BooleanField(verbose_name='Acquisition possible en année N', blank=True, null=True)

    # quantité validée par commission
    quantite_validee = models.DecimalField(
        verbose_name=_("Quantité validée"),
        max_digits=4,
        decimal_places=0,
        blank=True,
        null=True,
        help_text=_("quantité d'équipements validée par commission"),
    )

    # montant de l'enveloppe allouée par la commission pour cette
    # demande => = quantitévalidée x montant unitaire acheteur
    enveloppe_allouee = models.DecimalField(
        verbose_name=_("montant de l'enveloppe allouée"),
        help_text=_("enveloppe financière allouée par la commission"),
        max_digits=9,
        decimal_places=0,
        default=None,
        blank=True,
        null=True,
    )

    # plan d'équipement (service acheteur) concerné
    programme = models.ForeignKey(
        'common.Programme',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    # domaine d'achat
    domaine = models.ForeignKey('common.Domaine', blank=True, null=True, on_delete=models.PROTECT)

    # avis de l'acheteur/expert biomédical
    avis_biomed = models.BooleanField(verbose_name="Avis de l'expert métier", help_text="", blank=True, null=True)

    commentaire_biomed = models.TextField(default=None, blank=True, null=True)

    documents_generic = GenericRelation(GenericDocument, related_query_name='demande')

    # avis provisoire, puis définitif de la commission
    arbitrage_commission = models.ForeignKey(
        'Arbitrage',
        verbose_name="Arbitrage de la commission",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    # COMMENTAIRE_COMMISSION_PROVISOIRE
    commentaire_provisoire_commission = models.TextField(
        help_text="Commentaires de la commission lors des auditions",
        default=None,
        blank=True,
        null=True,
    )

    # COMMENTAIRE_COMMISSION_DEFINITIF
    commentaire_definitif_commission = models.TextField(
        help_text=_("Commentaires définitifs de la commission concernant la demande"),
        default=None,
        blank=True,
        null=True,
    )

    # Etat de la demande dans le workflow (duck typing name : Ne pas changer le nom du champ !)
    # C'est un champ calculé
    # MAIS le calcul n'est pas automatique (pour l'instant) : Il faut sauver ce champ avec les autres pour
    # déclencher le calcul !
    state_code = DemandeStateCodeField(
        max_length=16,
        verbose_name=_("Etat de la demande"),
        default=None,
        blank=True,
        null=True,
    )

    # Flag pour le gel de la demande (clôture du traitement ==> acceptée ou refusée)
    gel = models.BooleanField(blank=True, null=False, default=False)

    arg_interet_medical = models.BooleanField(
        verbose_name=_("Intérêt médical"),
        help_text=_("Cette demande apporte-t-elle un intérêt médical ?"),
        default=False,
    )
    arg_commentaire_im = models.TextField(
        verbose_name=_("Précisions sur l'intérêt médical"),
        help_text=_(
            "Indiquez ici quel bénéfice ce matériel pourrait apporter à la prise en charge."
            " N'hésitez pas à joindre des documents (publications, références, expériences, ...)"
            " à la demande pour appuyer votre argumentation."
        ),
        blank=True,
    )
    arg_oblig_reglementaire = models.BooleanField(
        verbose_name=_("Obligation réglementaire"),
        help_text=_("Existe-t-il une obligation réglementaire liée à cette demande ?"),
        default=False,
    )
    arg_commentaire_or = models.TextField(
        verbose_name=_("Précisions sur l'obligation réglementaire"),
        help_text=_(
            "Indiquez ici quelle est l'obligation réglementaire"
            " (référence du texte) et en quoi cela participe à l'argumentation."
            "\n\nN'hésitez pas à joindre des documents (textes, analyse...)"
            " à la demande pour appuyer votre argumentation."
        ),
        blank=True,
    )
    arg_recommandations = models.BooleanField(
        verbose_name=_("Recommandations"),
        help_text=_("Y a-t-il des recommandations liées à cette demande ?"),
        default=False,
    )
    arg_commentaire_r = models.TextField(
        verbose_name=_("Précisions recommandations"),
        help_text=_(
            "Indiquez quelles sont les recommandations (références, organisme)"
            " et comment elles sont en faveur de la demande.\
            \n\nN'hésitez pas à joindre des documents (recommandations) à la demande pour appuyer votre argumentation."
        ),
        blank=True,
    )
    arg_projet_chu_pole = models.BooleanField(
        verbose_name=_("Projet institutionnel"),
        help_text=_("La demande est-elle liée à un projet de pôle ou au projet d'établissement ?"),
        default=False,
    )
    arg_commentaire_pcp = models.TextField(
        verbose_name=_("Précisions projet institutionnel"),
        help_text=_(
            "Préciser si la demande est liée à un projet du pôle ou de l'établissement"
            " et le niveau de validation du projet en question.\n\n"
            " N'hésitez pas à joindre des documents (descriptif du projet, validation...)"
            " à la demande pour appuyer votre argumentation."
        ),
        blank=True,
    )
    arg_confort_patient = models.BooleanField(
        verbose_name=_("Confort patient"),
        help_text=_("La demande a-t-elle en vue d'améliorer le confort patient ?"),
        default=False,
    )
    arg_commentaire_cp = models.TextField(
        verbose_name=_("Précisions confort patient"),
        help_text=_(
            "Précisez comment l'objet de la demande pourra améliorer le confort ou l'expérience des patients."
            "\n\nN'hésitez pas à joindre des documents (articles, essais...)"
            " à la demande pour appuyer votre argumentation."
        ),
        blank=True,
    )
    arg_confort_perso_ergo = models.BooleanField(
        verbose_name=_("Ergonomie du travail"),
        help_text=_("La demande améliore-t-elle l'ergonomie ou le confort du personnel ?"),
        default=False,
    )
    arg_commentaire_pe = models.TextField(
        verbose_name=_("Précisions sur l'ergonomie"),
        help_text=_(
            "Détaillez quel impact sur l'ergonomie ou le confort du personnel pourrait avoir la demande"
            "\n\nN'hésitez pas à joindre des documents (étude de poste, etc.)"
            " à la demande pour appuyer votre argumentation."
        ),
        blank=True,
    )
    arg_notoriete = models.BooleanField(
        verbose_name=_("Notoriété, Attractivité"),
        help_text=_("La demande permettrait-elle d'améliorer la notoriété de l'établissement ?"),
        default=False,
    )
    arg_commentaire_n = models.TextField(
        verbose_name=_("Précisions sur la notoriété"),
        help_text=_(
            "Indiquez ici comment l'accord de la demande participerait à la notoriété de l'établissement"
            "au sein du territoire et avec quelle ampleur\n\nN'hésitez pas à joindre des documents"
            "(rapport de consultant, etc.) à la demande pour appuyer votre argumentation."
        ),
        blank=True,
    )
    arg_innovation_recherche = models.BooleanField(
        verbose_name="Innovation / Recherche",
        help_text="La demande concerne-t-elle un projet innovant ou de recherche ?",
        default=False,
    )
    arg_commentaire_ir = models.TextField(
        verbose_name="Précisions innovation/recherche",
        help_text="Indiquez ici en quoi cette demande participerait à l'innovation,\
            les éventuels liens avec la commission innovation pour le financement du fonctionnement.\
            Vous pouvez aussi préciser le nom du projet du reherche associé.\
            \n\nN'hésitez pas à joindre des documents (article scientifique, projet de recherche, etc.)\
            à la demande pour appuyer votre argumentation.",
        blank=True,
    )
    arg_mutualisation = models.BooleanField(
        verbose_name="Mutualisation",
        help_text="L'équipement demandé sera-il mutualisé avec d'autres services ?",
        default=False,
    )
    arg_commentaire_m = models.TextField(
        verbose_name="Précisions sur la mutualisation",
        help_text=_(
            "Préciser avec quel(s) autre(s) service(s) la mutualisation est envisagée,"
            "selon quelles modalités (répartition des plages horaires, vacations, etc.)"
            "\n\nN'hésitez pas à joindre des documents (planning de partage, accord autre service, CR de réunion...)"
            "à la demande pour appuyer votre argumentation."
        ),
        blank=True,
    )
    arg_gain_financier = models.BooleanField(
        verbose_name="Gains économiques",
        help_text="La demande permettrait-elle de réaliser des gains économiques ?",
        default=False,
    )
    arg_commentaire_gf = models.TextField(
        verbose_name="Précisions gains économiques",
        help_text=_(
            "Précisez ici comment la demande pourrait entrainer une économie ou une recette pour l'établissement."
            " \n\nN'hésitez pas à joindre des documents (étude médico-économique, business plan...)"
            " à la demande pour appuyer votre argumentation."
        ),
        blank=True,
    )

    # ==============================================================================================
    # Champs spécifiques aux demandes de travaux

    # Provisoirement, on fait une liste de choix simple
    # A terme, quand il y aura une gestion patrimoniale complète, on reverra peut-être avec une FK
    TVX_BATIMENT_CHOICE = (
        ('NCHU', _("Nouveau CHU (Halls 1 et 2)")),
        ('H3', _("Bâtiment Fontenoy (Halls 3)")),
        ('SVP', _("Saint-Vincent de Paul")),
        ('SV', _("Saint-Victor")),
        ('HN', _("Hôpital Nord")),
        ('EC', _("Ecoles")),
        ('SIM', _("SimUSanté")),
        ('TEP', _("TEP")),
        ('CBH', _("CBH")),
        ('HEM', _("Hémato")),
        ('BB', _("Biobanque")),
        ('AU', _("Autre")),
    )

    tvx_batiment: models.CharField = models.CharField(
        max_length=8,
        choices=TVX_BATIMENT_CHOICE,
        null=True,
        blank=True,
    )

    TVX_ETAGE_CHOICE = (
        ('SS', "Sous-sol"),
        ('RDJ', "Rez-de-Jardin"),
        ('RDC', "Rez-de-Chaussée"),
        ('1', "1er étage"),
        ('2', "2ème étage"),
        ('3', "3ème étage"),
        ('4', "4ème étage"),
        ('5', "5ème étage"),
        ('6', "6ème étage"),
    )
    tvx_etage = models.CharField(
        max_length=8,
        choices=TVX_ETAGE_CHOICE,
        null=True,
        blank=True,
    )
    tvx_arg_normes = models.BooleanField(
        verbose_name=_("Mise aux normes"),
        # help_text=_("TODO..."),
        default=False,
    )
    tvx_arg_normes_comment = models.TextField(
        verbose_name=_("Mise aux normes"),
        # help_text=_("TODO..."),
        null=True,
        blank=True,
    )
    tvx_arg_reorg = models.BooleanField(
        verbose_name=_("Réorganisation des activités"),
        # help_text=_("TODO..."),
        default=False,
    )
    tvx_arg_reorg_comment = models.TextField(
        verbose_name=_("Réorganisation des activités"),
        # help_text=_("TODO..."),
        null=True,
        blank=True,
    )
    tvx_arg_devact = models.BooleanField(
        verbose_name=_("Développement de l’activité"),
        # help_text=_("TODO..."),
        default=False,
    )
    tvx_arg_devact_comment = models.TextField(
        verbose_name=_("Développement de l’activité"),
        # help_text=_("TODO..."),
        null=True,
        blank=True,
    )
    tvx_arg_eqpt = models.BooleanField(
        verbose_name=_("Arrivée d'un équipement"),
        # help_text=_("TODO..."),
        default=False,
    )
    tvx_arg_eqpt_comment = models.TextField(
        verbose_name=_("Arrivée d'un équipement"),
        # help_text=_("TODO..."),
        null=True,
        blank=True,
    )
    tvx_arg_qvt = models.BooleanField(
        verbose_name=_("Confort et/ou sécurité des personnels"),
        # help_text=_("TODO..."),
        default=False,
    )
    tvx_arg_qvt_comment = models.TextField(
        verbose_name=_("Confort et/ou sécurité des personnels"),
        # help_text=_("TODO..."),
        null=True,
        blank=True,
    )
    tvx_arg_securite = models.BooleanField(
        verbose_name=_("Confort et/ou sécurité des patients"),
        # help_text=_("TODO..."),
        default=False,
    )
    tvx_arg_securite_comment = models.TextField(
        verbose_name=_("Confort et/ou sécurité des patients"),
        # help_text=_("TODO..."),
        null=True,
        blank=True,
    )
    tvx_arg_vetustes = models.BooleanField(
        verbose_name=_("Locaux vétustes"),
        # help_text=_("TODO..."),
        default=False,
    )
    tvx_arg_vetustes_comment = models.TextField(
        verbose_name=_("Locaux vétustes"),
        # help_text=_("TODO..."),
        null=True,
        blank=True,
    )

    tvx_contrainte_lib = models.BooleanField(
        verbose_name=_("Les locaux seront libérés"),
        # help_text=_("TODO..."),
        default=False,
    )

    tvx_contrainte_alib = models.BooleanField(
        verbose_name=_("Des locaux provisoires devront être aménagés pendant la période de travaux"),
        # help_text=_("TODO..."),
        default=False,
    )

    tvx_contrainte_lar = models.BooleanField(
        verbose_name=_("Les travaux sont situés dans une zone à risque particulier"),
        # help_text=_("TODO..."),
        default=False,
    )

    tvx_contrainte_autre = models.BooleanField(
        verbose_name=_("Autre contrainte (précisez ci-dessous)"),
        # help_text=_("TODO..."),
        default=False,
    )

    tvx_contrainte = models.TextField(
        verbose_name=_("Précisions sur les contraintes"),
        # help_text=_("TODO..."),
        null=True,
        blank=True,
    )

    TVX_PRIORITE = (
        ('1', _("Locaux particulièrement vétustes, travaux indispensables")),
        ('2', _("Nécessite des aménagements,  à l'origine de probleme d'exploitation")),
        ('3', _("Amélioration significative des locaux ou du fonctionnement")),
        ('4', _("Axe de progrès")),
    )
    tvx_priorite = models.CharField(
        verbose_name=_("Priorité"),
        # help_text=_("TODO..."),
        choices=TVX_PRIORITE,
        max_length=8,
        null=True,
        blank=True,
    )
    tvx_eval_devact = models.IntegerField(
        verbose_name=_("Evaluation développement d'activité"),
        # help_text=_("TODO..."),
        null=True,
        blank=True,
    )
    tvx_eval_contin = models.IntegerField(
        verbose_name=_("Evaluation continuité exploitation"),
        # help_text=_("TODO..."),
        null=True,
        blank=True,
    )
    tvx_eval_confort = models.IntegerField(
        verbose_name=_("Evaluation confort patients/personnel"),
        # help_text=_("TODO..."),
        null=True,
        blank=True,
    )
    tvx_eval_securite = models.IntegerField(
        verbose_name=_("Evaluation sécurité"),
        # help_text=_("TODO..."),
        null=True,
        blank=True,
    )
    tvx_eval_qvt = models.IntegerField(
        verbose_name=_("Evaluation QVT"),
        # help_text=_("TODO..."),
        null=True,
        blank=True,
    )
    # ==============================================================================================

    it_caracteristiques_minimales = models.TextField(
        verbose_name=_("Caractéristiques minimales"),
        # help_text=_("TODO..."),
        null=True,
        blank=True,
    )

    it_a_installer = models.TextField(
        verbose_name=_("Produits/logiciels à installer"),
        # help_text=_("TODO..."),
        null=True,
        blank=True,
    )

    it_cout_formation = models.DecimalField(
        max_digits=9,
        verbose_name=_("Coût de la formation associée"),
        decimal_places=0,
        default=None,
        blank=True,
        null=True,
        help_text=_("Coût de la formation associée au logiciel (par personne ou pour un groupe)"),
    )

    # ==============================================================================================
    # Champs provisoires pour la gestion de l'intéressement CHU Amiens-Picardie
    # ==============================================================================================
    tmp_int_year = models.IntegerField(
        verbose_name=_("Année enveloppe intéressement"),
        default=None,
        blank=True,
        null=True,
    )
    tmp_int_remain = models.DecimalField(
        max_digits=9,
        verbose_name=_("Montant restant de l'enveloppe d'intéressement"),
        decimal_places=2,
        default=None,
        blank=True,
        null=True,
        help_text=_(""),
    )

    # ==============================================================================================

    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date de création', null=True)

    date_modification = models.DateTimeField(auto_now=True, verbose_name='date de modification', null=True)

    # Generic fields

    # comments = GenericRelation(GenericComment, related_query_name='demande')

    code = models.CharField(
        max_length=400, default=increment_code_number, editable=False
    )  # TODO : quand ce sera valider à mettre en editable=False
    objects = DataFrameManager()

    workflow_alert = models.CharField(
        verbose_name=_("Alerte traitement"),
        max_length=1024,
        default=None,
        blank=True,
        null=True,
    )

    analyse = models.JSONField(
        verbose_name=_("Analyse technique de la demande"),
        default=None,
        blank=True,
        null=True,
    )

    def __str__(self):
        # return "{0}  {1}  {2}  {3}".format(self.num_dmd, self.nom_projet, self.contact, self.dectcontact)
        return "{} - {}".format(self.code, self.libelle)

    def get_absolute_url(self):
        return reverse('dem:demande', kwargs={'pk': self.pk})


class CoutComplementaire(models.Model):
    """table des surcout liés à chaque demande"""

    class Meta:
        indexes = [
            models.Index(fields=['num_dmd']),
        ]

    TYPE_SURCOUT = (
        (1, 'Consommable'),
        (2, 'Maintenance'),
        (3, 'Informatique'),
        (4, 'Travaux'),
        (5, 'Autre'),
    )
    type_surcout = models.DecimalField(choices=TYPE_SURCOUT, max_digits=5, decimal_places=0, blank=True, null=True)
    nom_surcout = models.CharField(max_length=50, blank=True, null=True)
    reference_surcout = models.CharField(max_length=50, blank=True, null=True)
    cout_unitaire_surcout = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        blank=True,
        verbose_name='cout unitaire',
    )
    qt_annuelle_surcout = models.DecimalField(
        max_digits=5,
        blank=True,
        decimal_places=0,
        verbose_name='quantité annuelle',
    )
    num_dmd = models.ForeignKey('Demande', blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return "{0}".format(self.type_surcout)

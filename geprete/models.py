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
from django.db import models
from django.utils.translation import gettext as _

from django.contrib.contenttypes.fields import GenericRelation
from generic_comment.models import GenericComment

from common.models import Uf


class Geprete(models.Model):

    """Liste des prêts réalisés"""

    UNITE = (
        ("J", "jours"),
        ("S", "semaines"),
        ("M", "mois"),
    )

    id = models.AutoField(primary_key=True)
    marque = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    num_inv = models.TextField()
    uf_preteur = models.ForeignKey(Uf, blank=True, null=True, on_delete=models.PROTECT, related_name='uf_preteur')
    uf_receveur = models.ForeignKey(Uf, null=True, on_delete=models.PROTECT, related_name='uf_receveur')
    contact_preteur = models.TextField(
        blank=True,
        null=True,
        help_text=_("Nom et numéro de télépone de la personne qui fait le prêt"),
    )
    contact_receveur = models.TextField(
        blank=True,
        null=True,
        help_text=_("Nom et numéro de télépone de la personne qui reçoit le prêt"),
    )
    date_demande = models.DateField(blank=True, null=True)
    debut_pret = models.DateField()
    fin_pret = models.DateField(blank=True, null=True)
    duree_pret = models.DecimalField(blank=True, null=True, decimal_places=1, max_digits=2)
    unite = models.CharField(choices=UNITE, max_length=180)
    # comm_pret = models.TextField(blank=True, null=True)
    # Generic fields
    documents = GenericRelation(GenericComment, related_query_name='geprete')
    comments = GenericRelation(GenericComment, related_query_name='geprete')

    def __str__(self):
        return "{0}".format(self.num_inv)


class Gessaye(models.Model):

    """Liste des essais réalisés dans les services - géré par le biomed et le service en question"""

    UNITE = (
        ("J", "jours"),
        ("S", "semaines"),
        ("M", "mois"),
    )

    id = models.AutoField(primary_key=True)
    numero_de_serie = models.CharField(blank=True, null=True, max_length=180)
    quantite = models.IntegerField()
    type = models.CharField(max_length=180)
    marque = models.CharField(max_length=180)
    accessoires = models.TextField(blank=True, null=True)
    descriptif = models.TextField(blank=True, null=True)
    num_ce = models.CharField(blank=True, null=True, max_length=180)
    debut = models.DateField()
    fin = models.DateField(blank=True, null=True)
    reprise = models.DateField(blank=True, null=True)
    duree = models.DecimalField(blank=True, null=True, decimal_places=1, max_digits=2)  # mettre un int si c'est penible
    unite_duree = models.CharField(choices=UNITE, max_length=180)
    ingenieur_responsable = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    unite_fonctionnelle = models.ForeignKey(Uf, on_delete=models.PROTECT)
    nom_emprunteur = models.CharField(blank=True, null=True, max_length=180)
    fournisseur = models.CharField(max_length=180)
    contact_fournisseur = models.TextField()
    coord_fournisseur = models.TextField()
    commentaire = models.TextField(blank=True, null=True)
    documents = GenericRelation(GenericComment, related_query_name='geprete')
    comments = GenericRelation(GenericComment, related_query_name='geprete')
    # CASCADE supprime en cascade PROTECT le protège

    def __str__(self):
        return "{0}- {1} - {2}".format(self.id, self.type, self.marque)
